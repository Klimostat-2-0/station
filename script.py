import RPi.GPIO as GPIO
import time
import adafruit_dht, board

LED_PIN_GR = 7
LED_PIN_YE = 12

dht22gpiopin = 'D21'
dhtboard = getattr(board, dht22gpiopin)

dhtDevice = adafruit_dht.DHT22(dhtboard, use_pulseio=False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

def toggleYellow():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)

def getSurroundings():
    try:
        temperature, humidity = dhtDevice.temperature, dhtDevice.humidity
        print("Temperature: {:.1f} °C  Humidity: {:.1f} %".format(temperature, humidity))
    except RuntimeError as error:
        time.sleep(2.0)
        temperature, humidity = dhtDevice.temperature, dhtDevice.humidity
        print("Temperature: {:.1f} °C  Humidity: {:.1f} %".format(temperature, humidity))

try:
    toggleGreen()
    toggleYellow()
    getSurroundings()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()