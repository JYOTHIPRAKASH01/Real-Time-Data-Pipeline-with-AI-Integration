from kafka import KafkaConsumer
import json

KAFKA_TOPIC = "real_time_data"
KAFKA_BROKER = "localhost:9092"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest"
)

if __name__ == "__main__":
    for message in consumer:
        data = message.value
        print(f"Consumed: {data}")
