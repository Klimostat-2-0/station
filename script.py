import RPi.GPIO as GPIO
import mh_z19
from datetime import datetime
import Adafruit_DHT
import requests
import json
import os
from datetime import datetime

PATH = "/home/pi/station/"
URL = open(PATH + '.url', 'r').readline().strip()

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

def sendData(data):
    #TODO: Make request to Azure IOT
    r = requests.post(
        url=URL,
        data=data
    )


try:
    time = str(datetime.now())
    humidity, temperature = getTempHum()
    co2 = getCO2()['co2']
    station = open(PATH + '.station', 'r').readline().strip()
    req = {
        "timestamp": time,
        "temperature": temperature,
        "humidity": humidity,
        "co2": co2,
        "station": station
    }

    if not is_cnx_active(1):
        open(PATH + 'klimostat.log', 'a').write(f"{datetime.now()} - Couldn't reach API \n")
        json_object = json.dumps(req, indent=0).replace("\n", "") + "\n"

        with open(PATH + 'cache.json', 'a') as outfile:
            outfile.write(json_object)
    else:
        if os.path.exists(PATH + 'cache.json'):
            with open(PATH + 'cache.json') as f:
                for jsonLine in f:
                    obj = json.loads(jsonLine)
                    sendData(obj)
                os.remove(PATH + 'cache.json')
        sendData(req)

    toggleGreen()
    toggleYellow()

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
