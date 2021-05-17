### producer.py

```bash
export KAFKA_BOOTSTRAP_SERVERS="example-host:1234"
export KAFKA_TOPIC="example-topic"
export CHECK_INTERVAL_IN_SECONDS=5
export CHECK_URL=https://afun.fi

python producer.py
```

### consumer.py

```bash
export KAFKA_BOOTSTRAP_SERVERS="example-host:1234"
export KAFKA_TOPIC="example-topic"
export DB_HOST="postgres"
export DB_PORT=5432
export DB_USER="my_user"
export DB_PASSWORD="securepassword"
export AGGREGATE_DATA_AS_HOURLY=FALSE

python consumer.py
```

### Attribution:
- https://docs.github.com/en/actions/guides/building-and-testing-python
- https://docs.docker.com/compose/
- https://github.com/bitnami/bitnami-docker-kafka
- https://help.aiven.io/en/articles/489572-getting-started-with-aiven-for-apache-kafka
- https://www.confluent.io/blog/kafka-listeners-explained/
- https://github.com/dpkp/kafka-python




TODO:
[x] Linting
[x] Test +  Coverage
   - Not 100% coverage, add 1 test for producer.py as an example
[x] Docstring
[] Github Actions
[] Packaging 
[] README
[] Aiven credential
