from kafka import KafkaProducer
from datetime import datetime
import time
import json

# Define the Kafka broker and topic
broker = 'kafka.loic-mulder-dev.svc.cluster.local:9092'
topic = 'partitionned'

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[broker],
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_PLAINTEXT',
    sasl_plain_username='user1',
    sasl_plain_password='VkEc1DVF03',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Infinite loop
i = 0
while True:
    # Define the message to send in a specific topic
    i+=1
    message = {
        'key': 'id',
        'value': i,
        'timestamp': time.time()
    }

    # Send the message to the Kafka topic
    producer.send(topic, value=message)

    # Ensure all messages are sent before closing the producer
    producer.flush()

    print(f"Message {i} sent to topic {topic}")

    time.sleep(5)