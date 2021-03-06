import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 4 
GPIO_ECHO = 17
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartZeit = time.time()
    StopZeit = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
 
    TimeElapsed = StopZeit - StartZeit
   
    distance = (TimeElapsed * 34300) / 2
 
    return distance
    
