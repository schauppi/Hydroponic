import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 4 
GPIO_ECHO = 17
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)



#--neu
#30 - 9.0
#27.5 - 8.0
#25l - 10.0 
#22.5l - 13.0 / 12
#20l - 15.0 / 14
#17.5l - 16.0 / 17 --Warnung
def distance():
    try:
        
        distance_list_5 = []
        
        #average over 5 averages
        
        for i in range(5):
    
            distance_list = []

            #measure and average 1500 measurements
            for i in range(1500):
            
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
                
                distance_list.append(distance)
            
            distance = round(sum(distance_list) / len(distance_list))
            
            distance_list_5.append(distance)
            
        distance = round(sum(distance_list_5) / len(distance_list_5))
        
        if distance == 9.0:
             return 30.0
        elif distance == 8.0:
            return 27.5
        elif distance == 10.0:
            return 25.0
        elif distance == 12.0 or distance == 13.0:
            return 22.5
        elif distance == 15.0 or distance == 14.0:
            return 20.0
        elif distance == 16.0 or distance == 17.0:
            return 17.5
        elif distance == None:
            return 27.5
        
        #return distance
        
    except:
        
        return 0


