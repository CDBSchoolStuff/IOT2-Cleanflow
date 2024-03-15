# Complete project details at https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

# https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/
# https://pimylifeup.com/raspberry-pi-mosquitto-mqtt-server/

# RaspberryPi Mosquitto Command:
# mosquitto_sub -d -h localhost -t mqtt_data

import ubinascii
import machine, time
from umqttsimple import MQTTClient
from credentials import credentials

mqtt_server = credentials['mqtt_server']
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'mqtt_data'
topic_pub = b'mqtt_data'

last_message = 0
message_interval = 5
counter = 0

client = MQTTClient(client_id, mqtt_server)

#########################################################################
# FUNCTIONS

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')

def connect_and_subscribe():
    #global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


def run_once():
    try:
        client = connect_and_subscribe()
    except OSError as e:
        restart_and_reconnect()
      
def send_message(msg, topic):
    try:
        #client = connect_and_subscribe()
        client.publish(topic, msg)
        print(f"[MQTT] Topic: {topic} | Message: {msg}")
    except OSError as e:
        restart_and_reconnect()