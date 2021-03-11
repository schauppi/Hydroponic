import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

broker_address="broker.mqttdashboard.com"

client = mqtt.Client("Client2")

client.on_message=on_message
client.on_connect=on_connect

client.connect(broker_address)

client.loop_start()

for i in range(3):

	client.publish("hydro/temp", "{} Grad".format(i))

	client.publish("hydro/ph", "{} ph".format(i))

	time.sleep(4)

client.loop_stop()




