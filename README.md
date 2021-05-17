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




TODO:
Linting
Test +  Coverage
Docstring
Github Actions
Packaging 
README
Aiven credential