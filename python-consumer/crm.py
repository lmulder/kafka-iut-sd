from kafka import KafkaConsumer
import json
import mysql.connector
import uuid
import time

# Define the Kafka broker and topic
broker = 'my-kafka.{user-dev}.svc.cluster.local:9092'
topic = 'dbserver1.inventory.customers'

# Definie the database connection parameters
db_host = 'mariadb.{user-dev}.svc.cluster.local'
db_port = 3306
db_user = 'mysqluser'
db_password = 'changeme'
db_name = 'crm'

# Create a Kafka consumer
try:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[broker],
        sasl_mechanism='SCRAM-SHA-256',
        security_protocol='SASL_PLAINTEXT',
        sasl_plain_username='user1',
        sasl_plain_password='changeme',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='crm'
    )
    print(f"Connected to Kafka broker at {broker}")
    print(f"Listening to topic {topic}")
except Exception as e:
    print(f"Error connecting to Kafka broker: {e}")
    exit(1)

print(f"Connection to DB server at {db_host}:{db_port}")
# connect to a MySQL/MariaDB database
try:
    conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )
    print("Connected to MariaDB database")
except mysql.connector.Error as e:
    print(f"Error connecting to MariaDB database: {e}")
    exit(1)

# Poll messages from the Kafka topic
while True:
    for message in consumer:
        print(f"Received message: {message.value}")
        # Process the JSON message. First we will look at the key payload.before and payload.after
        data = json.loads(message.value)
        before = data.get('payload', {}).get('before')
        after = data.get('payload', {}).get('after')
        cursor = conn.cursor()
        # If before is null, it means a new record was created
        if before is None:
            print(f"New record created: {after}")
            # insert the new record into the database. id is uuid, source_id is the same as id, first_name, last_name and email are also in the after payload
            cursor.execute(
                "INSERT INTO customers (id, source_id, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)",
                (str(uuid.uuid4()), after['id'], after['first_name'], after['last_name'], after['email'])
            )
        # If after is null, it means a record was deleted
        elif after is None:
            print(f"Record deleted: {before}")
            # delete the record in the database by source_id
            cursor.execute("DELETE FROM customers WHERE source_id = %s", (before['id'],))
        # If both before and after are not null, it means a record was updated
        else:
            print(f"Record updated from {before} to {after}")
            # update the record in the database by source_id
            cursor.execute(
                "UPDATE customers SET first_name = %s, last_name = %s, email = %s WHERE source_id = %s",
                (after['first_name'], after['last_name'], after['email'], after['id'])
            )
        conn.commit()
    # wait for a short period before polling for new messages
    time.sleep(1)