import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

p = GPIO.PWM(11,50)
p.start(0)
print("Starting 0")
time.sleep(5)

p.ChangeDutyCycle(3)
print("3")
time.sleep(5)

try:
    while True:
        i = 4
        while i < 10:
            print(i)
            p.ChangeDutyCycle(i)
            time.sleep(0.05)
            i += 0.02
        while i > 4:
            print(i)
            p.ChangeDutyCycle(i)
            time.sleep(0.05)
            i -= 0.05
except:
    KeyboardInterrupt