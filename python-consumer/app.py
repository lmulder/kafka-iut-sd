from kafka import KafkaConsumer
import json

# Define the Kafka broker and topic
broker = '{RPI_IP}}:9092'
topic = 'my-first-topic'

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[broker],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"Listening to topic {topic}")

# Poll messages from the Kafka topic
for message in consumer:
    print(f"Received message: {message.value}")