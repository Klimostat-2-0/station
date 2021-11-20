import RPi.GPIO as GPIO
import mh_z19
from datetime import datetime
import Adafruit_DHT
import requests

URL = open('.url', 'r').readline()

LED_PIN_GR = 7
LED_PIN_YE = 12
CO2_PIN = 14
SENSE_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)
DHTSensor = Adafruit_DHT.DHT11

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
    station = open('.station', 'r').readline()
    req = {
        "timestamp": time,
        "temperature": temperature,
        "humidity": humidity,
        "co2": co2,
        "station": station
    }
    r = requests.post(
        url = URL,
        data = req
    )

    print(r)

    toggleGreen()
    toggleYellow()



except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()