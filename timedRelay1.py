import time
import board
import RPi.GPIO as GPIO
from digitalio import DigitalInOut, Direction


relay1 = board.D5






while True:
    try:
        
           
            with DigitalInOut(relay1) as r1:
                reading = 0

                # setup pin as output and direction low value
                r1.direction = Direction.OUTPUT
                r1.value = True

                time.sleep(0.1)

                r1.direction = Direction.OUTPUT
                r1.value = False
                
                
                time.sleep(900)
                
               
                r1.direction = Direction.OUTPUT
                r1.value = True
                
                
                time.sleep(900)
         
         
     
     

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        
        raise error

    time.sleep(2.0)
    
    
    
    


 


