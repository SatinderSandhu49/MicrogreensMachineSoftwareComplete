import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
from digitalio import DigitalInOut, Direction

# Initial the dht device, with data pin connected to:
#dhtDevice = adafruit_dht.DHT22(board.D4)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice1 = adafruit_dht.DHT11(board.D25, use_pulseio=False)
dhtDevice2 = adafruit_dht.DHT11(board.D16, use_pulseio=False)
relay1 = board.D23
relay2 = board.D24





while True:
    try:
        # Print the values to the serial port
        temperature_c1 = dhtDevice1.temperature
        temperature_c2 = dhtDevice2.temperature
        
        humidity = dhtDevice1.humidity
        print(
            "Temp1:  {:.1f} C, Temp2:  {:.1f} C   ".format(
                temperature_c1, temperature_c2
            )
        )
        
        if temperature_c1 > 35:
       
           
            with DigitalInOut(relay1) as r1:
                reading = 0

                # setup pin as output and direction low value
                r1.direction = Direction.OUTPUT
                r1.value = True

                time.sleep(0.1)

                r1.direction = Direction.OUTPUT
                r1.value = False
                
                
                time.sleep(20)
         
        if temperature_c2 > 15:
       
           
            with DigitalInOut(relay2) as r2:
                reading1 = 0

                # setup pin as output and direction low value
                r2.direction = Direction.OUTPUT
                r2.value = True

                time.sleep(0.1)

                r2.direction = Direction.OUTPUT
                r2.value = False
                
                
                time.sleep(20)
        

        
        
        
     

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice1.exit()
        raise error

    time.sleep(2.0)
    
    
    
    


 

