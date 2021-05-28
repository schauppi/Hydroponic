from AtlasI2C import (AtlasI2C)
import time
import ph_ec_helper
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import ultrasonic_helper
import dht11_helper

GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern
RELAIS_lamp = 24 #Lampe
RELAIS_water_pump = 18 #Wasserpumpe
RELAIS_air_pump = 23 #Luftpumpe

RELAIS_dosing_pump_4 = 21 #Dosierpumpe4(innen)
RELAIS_dosing_pump_3 = 20 #Dosierpumpe3
RELAIS_dosing_pump_2 = 26 #Dosierpumpe2
RELAIS_dosing_pump_1 = 19 #Dosierpumpe1(aussen)

GPIO.setup(RELAIS_lamp, GPIO.OUT) # GPIO Modus zuweisen
GPIO.setup(RELAIS_water_pump, GPIO.OUT) # GPIO Modus zuweisen
GPIO.setup(RELAIS_air_pump, GPIO.OUT) # GPIO Modus zuweisen
GPIO.setup(RELAIS_dosing_pump_4, GPIO.OUT) # GPIO Modus zuweisen
GPIO.setup(RELAIS_dosing_pump_3, GPIO.OUT) # GPIO Modus zuweisen
GPIO.setup(RELAIS_dosing_pump_2, GPIO.OUT) # GPIO Modus zuweisen
GPIO.setup(RELAIS_dosing_pump_1, GPIO.OUT) # GPIO Modus zuweisen

#init when program opens
GPIO.output(RELAIS_lamp, True)
GPIO.output(RELAIS_water_pump, True)
GPIO.output(RELAIS_air_pump, True)

GPIO.output(RELAIS_dosing_pump_1, True)
GPIO.output(RELAIS_dosing_pump_2, True)
GPIO.output(RELAIS_dosing_pump_3, True)
GPIO.output(RELAIS_dosing_pump_4, True)

def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("connection ok", rc)
	else:
		print("connection error", rc)

def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))

	if message.topic == "hydro/lamp":
		print("topic lamp")
		if message.payload == "true":
			GPIO.output(RELAIS_lamp, True)
		elif message.payload == "false":
			GPIO.output(RELAIS_lamp, False)
		
	elif message.topic == "hydro/water_pump":
		print("topic water pump")
		if message.payload == "true":
			GPIO.output(RELAIS_water_pump, True)
		elif message.payload == "false":
			GPIO.output(RELAIS_water_pump, False)

	elif message.topic == "hydro/air_pump":
		print("topic air pump")
		if message.payload == "true":
			GPIO.output(RELAIS_air_pump, True)
		elif message.payload == "false":
			GPIO.output(RELAIS_air_pump, False)
			
	elif message.topic == "hydro/dosing_pump_1":
		print("dosing pump 1")
		if message.payload == "true":
			GPIO.output(RELAIS_dosing_pump_1, False)
		elif message.payload == "false":
			GPIO.output(RELAIS_dosing_pump_1, True)
			
	elif message.topic == "hydro/dosing_pump_2":
		print("dosing pump 2")
		if message.payload == "true":
			GPIO.output(RELAIS_dosing_pump_2, False)
		elif message.payload == "false":
			GPIO.output(RELAIS_dosing_pump_2, True)

	elif message.topic == "hydro/dosing_pump_3":
		print("dosing pump 3")
		if message.payload == "true":
			GPIO.output(RELAIS_dosing_pump_3, False)
		elif message.payload == "false":
			GPIO.output(RELAIS_dosing_pump_3, True)
			
	elif message.topic == "hydro/dosing_pump_4":
		print("dosing pump 4")
		if message.payload == "true":
			GPIO.output(RELAIS_dosing_pump_4, False)
		elif message.payload == "false":
			GPIO.output(RELAIS_dosing_pump_4, True)
			
			
#Mqtt Standard procedure
broker_address = "192.168.8.166"
client = mqtt.Client("Actuators")
client.on_connect=on_connect
client.on_message=on_message
client.connect(broker_address)
client.loop_start()

client.subscribe("hydro/air_pump")
client.subscribe("hydro/lamp")
client.subscribe("hydro/water_pump")
client.subscribe("hydro/dosing_pump_1")
client.subscribe("hydro/dosing_pump_2")
client.subscribe("hydro/dosing_pump_3")
client.subscribe("hydro/dosing_pump_4")

while True:
	
	if GPIO.input(RELAIS_lamp) == 1:
		client.publish("hydro/lamp_status", 1)
	else:
		client.publish("hydro/lamp_status", 0)
	
	if GPIO.input(RELAIS_air_pump) == 1:
		client.publish("hydro/air_pump_status", 1)
	else:
		client.publish("hydro/air_pump_status", 0)
		
	if GPIO.input(RELAIS_water_pump) == 1:
		client.publish("hydro/water_pump_status", 1)
	else:
		client.publish("hydro/water_pump_status", 0)
		
	time.sleep(60)

