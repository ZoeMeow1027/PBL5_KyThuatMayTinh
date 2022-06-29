from glob import glob
import board
import adafruit_dht
import RPi.GPIO as GPIO
import time
import json

import files.fire_detector.physcal_demo as fire_detector_physcal_demo

# MQ-7 - Pin 16
PIN_MQ7 = 23
# Flame sensor - Pin 18
PIN_FLAME = 24
# Buzzer - Pin 22
PIN_BUZZER = 25
# DHT11 - Pin 12
PIN_DHT11 = board.D18

dht11 = None
SETUP_DONE = False

def FireDetect_Setup():
    global SETUP_DONE
    global dht11
    if SETUP_DONE == False:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_MQ7, GPIO.IN)
        GPIO.setup(PIN_FLAME, GPIO.IN)
        GPIO.setup(PIN_BUZZER, GPIO.OUT)
        dht11 = adafruit_dht.DHT11(PIN_DHT11)
        SETUP_DONE = True

def FireDetect_Physcal():
    global SETUP_DONE
    if (SETUP_DONE):
        try:
            result = {}
            result['datetime_unix'] = int(time.time())
            result['temperature'] = dht11.temperature
            result['humidity'] = dht11.humidity
            result['co_detected'] = False if GPIO.input(PIN_MQ7) != 1 else True
            result['flame_detected'] = False if GPIO.input(PIN_FLAME) != 1 else True
        except Exception as ex:
            print('W: '.format(ex))
            result = fire_detector_physcal_demo.FireDetect_Demo()
    else:
        result = fire_detector_physcal_demo.FireDetect_Demo()
    return result

def ToggleBuzzer(enabled: bool):
    global SETUP_DONE
    if (SETUP_DONE):
        GPIO.output(
            PIN_BUZZER,
            GPIO.HIGH if enabled else GPIO.LOW
        )
    else:
        print('W: Physcal components is not initialized!')
    pass

def FireDetect_Release():
    global SETUP_DONE
    global dht11
    SETUP_DONE = False
    if (dht11 != None):
        dht11.exit()
    GPIO.release()
    pass

if __name__ == '__main__':
    while True:
        try:
            FireDetect_Setup()
            print(json.dumps(FireDetect_Physcal()))
            time.sleep(1)
        except Exception as ex:
            print(ex)
        finally:
            FireDetect_Setup()

