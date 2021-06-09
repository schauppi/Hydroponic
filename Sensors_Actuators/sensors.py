from AtlasI2C import (AtlasI2C)
import time
import ph_ec_helper
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import ultrasonic_helper
import dht11_helper
import webcam_helper
import schedule
from simple_pid import PID
import fertilizer_helper
import display_1_helper
import display_2_helper

time_global = 0
time_global_after = 0

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
	
	if message.topic == "hydro/fertilize":
		#client.publish("hydro/fertilize/telegram", "Fertilizing...")
		#water_level = ultrasonic_helper.distance()
		water_level = 30
		time_dosing_pump_3, time_dosing_pump_4 = fertilizer_helper.fertilize(water_level)
		payload = str(time_dosing_pump_3) + "," + str(time_dosing_pump_4)
		print(payload)
		client.publish("hydro/fertilize/actuators", payload)
	else:
		pass
		
#Mqtt Standard procedure
broker_address = "192.168.8.190"
client = mqtt.Client("Sensors")
client.on_connect=on_connect
client.on_message=on_message
client.connect(broker_address)
client.loop_start()

client.subscribe("hydro/fertilize")


#controller
pid = PID(1, 0, 0, setpoint=5.7)
#pid_2 = PID(1.1, 0.1, 0, setpoint=5.7)


def controller():
	control_value = pid(ph)
	if control_value > 0.5:
		#print("ph value too low")
		client.publish("hydro/ph/telegram", "PH value too low")
		if control_value >= 0.5 and control_value <= 0.6:
			client.publish("hydro/dosing_pump_2", "true")
			time.sleep(4)
			client.publish("hydro/dosing_pump_2", "false")
		elif control_value >= 0.6 and control_value <= 0.9:
			client.publish("hydro/dosing_pump_2", "true")
			time.sleep(11)
			client.publish("hydro/dosing_pump_2","false")
		elif control_value >=1 and control_value <= 1.5:
			client.publish("hydro/dosing_pump_2", "true")
			time.sleep(18)
			client.publish("hydro/dosing_pump_2", "false")
		elif control_value >=1.5 and control_value <= 2:
			client.publish("hydro/dosing_pump_2", "true")
			time.sleep(24)
			client.publish("hydro/dosing_pump_2", "false")
		elif control_value >=2 and control_value <= 2.5:
			client.publish("hydro/dosing_pump_2", "true")
			time.sleep(36)
			client.publish("hydro/dosing_pump_2", "false")
		elif control_value >=2.5:
			client.publish("hydro/dosing_pump_2", "true")
			time.sleep(44)
			client.publish("hydro/dosing_pump_2", "false")
	if control_value < -0.5:
		print("ph value too high")
		client.publish("hydro/ph/telegram", "PH value too high")
		if control_value <= -0.5 and control_value >= -0.6:
			client.publish("hydro/dosing_pump_1", "true")
			time.sleep(5)
			client.publish("hydro/dosing_pump_1", "false")
		elif control_value <= -0.6 and control_value >= -0.9:
			client.publish("hydro/dosing_pump_1", "true")
			time.sleep(16)
			client.publish("hydro/dosing_pump_1", "false")
		elif control_value <= -1 and control_value >= -1.5:
			client.publish("hydro/dosing_pump_1", "true")
			time.sleep(25)
			client.publish("hydro/dosing_pump_1", "false")
		elif control_value <= -1.5 and control_value >= -2:
			client.publish("hydro/dosing_pump_1", "true")
			time.sleep(34)
			client.publish("hydro/dosing_pump_1", "false")
		elif control_value <= -2 and control_value >= -2.5:
			client.publish("hydro/dosing_pump_1", "true")
			time.sleep(50)
			client.publish("hydro/dosing_pump_1", "false")
		elif control_value<= -2.5:
			client.publish("hydro/dosing_pump_1", "true")
			time.sleep(63)
			client.publish("hydro/dosing_pump_1", "false")
	print(control_value)
	
#schedule.every(50).minutes.do(controller)

while True:
	#measure ph and ec from ph_ec_helper module
	ph, ec = ph_ec_helper.measure(device_list)
	#water_level = ultrasonic_helper.distance()
	water_level = 30
	humidity, temperature = dht11_helper.measure()
	webcam_image = webcam_helper.webcam()
	
	#publish the values on topics
	client.publish("hydro/ph", ph)
	client.publish("hydro/ec", ec)
	client.publish("hydro/water_level", water_level)
	client.publish("hydro/temperature", temperature)
	client.publish("hydro/humidity", humidity)
	
	webcam_image=open("image.png", "rb") #3.7kiB in same folder
	fileContent = webcam_image.read()
	byteArr = bytearray(fileContent)
	client.publish("hydro/webcam", byteArr)
	
	print("ph:", ph)
	print("ec:", ec)
	
	display_1_helper.display_1(ec, ph)
	
	#control_value2 = pid_2(ph)
	#print(control_value2)
	
	#schedule.run_pending()
	time.sleep(60)
