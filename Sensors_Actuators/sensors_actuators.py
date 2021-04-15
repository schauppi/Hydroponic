from AtlasI2C import (AtlasI2C)
import time
import ph_ec_helper
import paho.mqtt.client as mqtt

#get i2c devices from ph_ec_helper module
#ph 0x63 / 99 i2c
#ec 0x64 / 100 i2c
device_list = ph_ec_helper.get_devices()
device = device_list

def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("connection ok", rc)
	else:
		print("connection error", rc)

#Mqtt Standard procedure
broker_address = "192.168.8.166"
client = mqtt.Client("Sensors_Actuators")
client.on_connect=on_connect
client.connect(broker_address)
client.loop_start()
	

while True:
	#measure ph and ec from ph_ec_helper module
	ph, ec = ph_ec_helper.measure(device_list)
	
	#publish the values on topics
	client.publish("hydro/ph", ph)
	client.publish("hydro/ec", ec)
	time.sleep(60)
	
