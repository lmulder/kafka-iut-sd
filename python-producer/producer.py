from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

class KafkaMessageProducer:
    def __init__(self, bootstrap_servers, sasl_mechanism, security_protocol, sasl_plain_username, sasl_plain_password):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_plain_username,
            sasl_plain_password=sasl_plain_password,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        future = self.producer.send(topic, message)
        try:
            record_metadata = future.get(timeout=10)
            print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        except KafkaError as e:
            print(f"Failed to send message: {e}")

    def close(self):
        self.producer.close()

# Example usage:
producer = KafkaMessageProducer(
     bootstrap_servers='my-kafka.loic-mulder-dev.svc.cluster.local:9092',
     sasl_mechanism='SCRAM-SHA-256',
     security_protocol='SASL_PLAINTEXT',
     sasl_plain_username='user1',
     sasl_plain_password='Sp1KxdxyVX'
)
producer.send_message('my-first-topic', {'key': 'value'})
producer.close()