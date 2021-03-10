import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	
broker_address="broker.mqttdashboard.com"

client = mqtt.Client("Client1")

client.on_message=on_message

print("connecting to broker")

client.connect(broker_address)

client.loop_start()

client.subscribe("hydro/temp")

client.publish("hydro/temp", "21 Grad")

"""
client.subscribe("FH/test")

client.publish("FH/test", "xoxo")

client.subscribe("topic/fh/test")"""

time.sleep(4)

client.loop_stop()



