import RPi.GPIO as GPIO
import mh_z19
from datetime import datetime
import Adafruit_DHT
import requests
import json
import os

URL = open('.url', 'r').readline().strip()

LED_PIN_GR = 7
LED_PIN_YE = 12
CO2_PIN = 14
SENSE_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)
DHTSensor = Adafruit_DHT.DHT11

def is_cnx_active(timeout):
    try:
        requests.head(URL, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

def toggleYellow():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)

def getCO2():
    return mh_z19.read_from_pwm(CO2_PIN)

def getTempHum():
    _humid, _temper = Adafruit_DHT.read_retry(DHTSensor, SENSE_PIN)
    return _humid, _temper

try:
    time = str(datetime.now())
    humidity, temperature = getTempHum()
    co2 = getCO2()['co2']
    station = open('.station', 'r').readline().strip()
    req = {
        "timestamp": time,
        "temperature": temperature,
        "humidity": humidity,
        "co2": co2,
        "station": station
    }

    if not is_cnx_active(1):
        json_object = json.dumps(req, indent=4)

        if os.path.exists("cache.json"):
            content = open("cache.json", "r").read()


        with open("cache.json", "w") as outfile:
            if content is not None:
                outfile.write(content + "\n")
            outfile.write(json_object)
        print("Can't connect!")
    else:
        r = requests.post(
            url=URL,
            data=req
        )
        print("Connected:", r)

    toggleGreen()
    toggleYellow()



except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()