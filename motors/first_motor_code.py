#!/usr/bin/python3
import time
import numpy as np
import RPi.GPIO as GPIO

# pins
motor13 = 13
motor18 = 18
motor35 = 35
motor38 = 38
frequency = 50


def main():

    # Setting pins as outputs
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # GPIO Numbering
    GPIO.setup(motor13, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(motor18, GPIO.OUT)
    GPIO.setup(motor35, GPIO.OUT)
    GPIO.setup(motor38, GPIO.OUT)

    # Adjusting motor frequency
    p_motor13 = GPIO.PWM(motor13, frequency)
    p_motor18 = GPIO.PWM(motor18, frequency)
    p_motor35 = GPIO.PWM(motor35, frequency)
    p_motor38 = GPIO.PWM(motor38, frequency)

    # Motor start
    p_motor13.start(0)
    p_motor18.start(0)
    p_motor35.start(0)
    p_motor38.start(0)
    print("starting 0")
    time.sleep(3)

    # Motor spinning
    p_motor13.ChangeDutyCycle(3)
    p_motor18.ChangeDutyCycle(3)
    p_motor35.ChangeDutyCycle(3)
    p_motor38.ChangeDutyCycle(3)
    print("3")
    time.sleep(5)

    try:
        while 1:
            for dc in np.arange(0, 21, 0.2):
                p_motor13.ChangeDutyCycle(dc)
                p_motor18.ChangeDutyCycle(dc)
                p_motor35.ChangeDutyCycle(dc)
                p_motor38.ChangeDutyCycle(dc)
                time.sleep(0.1)
            for dc in np.arange(20, -1, -0.2):
                p_motor13.ChangeDutyCycle(dc)
                p_motor18.ChangeDutyCycle(dc)
                p_motor35.ChangeDutyCycle(dc)
                p_motor38.ChangeDutyCycle(dc)
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    # Motor stop
    p_motor13.stop()
    p_motor18.stop()
    p_motor35.stop()
    p_motor38.stop()

    GPIO.cleanup()


if __name__ == "__main__":
    main()
