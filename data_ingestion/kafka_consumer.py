from kafka import KafkaProducer
import json
import time
import random

KAFKA_TOPIC = "real_time_data"
KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_data():
    return {
        "timestamp": time.time(),
        "sensor_id": random.randint(1, 100),
        "value": round(random.uniform(20.0, 100.0), 2)
    }

if __name__ == "__main__":
    while True:
        data = generate_data()
        producer.send(KAFKA_TOPIC, data)
        print(f"Produced: {data}")
        time.sleep(2)

