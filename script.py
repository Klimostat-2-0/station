import RPi.GPIO as GPIO
import Adafruit_DHT
import time

LED_PIN_GR = 7
LED_PIN_YE = 12
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

def toggleYellow():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)

def getSurroundings():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")

try:
    toggleGreen()
    toggleYellow()
    getSurroundings()
    time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()