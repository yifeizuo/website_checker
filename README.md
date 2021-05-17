### producer.py

```bash
# optionally you can set env var: CHECK_REGEX="A fun company"
KAFKA_BOOTSTRAP_SERVERS="kafka-348471e1-yifeizuo-4f83.aivencloud.com:23924" KAFKA_TOPIC="remote_topic" CHECK_INTERVAL_IN_SECONDS=1 CHECK_URL=https://afun.fi python website_checker/producer.py
```

### consumer.py

```bash
# optionally env var AGGREGATE_DATA_AS_HOURLY can be set to True to improve DB performance while storing less data 
KAFKA_BOOTSTRAP_SERVERS="kafka-348471e1-yifeizuo-4f83.aivencloud.com:23924" KAFKA_TOPIC="remote_topic" DB_HOST="pg-2c97f07-yifeizuo-4f83.aivencloud.com" DB_PORT=23922 DB_USER="avnadmin" DB_PASSWORD="xfozw58iztfczvsx" DB_NAME=defaultdb AGGREGATE_DATA_AS_HOURLY=FALSE python website_checker/consumer.py
```

### Attribution:
- https://docs.github.com/en/actions/guides/building-and-testing-python
- https://docs.docker.com/compose/
- https://github.com/bitnami/bitnami-docker-kafka
- https://help.aiven.io/en/articles/489572-getting-started-with-aiven-for-apache-kafka
- https://www.confluent.io/blog/kafka-listeners-explained/
- https://github.com/dpkp/kafka-python

### TODO:
- [x] Linting
- [ ] Test +  Coverage
   - Not 100% coverage, add 1 test for producer.py as an example
- [x] Docstring
- [x] Github Actions
- [ ] Packaging 
- [X] README
- [X] Aiven credential
   - credentials to connect Aiven Kafka and PostgreSQL service are vaulted using github repository variables 


