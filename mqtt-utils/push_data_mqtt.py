from paho.mqtt import client as mqtt_client
import json
from datetime import datetime
import random
import time

# Define Variables
broker = '127.0.0.1'
port = 1883
topic = "baeldung"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
cities = ["pune-1", "bangalore-1", "pune-2", "bangalore-2", "bangalore-3"]
binStatus = ["full", "empty", "half", "quarter", "three-quarter"]

latitude_list = [30.3358376, 30.307977, 30.3216419, 30.3427904,
                 30.378598, 30.3548185, 30.3345816, 30.387299,
                 30.3272198, 30.3840597, 30.4158, 30.340426,
                 30.3984348, 30.3431313, 30.273471]

longitude_list = [77.8701919, 78.048457, 78.0413095, 77.886958,
                  77.825396, 77.8460573, 78.0537813, 78.090614,
                  78.0355272, 77.9311923, 77.9663, 77.952092,
                  78.0747887, 77.9555512, 77.9997158]



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def publish(client):
    for j in range(10):
        time.sleep(1)
        print("Iteration", j)
        msg = {"datetime": datetime.now().strftime("%d:%m:%Y-%H:%M:%S"),
                    "bin_id": j,
                    "status": random.choice(binStatus),
                    "region": random.choice(cities),
                    "gelocation": [random.choice(latitude_list), random.choice(longitude_list)]}

        m= "{\"id\":1234,\"message\":\"This is a test\"}"
        result = client.publish(topic, json.dumps(str(m)))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()