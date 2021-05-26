from AtlasI2C import (AtlasI2C)
import time
import ph_ec_helper
import paho.mqtt.client as mqtt
import time
import schedule
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

button_lamp = 5 #Button Lampe

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

#setup buttons
GPIO.setup(button_lamp, GPIO.IN, GPIO.PUD_UP)
		
#Callback togglen
def lamp_interrupt(channel):
	print("pressed")
	print(channel)
	
GPIO.add_event_detect(button_lamp, GPIO.RISING, callback=lamp_interrupt, bouncetime = 250)

GPIO.remove_event_detect(RELAIS_lamp)
GPIO.remove_event_detect(RELAIS_water_pump)
GPIO.remove_event_detect(RELAIS_air_pump)


def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("connection ok", rc)
	else:
		print("connection error", rc)

		
def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	topic = str(message.topic)
	#message = str(message.payload.decode("utf-8"))
	#print(len(message.payload))
	#print(topic)
	#global topic

	if message.topic == "hydro/lamp/on":
		GPIO.output(RELAIS_lamp, True)
	elif message.topic == "hydro/lamp/off":
		GPIO.output(RELAIS_lamp, False)
		
	elif message.topic == "hydro/water_pump/on":
		GPIO.output(RELAIS_water_pump, True)
	elif message.topic == "hydro/water_pump/off":
		GPIO.output(RELAIS_water_pump, False)
		
	elif message.topic == "hydro/air_pump/on":
		GPIO.output(RELAIS_air_pump, True)
	elif message.topic == "hydro/air_pump/off":
		GPIO.output(RELAIS_air_pump, False)

	
	#dosing pumps
	elif message.topic == "hydro/dosing_pump_1/on":
		GPIO.output(RELAIS_dosing_pump_1, False)
	elif message.topic == "hydro/dosing_pump_1/off":
		GPIO.output(RELAIS_dosing_pump_1, True)
		
	elif message.topic == "hydro/dosing_pump_2/on":
		GPIO.output(RELAIS_dosing_pump_2, False)
	elif message.topic == "hydro/dosing_pump_2/off":
		GPIO.output(RELAIS_dosing_pump_2, True)
		
	elif message.topic == "hydro/dosing_pump_3/on":
		GPIO.output(RELAIS_dosing_pump_3, False)
	elif message.topic == "hydro/dosing_pump_3/off":
		GPIO.output(RELAIS_dosing_pump_3, True)
		
	elif message.topic == "hydro/dosing_pump_4/on":
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
client.subscribe("hydro/lamp/hardware_button/on")
client.subscribe("hydro/lamp/hardware_button/off")
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


def lamp_timer():
	if GPIO.input(RELAIS_lamp) == 1:
		client.publish("hydro/lamp/off")
	else:
		client.publish("hydro/lamp/on")
		
schedule.every(12).hours.do(lamp_timer)

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
		
	schedule.run_pending()
	time.sleep(60)
	

