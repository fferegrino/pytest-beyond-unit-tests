import os


def get_kafka_config():
    return {
        "bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVER"],
        "group.id": "feature-enrichment",
        "auto.offset.reset": "earliest",
    }


def get_db_uri():
    return os.environ["DB_URI"]
