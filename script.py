import RPi.GPIO as GPIO
import time

LED_PIN_GR = 7
LED_PIN_YE = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

def toggleYellow():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

try:
    toggleGreen()
    toggleYellow()
    time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()