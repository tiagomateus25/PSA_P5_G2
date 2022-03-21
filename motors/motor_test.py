import RPi.GPIO as GPIO
from time import sleep

# Pins for Motor Driver Inputs
Motor1A = 21
Motor1B = 20
Motor1E = 16


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # GPIO Numbering
    GPIO.setup(Motor1A, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)


def loop():
    # Going forwards
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Going forwards")

    sleep(5)
    # Going backwards
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Going backwards")

    sleep(5)
    # Stop
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    print("Stop")


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

