import paho.mqtt.client as mqtt
import time

import RPi.GPIO as GPIO
import Adafruit_DHT

DHTSensor_1 = Adafruit_DHT.DHT11
DHTSensor_2 = Adafruit_DHT.DHT11

GPIO_1 = 16
GPIO_2 = 26
GPIO_3 = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_3, GPIO.OUT)

def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	
	if message.topic == "hydro/rel/on":
		GPIO.output(GPIO_3, True)
	elif message.topic == "hydro/rel/off":
		GPIO.output(GPIO_3, False)
    
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

client.subscribe("hydro/rel/off")
client.subscribe("hydro/rel/on")

while True:
	
	Hum1, Temp1 = Adafruit_DHT.read_retry(DHTSensor_1, GPIO_1)
	Hum2, Temp2 = Adafruit_DHT.read_retry(DHTSensor_2, GPIO_2)
	
	client.publish("hydro/temp/1",Temp1)
	client.publish("hydro/hum/1", Hum1)
	client.publish("hydro/temp/2",Temp2)
	client.publish("hydro/hum/2", Hum2)
	
	time.sleep(10)

client.loop_stop()
