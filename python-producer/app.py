from kafka import KafkaProducer
import json

# Define the Kafka broker and topic
broker = 'kafka.loic-mulder-dev.svc.cluster.local:9092'
topic = 'my-first-topic'

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[broker],
   sasl_mechanism='SCRAM-SHA-256',
     security_protocol='SASL_PLAINTEXT',
     sasl_plain_username='user1',
     sasl_plain_password='VkEc1DVF03',
     value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define the message to send in a specific topic
message = {
    'key': 'this-is-a-key',
    'value': 'this-is-a-value'
}

# Send the message to the Kafka topic
producer.send(topic, partition=0, value=message)

# Ensure all messages are sent before closing the producer
producer.flush()

print(f"Message sent to topic {topic}")