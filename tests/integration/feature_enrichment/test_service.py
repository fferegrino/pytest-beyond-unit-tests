from unittest.mock import MagicMock, patch

import pytest

from feature_enrichment.database import DatabaseService
from feature_enrichment.feature_enrichment_service import FeatureEnrichmentService
from feature_enrichment.kafka_services import KafkaService


@pytest.fixture
def setup_sqlite_db(tmp_path):
    import sqlite3

    db_path = f"{tmp_path}/test.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE restaurant_features (
            id INTEGER PRIMARY KEY,
            current_order_count INTEGER,
            average_delivery_time_30_mins FLOAT
        )
    """
    )

    conn.commit()

    cursor.execute(
        """
        INSERT INTO restaurant_features (id, current_order_count, average_delivery_time_30_mins)
        VALUES
            (1, 10, 30.0),
            (2, 5, 20.0),
            (3, 15, 40.0)
    """
    )

    conn.commit()

    yield f"sqlite:///{db_path}"

    cursor.execute("DROP TABLE restaurant_features")
    conn.close()


@pytest.fixture
def mock_kafka_service():
    with patch("feature_enrichment.kafka_services.Consumer"), patch("feature_enrichment.kafka_services.Producer"):

        kafka_service = KafkaService({"bootstrap.servers": "localhost:9092"}, "input_topic", "output_topic")

        mock_message = MagicMock()
        mock_message.value.return_value = b'{"restaurant_id": 1}'
        mock_message.error.return_value = None
        kafka_service.consumer.poll.side_effect = [mock_message, KeyboardInterrupt]

        yield kafka_service


def test_kafka_service_runs(setup_sqlite_db, mock_kafka_service):

    database_service = DatabaseService(setup_sqlite_db)
    feature_enrichment_service = FeatureEnrichmentService(mock_kafka_service, database_service)

    with pytest.raises(KeyboardInterrupt):
        feature_enrichment_service.run()

    assert mock_kafka_service.consumer.subscribe.called
    mock_kafka_service.producer.produce.assert_called_once_with(
        "output_topic", b'{"restaurant_id": 1, "current_order_count": 10, "average_delivery_time_30_mins": 30.0}'
    )
