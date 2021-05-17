## Installation
```bash
pip3 install git+https://github.com/yifeizuo/website_checker.git
```

## Run website checker <produce/consume>
### producer
```bash
KAFKA_BOOTSTRAP_SERVERS="kafka-348471e1-yifeizuo-4f83.aivencloud.com:23924" \
  KAFKA_TOPIC="remote_topic" \
  CHECK_INTERVAL_IN_SECONDS=1 \
  CHECK_URL=https://afun.fi \
  python3 -m website_checker produce
```

### consumer
```bash
KAFKA_BOOTSTRAP_SERVERS="kafka-348471e1-yifeizuo-4f83.aivencloud.com:23924" \
  KAFKA_TOPIC="remote_topic" \
  DB_HOST="pg-2c97f07-yifeizuo-4f83.aivencloud.com" \
  DB_PORT=23922 \
  DB_USER="avnadmin" \
  DB_PASSWORD="xfozw58iztfczvsx" \
  DB_NAME=defaultdb \
  python3 -m website_checker consume
```

### Attribution:
- https://docs.github.com/en/actions/guides/building-and-testing-python
- https://docs.docker.com/compose/
- https://github.com/bitnami/bitnami-docker-kafka
- https://help.aiven.io/en/articles/489572-getting-started-with-aiven-for-apache-kafka
- https://www.confluent.io/blog/kafka-listeners-explained/
- https://github.com/dpkp/kafka-python
- https://github.com/psf/requests
- https://pipxproject.github.io/pipx/how-pipx-works/#developing-for-pipx

### TODO:
- [x] Linting
   - [x] flake8 
- [x] Test +  Coverage
   - [x] Not 100% coverage, add 1 test for producer.py as an example
   - [ ] Improve coverage
- [x] Docstring
- [x] Github Actions enabled **CI/CD pipine**
- [x] Packaging 
- [X] README
- [X] Aiven credential
   - [x] credentials to connect Aiven Kafka and PostgreSQL service are vaulted using github repository variables 
   - [ ] Apply the credentials CI/CD pipeline
   - [ ] SSL cert file valut
- [ ] Docker SSL Config
   - [x] Docker setup works with first commit in this repo, without SSL

## Run from source (with additional configs explained)
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
