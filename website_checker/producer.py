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

from typing import Optional
from time import sleep
from kafka import KafkaProducer
import requests
import os
import logging
import re
from website_checker.result import WebsiteCheckResult

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger("producer")
CURRENT_PATH = os.path.dirname(__file__)


class Producer(object):
    def __init__(self,
                 topic: str = os.getenv("KAFKA_TOPIC", "example-topic"),
                 bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "example-host:1234")) -> None:
        self.topic = topic

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol="SSL",
            ssl_cafile=os.path.abspath(os.path.join(CURRENT_PATH, '..', 'ssl', 'ca.pem')),
            ssl_certfile=os.path.abspath(os.path.join(CURRENT_PATH, '..', 'ssl', 'service.cert')),
            ssl_keyfile=os.path.abspath(os.path.join(CURRENT_PATH, '..', 'ssl', 'service.key')))
        logger.info("Connected to kafka.")

    def send(self, value: bytes) -> None:
        self.producer.send(self.topic, value=value).get(timeout=60)
        logger.info("Produced result to topic: {}.".format(self.topic))

    def close(self) -> None:
        self.producer.close()


class WebsiteChecker(object):
    def __init__(self,
                 producer: Producer,
                 check_interval_in_seconds: str = os.getenv("CHECK_INTERVAL_IN_SECONDS", "5"),
                 check_url: str = os.getenv("CHECK_URL", "https://www.example-url"),
                 check_regex: str = os.getenv("CHECK_REGEX")):
        self.check_interval_in_seconds = int(check_interval_in_seconds)
        self.check_url = check_url
        self.check_regex = check_regex
        self.producer = producer

    def check(self) -> Optional[WebsiteCheckResult]:
        """Check the website once and return the result we're interested in.

        Returns:
            Optional[WebsiteCheckResult]: Website check result, otherwise None if there's an error
        """

        try:
            response = requests.get(self.check_url)

            if self.check_regex is not None:
                is_regex_match = True if re.search(self.check_regex, response.text) else False
            else:
                is_regex_match = None

            return WebsiteCheckResult(
                response.status_code,
                response.elapsed.total_seconds(),
                response_data_regex=self.check_regex,
                is_regex_matched=is_regex_match
            )
        except requests.exceptions.RequestException as error:
            logger.error("Error raised {}.".format(error))
            return None

    def loop_checker(self) -> None:
        """Periodically conduct checking the website. Wait specified interval in between loops."""

        while True:
            try:
                result: Optional[WebsiteCheckResult] = self.check()
                if result is not None:
                    logger.info("Check result: {}.".format(result.result()))
                    self.producer.send(result.serialize())
                else:
                    logger.warning("TODO: Skipped sending data to kafka.")
            except Exception as error:
                logger.error("Unknown error: {}".format(error))
            finally:
                sleep(self.check_interval_in_seconds)

    def close(self) -> None:
        self.producer.close()


def main():
    website_checker = None
    try:
        website_checker = WebsiteChecker(Producer())
        website_checker.loop_checker()
    except KeyboardInterrupt:
        logger.info("Exiting...")
    finally:
        if website_checker:
            website_checker.close()


if __name__ == "__main__":
    main()
