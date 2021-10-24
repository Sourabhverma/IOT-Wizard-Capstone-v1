from kafka import KafkaConsumer
from json import loads
from time import sleep
consumer = KafkaConsumer(
    'baeldung',
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
print("started")
for event in consumer:
    print(event)
    event_data = event.value
    # Do whatever you want
    print(event_data)
    sleep(2)