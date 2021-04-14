from AtlasI2C import (AtlasI2C)
import time
#needed for PH and EC
def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
    for i in device_address_list:
		device.set_i2c_address(i)
		response = device.query("I")
		moduletype = response.split(",")[1] 
		response = device.query("name,?").split(",")[1]
		device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list 

def measure(device_list):
	for dev in device_list:
		dev.write("R")
		time.sleep(3)
	dev_count = 0
	for dev in device_list:
		if dev_count == 0:
			ph = dev.read()
			ph = ph
			ph = (float(ph))
		else:
			ec = dev.read()
			ec = ec
			ec = (float(ec))
		dev_count += 1
		
	return ph, ec
