import json

from kafka import KafkaConsumer
from json import loads
from time import sleep
# import app

consumer = KafkaConsumer(
    'connect-custom',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
print("kafa stream processor started")
for event in consumer:
    print(event)
    event_data = event.value
    # Do whatever you want
    print(event_data)
    # app.update_bin_status(json.dumps(event_data))
    sleep(2)