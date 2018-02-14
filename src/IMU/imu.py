#!/usr/bin/env python
"""Released under the MIT License
Copyright 2015, 2016 MrTijn/Tijndagamer
"""

from mpu6050 import mpu6050
from time import sleep

#sensor = mpu6050(0x68)

#while True:
#    accel_data = sensor.get_accel_data()
#    gyro_data = sensor.get_gyro_data()
#   temp = sensor.get_temp()

#    print("Accelerometer data")
#    print("x: " + str(accel_data['x']))
#    print("y: " + str(accel_data['y']))
#    print("z: " + str(accel_data['z']))

#   print("Gyroscope data")
#    print("x: " + str(gyro_data['x']))
#    print("y: " + str(gyro_data['y']))
#    print("z: " + str(gyro_data['z']))

#    print("Temp: " + str(temp) + " C")
#    sleep(0.5)

def Calibration(sensor):
    averageAccel = [0.0, 0.0, 0.0]
    averageGyro = [0.0, 0.0, 0.0]

    i = 0

    while i < 10:

        accelData = sensor.get_accel_data()
        gyroData = sensor.get_gyro_data()

        averageAccel[0] = averageAccel[0] + accelData['x']
        averageAccel[1] = averageAccel[1] + accelData['y']
        averageAccel[2] = averageAccel[2] + accelData['z']

        averageGyro[0] = averageGyro[0] + gyroData['x']
        averageGyro[1] = averageGyro[1] + gyroData['y']
        averageGyro[2] = averageGyro[2] + gyroData['z']

        i = i+1
        sleep(0.2)

    averageAccel[0] = averageAccel[0]/i
    averageAccel[1] = averageAccel[1]/i
    averageAccel[2] = averageAccel[2]/i

    averageGyro[0] = averageGyro[0]/i
    averageGyro[1] = averageGyro[1]/i
    averageGyro[2] = averageGyro[2]/i
    
    return averageGyro, averageAccel

def waitCrash(sensor, averageAccel, averageGyro):

    isCrash = 0
    accelerationGravitationnel = 9.81
    coefMultiplicateur = 1.5

    while isCrash == 0:
            
        accelData = sensor.get_accel_data()
        gyroData = sensor.get_gyro_data()

        if abs(accelData['x']) > coefMultiplicateur*accelerationGravitationnel:
            isCrash = 1
            print("axe X : ", isCrash)
        elif abs(accelData['y']) > coefMultiplicateur*accelerationGravitationnel:
            isCrash = 1
            print("axe Y : ", isCrash)

        elif abs(accelData['z']) > coefMultiplicateur*accelerationGravitationnel:
            isCrash = 1
            print("axe Z : ", isCrash)

        else:
            isCrash = 0
            print("pas de crash")
                
                  
def test(sensor):

    accelData = sensor.get_accel_data()
    gyroData = sensor.get_gyro_data()
    while True:
        print("axe X", accelData['x'])
        print("axe Y", accelData['y'])
        print("axe Z", accelData['z'])
        sleep(10)

        

         

