import os

from feature_enrichment.database import DatabaseService
from feature_enrichment.feature_enrichment_service import FeatureEnrichmentService
from feature_enrichment.kafka_services import KafkaService

if __name__ == "__main__":
    db_uri = os.environ["DB_URI"]

    kafka_config = {
        "bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVER"],
        "group.id": "feature-enrichment",
        "auto.offset.reset": "earliest",
    }

    kafka_service = KafkaService(kafka_config, "raw.events", "enriched.events")
    db_service = DatabaseService(db_uri=db_uri)
    feature_enrichment_service = FeatureEnrichmentService(kafka_service, db_service)
    feature_enrichment_service.run()
