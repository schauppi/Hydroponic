import RPi.GPIO as GPIO
import time

#RELAIS_lamp = 18 #Lampe
taster = 5
#taster_state = 0
global taster_state
GPIO.setmode(GPIO.BCM)
GPIO.setup(taster, GPIO.IN, GPIO.PUD_UP)
#GPIO.setup(RELAIS_lamp, GPIO.OUT) # GPIO Modus zuweisen

#GPIO.output(RELAIS_lamp, True)
"""
if GPIO.input(RELAIS_lamp) == 1:
	taster_state = 1
	print(taster_state)
else:
	taster_state = 0
	print(taster_state)
"""

def button_callback(channel):
	print("test")
	"""
	if taster_state == 1:
		GPIO.output(RELAIS_lamp, False)
		taster_state = 0
		global taster_state
	elif taster_state == 0:
		GPIO.output(RELAIS_lamp, True)
		taster_state = 1
		global taster_state"""
		
	
GPIO.add_event_detect(taster, GPIO.RISING, callback=button_callback, bouncetime = 250)



while True:
	#button_state = GPIO.input(taster)
	#print("button_state")
	time.sleep(0.01)

