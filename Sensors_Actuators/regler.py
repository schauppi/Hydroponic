from AtlasI2C import (AtlasI2C)
import time
import ph_ec_helper
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import ultrasonic_helper
import dht11_helper
from simple_pid import PID

#get i2c devices from ph_ec_helper module
#ph 0x63 / 99 i2c
#ec 0x64 / 100 i2c
device_list = ph_ec_helper.get_devices()
device = device_list

GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern

button_lamp = 6 #Button Lampe
button_water_pump = 13 #Button Wasserpumpe
button_air_pump = 19 #Button Wasserpumpe

#setup buttons
GPIO.setup(button_lamp, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button_water_pump, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button_air_pump, GPIO.IN, GPIO.PUD_UP)

def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("connection ok", rc)
	else:
		print("connection error", rc)


def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))

def button_lamp_callback(channel):
	client.publish("hydro/lamp/on")
	print("lampe")
	
def button_water_pump_callback(channel):
	client.publish("hydro/water_pump/on")
	print("wasserpumpe")
	
def button_air_pump_callback(channel):
	client.publish("hydro/air_pump/on")
	print("luftpumpe")

GPIO.add_event_detect(button_water_pump, GPIO.RISING, callback=button_water_pump_callback, bouncetime = 250)
GPIO.add_event_detect(button_lamp, GPIO.RISING, callback=button_lamp_callback, bouncetime = 250)
GPIO.add_event_detect(button_air_pump, GPIO.RISING, callback=button_air_pump_callback, bouncetime = 250)


#Mqtt Standard procedure
broker_address = "192.168.8.166"
client = mqtt.Client("Sensors")
client.on_connect=on_connect
client.on_message=on_message
client.connect(broker_address)
client.loop_start()

#controller
pid = PID(1, 0, 0, setpoint=7.5)

while True:
	#measure ph and ec from ph_ec_helper module
	time_1 = time.time()
	ph, ec = ph_ec_helper.measure(device_list)
	print("PH: ", ph)
	time_2 = time.time()
	print("Elapsed: ", time_2 - time_1)
	water_level = ultrasonic_helper.distance()
	humidity, temperature = dht11_helper.measure()
	
	#publish the values on topics
	client.publish("hydro/ph", ph)
	client.publish("hydro/ec", ec)
	client.publish("hydro/water_level", water_level)
	client.publish("hydro/temperature", temperature)
	client.publish("hydro/humidity", humidity)
	
	control = pid(ph)
	print("control val: ", control)
	
