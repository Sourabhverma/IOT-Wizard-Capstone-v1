import json

from paho.mqtt import client as mqtt_client
import json
from datetime import datetime
import random
import time

# Define Variables
broker = '54.82.70.158'
port = 1883
topic = "mqtt-Iot"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
cities = ["pune-1", "bangalore-1", "pune-2", "bangalore-2", "bangalore-3"]
binStatus = ["full", "empty", "half", "quarter", "three-quarter"]


# pune = { "pune_baner" :[18.570833868305556, 73.77448819855145],"pune_pancard" : [18.561069600862393, 73.7838009534555],
#          "pune_balewadi": [18.566602470640955, 73.78599005770796]}
#
# bangalore = {"bangalore_marathali":[12.966863323570541, 77.70265004750561],"bangalore_hall_airport":[12.950176604086646, 77.68076224631193],
#             "bangalore_ferncity": [12.975674797436094, 77.6978237520109]}

region_to_loc = [{"bin_id": "101", "region": "pune", "location": [18.570833868305556, 73.77448819855145]},
                       {"bin_id": "102", "region": "pune", "location": [18.561069600862393, 73.7838009534555]},
                       {"bin_id": "103", "region": "pune", "location": [18.566602470640955, 73.78599005770796]},
                       {"bin_id": "104", "region": "bangalore", "location": [12.966863323570541, 77.70265004750561]},
                       {"bin_id": "105", "region": "bangalore", "location": [12.950176604086646, 77.68076224631193]},
                       {"bin_id": "106", "region": "bangalore", "location": [12.975674797436094, 77.6978237520109]}
                       ]


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


def simulated_publish(client):
    for j in range(1,10):
        time.sleep(1)
        print("Iteration", j)

        # msg = {"datetime": str(datetime.now().strftime("%d:%m:%Y-%H:%M:%S")),
        #        "bin_id": str(j),
        #        "status": str(random.choice(binStatus)),
        #        "region": str(random.choice(cities)),
        #        "gelocation": [str(random.choice(latitude_list)), str(random.choice(longitude_list))]}

        city = random.choice(region_to_loc)
        msg = {"datetime": str(datetime.now().strftime("%d:%m:%Y-%H:%M:%S")),
               "bin_id": str(city.get("bin_id")),
               "status": str(random.choice(binStatus)),
               "region": str(city.get("region")),
               "gelocation": [str(city.get("location")[0]), str(city.get("location")[1])]}

        msg.update({'_id': "{}-{}".format(msg.get("bin_id"), msg.get("datetime"))})
        result = client.publish(topic,json.dumps(msg))

        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


# def data_publish(client):
#     '''
#     Set Data as per below format
#     Populate msg object as below
#     :param client:
#
#     binStatus = ["full", "empty", "half", "quarter", "three-quarter"]
#     :return:
#     '''
#
#     msg = {"datetime": str(datetime.now().strftime("%d:%m:%Y-%H:%M:%S")),
#            "bin_id": str(101),
#            "status": str(binStatus),
#            "region": str(city_code),
#            "gelocation": [str(latitude), str(longitude)]}
#
#     msg.update({'_id': "{}-{}".format(msg.get("bin_id"), msg.get("datetime"))})
#     result = client.publish(topic, json.dumps(msg))
#
#     status = result[0]
#     if status == 0:
#         print(f"Send `{msg}` to topic `{topic}`")
#     else:
#         print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    simulated_publish(client)
    # data_publish(client)


if __name__ == '__main__':
    run()