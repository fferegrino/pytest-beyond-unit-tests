import json

from confluent_kafka import Consumer, Producer


class KafkaService:
    def __init__(self, kafka_config, input_topic, output_topic):
        self.consumer = Consumer(kafka_config)
        self.producer = Producer(kafka_config)
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.consumer.subscribe([self.input_topic])

    def poll_message(self):
        message = self.consumer.poll(1.0)
        if message is None or message.error():
            return None
        event = json.loads(message.value().decode("utf-8"))
        return event

    def produce_message(self, message):
        self.producer.produce(self.output_topic, message.encode("utf-8"))
        self.producer.flush()

    def commit(self):
        self.consumer.commit()
