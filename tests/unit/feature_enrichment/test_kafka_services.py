from unittest.mock import MagicMock, patch

import pytest

from feature_enrichment.kafka_services import KafkaService


@pytest.fixture
def kafka_config():
    return {"bootstrap.servers": "localhost:9092"}


@pytest.fixture
def kafka_service(kafka_config):
    with patch("feature_enrichment.kafka_services.Consumer"), patch("feature_enrichment.kafka_services.Producer"):
        yield KafkaService(kafka_config, "input_topic", "output_topic")


@patch("feature_enrichment.kafka_services.Consumer")
@patch("feature_enrichment.kafka_services.Producer")
def test_kafka_service_init(mock_producer, mock_consumer, kafka_config):
    KafkaService(kafka_config, "input_topic", "output_topic")
    mock_consumer.assert_called_once_with(kafka_config)
    mock_producer.assert_called_once_with(kafka_config)


def test_poll_message(kafka_service):
    mock_message = MagicMock()
    mock_message.value.return_value = b'{"restaurant_id": 1}'
    mock_message.error.return_value = None
    kafka_service.consumer.poll.return_value = mock_message

    event = kafka_service.poll_message()

    assert event == {"restaurant_id": 1}


def test_produce_message(kafka_service):
    kafka_service.produce_message("message")
    kafka_service.producer.produce.assert_called_once()
