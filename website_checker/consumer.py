# Copyright (C) 2021 yifeizuo@gmail.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import psycopg2
import socket
from kafka import KafkaConsumer
from result import WebsiteCheckResult

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger("consumer")
CURRENT_PATH = os.path.dirname(__file__)


class DbWriter(object):
    def __init__(self,
                 db_host: str = os.getenv("DB_HOST", "localhost"),
                 db_port: str = os.getenv("DB_PORT", "5432"),
                 db_name: str = os.getenv("DB_NAME", "my_db"),
                 db_user: str = os.getenv("DB_USER", "my_user"),
                 db_password: str = os.getenv("DB_PASSWORD", "my_password")) -> None:
        self.conn = psycopg2.connect(
            host=db_host,
            port=int(db_port),
            dbname=db_name,
            user=db_user,
            password=db_password,
        )
        logger.info("Connected to DB host:{}, port:{}, name:{}, user:{}".format(db_host, db_port, db_name, db_user))

        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS website_checker_result (id serial PRIMARY KEY,
                    check_timestamp timestamp UNIQUE NOT NULL,
                    response_time DOUBLE PRECISION,
                    status_code INTEGER,
                    response_data_regex TEXT,
                    is_regex_matched BOOLEAN
                    );
            """)
        self.conn.commit()

    def insert_data(self, result: WebsiteCheckResult, enable_aggregate_data_as_hourly: bool) -> None:
        if enable_aggregate_data_as_hourly:
            # check_timestamp is stripped to floored hour to be aggregated
            check_timestamp = result.check_timestamp.replace(minute=0, second=0, microsecond=0)
        else:
            check_timestamp = result.check_timestamp

        self.cur.execute(
            """
            INSERT INTO website_checker_result (check_timestamp, response_time, status_code, response_data_regex, is_regex_matched)
                VALUES (%(check_timestamp)s, %(response_time)s, %(status_code)s, %(response_data_regex)s, %(is_regex_matched)s)
                ON CONFLICT (check_timestamp) DO UPDATE
                SET response_time = EXCLUDED.response_time, status_code = EXCLUDED.status_code, response_data_regex = EXCLUDED.response_data_regex, is_regex_matched = EXCLUDED.is_regex_matched
            """,
            {
                'check_timestamp': check_timestamp,
                'response_time': result.response_time,
                'status_code': result.status_code,
                'response_data_regex': result.response_data_regex,
                'is_regex_matched': result.is_regex_matched
            }
        )
        self.conn.commit()
        logger.info("Written to DB.")

    def close_db_connection(self) -> None:
        self.cur.close()
        self.conn.close()
        logger.info("Closed DB connection.")


class WebsiteCheckResultConsumer(object):
    def __init__(self, db_writer: DbWriter,
                 topic: str = os.getenv("KAFKA_TOPIC", "example-topic"),
                 enable_aggregate_data_as_hourly: bool = bool(os.getenv("AGGREGATE_DATA_AS_HOURLY", False))) -> None:
        self.topic = topic
        self.enable_aggregate_data_as_hourly = enable_aggregate_data_as_hourly
        self.db_writer = db_writer
        self.consumer = KafkaConsumer(
            self.topic,
            group_id="aiven",
            client_id=socket.gethostname(),
            auto_offset_reset='earliest',
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "example-server"),
            security_protocol="SSL",
            ssl_cafile=os.path.abspath(os.path.join(CURRENT_PATH, '..', 'ssl', 'ca.pem')),
            ssl_certfile=os.path.abspath(os.path.join(CURRENT_PATH, '..', 'ssl', 'service.cert')),
            ssl_keyfile=os.path.abspath(os.path.join(CURRENT_PATH, '..', 'ssl', 'service.key')),
        )

    def consume_loop(self) -> None:
        self.consumer.subscribe([self.topic])

        while True:
            raw_messages = self.consumer.poll(timeout_ms=1000)

            for topic, msgs in raw_messages.items():
                if len(msgs) == 0:
                    logger.info("No message from topic {}.".format(topic))
                    continue
                for msg in msgs:
                    received_result: WebsiteCheckResult = WebsiteCheckResult.deserialize(msg.value)
                    if received_result.is_valid():
                        logger.info('Received message: {} from topic {}.'.format(received_result.result(), topic))
                        self.db_writer.insert_data(received_result, self.enable_aggregate_data_as_hourly)
                    else:
                        logger.warning('Received message is unrecognised. {}. Topic: {}.'.format(msg.value.decode(), topic))

    def close(self) -> None:
        self.consumer.close()
        self.db_writer.close_db_connection()


def main():
    consumer = None
    try:
        consumer = WebsiteCheckResultConsumer(DbWriter())
        consumer.consume_loop()
    except Exception as err:
        logger.error("Exception raised {}.".format(err))
        raise err
    except KeyboardInterrupt:
        logger.info("Exiting...")
    finally:
        if consumer:
            consumer.close()


if __name__ == "__main__":
    main()
