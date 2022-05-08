#!/usr/bin/python3
from mpu6050 import mpu6050
import time
mpu = mpu6050(0x68)  # check if it's the right pin

while True:
    print("Temp : "+str(mpu.get_temp()))
    print()

    accel_data = mpu.get_accel_data()
    print("Acc X : "+str(accel_data['x']), end='\r')
    print("Acc Y : "+str(accel_data['y']), end='\r')
    print("Acc Z : "+str(accel_data['z']), end='\r')
    print()

    gyro_data = mpu.get_gyro_data()
    print("Gyro X : "+str(gyro_data['x']), end='\r')
    print("Gyro Y : "+str(gyro_data['y']), end='\r')
    print("Gyro Z : "+str(gyro_data['z']), end='\r')

    time.sleep(0.1)

