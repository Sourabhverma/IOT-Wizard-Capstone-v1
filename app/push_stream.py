from time import sleep
from json import dumps
from kafka import KafkaProducer
from datetime import datetime
import random

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)
cities = ["Pune-1","Bangalore-1","Pune-2","Bangalore-2","Bangalore-3"]
binStatus =["Full","Empty","half","Quarter","three-quarter"]

latitude_list = [30.3358376, 30.307977, 30.3216419, 30.3427904,
                 30.378598, 30.3548185, 30.3345816, 30.387299,
                 30.3272198, 30.3840597, 30.4158, 30.340426,
                 30.3984348, 30.3431313, 30.273471]

longitude_list = [77.8701919, 78.048457, 78.0413095, 77.886958,
                  77.825396, 77.8460573, 78.0537813, 78.090614,
                  78.0355272, 77.9311923, 77.9663, 77.952092,
                  78.0747887, 77.9555512, 77.9997158]

for j in range(100):
    print("Iteration", j)

    data = {"datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
     "bin_id": j,
     "status": random.choice(binStatus),
     "region": random.choice(cities),
     "gelocation": {random.choice(latitude_list),random.choice(longitude_list)}}

    print("data pushed to kafka {}".format(data))
    producer.send('topic_set_bin_status', value=str(data))
    sleep(0.5)