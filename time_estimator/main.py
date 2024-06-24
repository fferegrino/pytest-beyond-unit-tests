import json
import os

from confluent_kafka import Consumer, Producer

consumer = Consumer(
    {
        "bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVER"],
        "group.id": "time-estimator",
        "auto.offset.reset": "earliest",
    }
)

producer = Producer({"bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVER"]})


consumer.subscribe(["enriched.events"])

print("Time estimator service started")

while True:
    message = consumer.poll(1.0)

    if message is None:
        continue
    if message.error():
        print("Consumer error: {}".format(message.error()))
        continue

    event = json.loads(message.value().decode("utf-8"))

    # {'restaurant_id': 1, 'timestamp': 1718902297, 'current_order_count': 10, 'average_delivery_time_30_mins': 30.0}

    # Calculate the score
    event["time_estimate"] = (event["current_order_count"] * event["average_delivery_time_30_mins"] * 0.1) + event[
        "average_delivery_time_30_mins"
    ]

    producer.produce("output.events", json.dumps(event).encode("utf-8"))

    consumer.commit()
