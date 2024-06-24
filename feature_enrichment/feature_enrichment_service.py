import json

from feature_enrichment.database import DatabaseService
from feature_enrichment.kafka_services import KafkaService


class FeatureEnrichmentService:
    def __init__(self, kafka_service: KafkaService, db_service: DatabaseService):
        self.kafka_service = kafka_service
        self.db_service = db_service

    def run(self):
        print("Feature enrichment service started")
        while True:
            event = self.kafka_service.poll_message()
            if event is None:
                continue

            features = self.db_service.get_restaurant_features(event["restaurant_id"])
            if features is None:
                print(f"Restaurant with id {event['restaurant_id']} not found")
                continue

            event.update(
                {
                    "current_order_count": features["current_order_count"],
                    "average_delivery_time_30_mins": features["average_delivery_time_30_mins"],
                }
            )

            self.kafka_service.produce_message(json.dumps(event))
            self.kafka_service.commit()
