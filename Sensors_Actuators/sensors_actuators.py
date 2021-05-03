from AtlasI2C import (AtlasI2C)
import time
import ph_ec_helper
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import ultrasonic_helper
import dht11_helper

#get i2c devices from ph_ec_helper module
#ph 0x63 / 99 i2c
#ec 0x64 / 100 i2c
device_list = ph_ec_helper.get_devices()
device = device_list

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
	
	#lamp, air/water pump
	if message.topic == "hydro/lamp/on":
		GPIO.output(RELAIS_lamp, True)
	elif message.topic == "hydro/lamp/off":
		GPIO.output(RELAIS_lamp, False)
		
	if message.topic == "hydro/water_pump/on":
		GPIO.output(RELAIS_water_pump, True)
	elif message.topic == "hydro/water_pump/off":
		GPIO.output(RELAIS_water_pump, False)
		
	if message.topic == "hydro/air_pump/on":
		GPIO.output(RELAIS_air_pump, True)
	elif message.topic == "hydro/air_pump/off":
		GPIO.output(RELAIS_air_pump, False)
		
	#dosing pumps
	if message.topic == "hydro/dosing_pump_1/on":
		GPIO.output(RELAIS_dosing_pump_1, False)
	elif message.topic == "hydro/dosing_pump_1/off":
		GPIO.output(RELAIS_dosing_pump_1, True)
		
	if message.topic == "hydro/dosing_pump_2/on":
		GPIO.output(RELAIS_dosing_pump_2, False)
	elif message.topic == "hydro/dosing_pump_2/off":
		GPIO.output(RELAIS_dosing_pump_2, True)
		
	if message.topic == "hydro/dosing_pump_3/on":
		GPIO.output(RELAIS_dosing_pump_3, False)
	elif message.topic == "hydro/dosing_pump_3/off":
		GPIO.output(RELAIS_dosing_pump_3, True)
		
	if message.topic == "hydro/dosing_pump_4/on":
		GPIO.output(RELAIS_dosing_pump_4, False)
	elif message.topic == "hydro/dosing_pump_4/off":
		GPIO.output(RELAIS_dosing_pump_4, True)

#Mqtt Standard procedure
broker_address = "192.168.8.166"
client = mqtt.Client("Sensors_Actuators")
client.on_connect=on_connect
client.on_message=on_message
client.connect(broker_address)
client.loop_start()

#topic subscriptions
client.subscribe("hydro/lamp/on")
client.subscribe("hydro/lamp/off")
client.subscribe("hydro/water_pump/on")
client.subscribe("hydro/water_pump/off")
client.subscribe("hydro/air_pump/on")
client.subscribe("hydro/air_pump/off")
client.subscribe("hydro/dosing_pump_1/on")
client.subscribe("hydro/dosing_pump_1/off")
client.subscribe("hydro/dosing_pump_2/on")
client.subscribe("hydro/dosing_pump_2/off")
client.subscribe("hydro/dosing_pump_3/on")
client.subscribe("hydro/dosing_pump_3/off")
client.subscribe("hydro/dosing_pump_4/on")
client.subscribe("hydro/dosing_pump_4/off")

while True:
	#measure ph and ec from ph_ec_helper module
	ph, ec = ph_ec_helper.measure(device_list)
	water_level = ultrasonic_helper.distance()
	humidity, temperature = dht11_helper.measure()
	
	#publish the values on topics
	client.publish("hydro/ph", ph)
	client.publish("hydro/ec", ec)
	client.publish("hydro/water_level", water_level)
	client.publish("hydro/temperature", temperature)
	client.publish("hydro/humidity", humidity)
	time.sleep(60)
	
