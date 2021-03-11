import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
	print("message received", str(message.payload.decode("utf-8")))
	
	
def on_subscribe(client, userdata, message, granted_qos):
	print(message)
	
broker_address="broker.mqttdashboard.com"

client = mqtt.Client("Client2")

client.on_message=on_message
client.on_subscribe=on_subscribe

print("connecting to broker")

client.connect(broker_address)

client.loop_start()

client.subscribe("hydro/temp",0)

time.sleep(4)

client.loop_stop()
