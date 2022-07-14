import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

ldr=17
tunda=2

def rc_time(ldr):
    count=0
    GPIO.setup(ldr,GPIO.OUT)
    GPIO.sleep(tunda)
    GPIO.setup(ldr,GPIO.IN)
    while(GPIO.input(ldr)==GPIO.LOW):
        count+=1
    return count

try:
    while True:
        print(rc_time(ldr))
except KeyboardInterrupt:
        pass
finally:
    GPIO.cleanup()
