import RPi.GPIO as GPIO
import mh_z19
import time
import Adafruit_DHT


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
    toggleGreen()
    toggleYellow()
    getCO2()
    getTempHum()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()