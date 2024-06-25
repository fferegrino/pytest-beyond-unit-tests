import json

import psycopg2
import pytest
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from psycopg2 import OperationalError


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Override default location of docker-compose.yml file."""
    return pytestconfig.rootpath / "test-docker-compose.yml"


@pytest.fixture(scope="session")
def kafka_broker(docker_services, docker_ip):

    def check_kafka_responsive(server):

        try:
            producer = Producer({"bootstrap.servers": server})
            producer.list_topics(timeout=5)
            return True
        except Exception as e:
            print(e)
            return False

    port = docker_services.port_for("kafka", 9092)
    docker_services.wait_until_responsive(
        check=lambda: check_kafka_responsive(f"{docker_ip}:{port}"),
        timeout=30.0,
        pause=0.1,
    )

    # Check topics do not exist
    topics = ["raw.events", "enriched.events", "output.events"]
    admin_client = AdminClient({"bootstrap.servers": f"{docker_ip}:{port}"})

    existing_topics = admin_client.list_topics().topics.keys()
    for topic in topics:
        assert topic not in existing_topics

    # Create topics
    admin_client.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics])

    yield f"{docker_ip}:{port}"

    # Delete topics
    admin_client.delete_topics(topics)


@pytest.fixture(scope="session")
def db_uri(docker_services, docker_ip):
    user = "user"
    password = "password"
    dbname = "dbname"
    port = docker_services.port_for("db", 5432)

    def check_db_responsive(host, port, dbname, user, password):
        try:
            # Attempt to connect to the database
            conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
            conn.close()
            return True
        except OperationalError:
            return False

    docker_services.wait_until_responsive(
        check=lambda: check_db_responsive(docker_ip, port, dbname, user, password), timeout=30.0, pause=0.1
    )
    return f"postgresql://{user}:{password}@{docker_ip}:{port}/{dbname}"


@pytest.fixture
def setup_database(db_uri):
    import sqlalchemy
    from sqlalchemy import text

    engine = sqlalchemy.create_engine(db_uri)

    restaurant_features = [
        (1, 10, 30.0),
        (2, 20, 40.0),
        (3, 30, 50.0),
    ]

    with engine.connect() as connection:
        connection.execute(
            text(
                """
            CREATE TABLE restaurant_features (
                id INTEGER PRIMARY KEY,
                current_order_count INTEGER,
                average_delivery_time_30_mins FLOAT
            )
            """
            )
        )

        connection.execute(
            text(
                """
            INSERT INTO restaurant_features (id, current_order_count, average_delivery_time_30_mins)
            VALUES (:id, :current_order_count, :average_delivery_time_30_mins)
            """
            ),
            [
                {
                    "id": id,
                    "current_order_count": current_order_count,
                    "average_delivery_time_30_mins": average_delivery_time_30_mins,
                }
                for id, current_order_count, average_delivery_time_30_mins in restaurant_features
            ],
        )
        connection.commit()

    yield

    with engine.connect() as connection:
        connection.execute(text("DROP TABLE restaurant_features"))


def test_end_to_end(setup_database, kafka_broker):

    # Arrange
    import time

    from confluent_kafka import Consumer, Producer

    producer = Producer({"bootstrap.servers": kafka_broker})
    inference_consumer = Consumer(
        {"bootstrap.servers": kafka_broker, "group.id": f"test-group", "auto.offset.reset": "earliest"}
    )
    inference_consumer.subscribe(["output.events"])

    events_to_produce = [
        {"restaurant_id": 1, "timestamp": 1718902297},
        {"restaurant_id": 2, "timestamp": 1718902297},
        {"restaurant_id": 3, "timestamp": 1718902297},
    ]

    # Act
    for event in events_to_produce:
        producer.produce("raw.events", json.dumps(event).encode("utf-8"))
    producer.flush()

    # Assert

    timeout = 60
    start_time = time.time()
    received_events = []
    while time.time() < start_time + timeout:
        msg = inference_consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        message = msg.value().decode("utf-8")
        received_events.append(json.loads(message))

    assert len(received_events) == len(events_to_produce)

    for event in received_events:
        assert "current_order_count" in event
        assert "average_delivery_time_30_mins" in event
        assert "time_estimate" in event
