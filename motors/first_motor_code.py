#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

# pins
motor2 = 2
motor5 = 5
motor9 = 9
motor13 = 13
frequency = 50


def main():

    # Setting pins as outputs
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # GPIO Numbering
    GPIO.setup(motor2, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(motor5, GPIO.OUT)
    GPIO.setup(motor9, GPIO.OUT)
    GPIO.setup(motor13, GPIO.OUT)

    # Adjusting motor frequency
    p_motor2 = GPIO.PWM(motor2, frequency)
    p_motor5 = GPIO.PWM(motor5, frequency)
    p_motor9 = GPIO.PWM(motor9, frequency)
    p_motor13 = GPIO.PWM(motor13, frequency)

    # Motor start
    p_motor2.start(0)
    p_motor5.start(0)
    p_motor9.start(0)
    p_motor13.start(0)
    print("starting 0")
    time.sleep(3)

    # Motor spinning
    p_motor2.ChangeDutyCycle(3)
    p_motor5.ChangeDutyCycle(3)
    p_motor9.ChangeDutyCycle(3)
    p_motor13.ChangeDutyCycle(3)
    print("3")
    time.sleep(10)

    try:
        while 1:
            for dc in range(0, 101, 5):
                p_motor2.ChangeDutyCycle(dc)
                p_motor5.ChangeDutyCycle(dc)
                p_motor9.ChangeDutyCycle(dc)
                p_motor13.ChangeDutyCycle(dc)
                time.sleep(0.1)
            for dc in range(100, -1, -5):
                p_motor2.ChangeDutyCycle(dc)
                p_motor5.ChangeDutyCycle(dc)
                p_motor9.ChangeDutyCycle(dc)
                p_motor13.ChangeDutyCycle(dc)
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    # Motor stop
    p_motor2.stop()
    p_motor5.stop()
    p_motor9.stop()
    p_motor13.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
