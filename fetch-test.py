import boto3
import hashlib
import json
import psycopg2
import argparse
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument("--buffer_size", required=True, help="number of user logins to process and insert to postgres at once.")
args = parser.parse_args()
buffer_size = args.buffer_size

def hash_sensitive_data(data):
    # Hash the data using SHA-256
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    return sha256.hexdigest()

def insert_user_logins(data):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
    conn.commit()
    cursor.close()
    conn.close()



if __name__ == "__main__":
    # Create an SQS client
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566/000000000000/login-queue', region_name='us-west', aws_access_key_id="ACCESS_ID",
            aws_secret_access_key= "ACCESS_KEY")

    queue_url = 'http://localhost:4566/000000000000/login-queue'

    # Receive a message from the queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages= int(buffer_size),
        MessageAttributeNames=[
            'All'
        ],
        WaitTimeSeconds=0
    )

    # Print the message body
    user_logins = []
    messages = response.get('Messages')
    for message in messages:
        user_info = json.loads(message['Body'])
        user_info["ip"] = hash_sensitive_data(user_info["ip"])
        user_info["device_id"] = hash_sensitive_data(user_info["device_id"])
        version = user_info["app_version"]
        parts = list(map(int, version.split('.')))
        result = 0
        for i, part in enumerate(parts):
            result += part * (10 ** (len(parts) - i - 1))
        user_info["app_version"] = result
        user_logins.append((user_info["user_id"], user_info["device_type"], user_info["ip"], user_info["device_id"], user_info["locale"], user_info["app_version"], date.today()))
    print(user_logins)
    insert_user_logins(user_logins)