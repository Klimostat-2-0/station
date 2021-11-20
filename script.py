import RPi.GPIO as GPIO
import time

LED_PIN_GR = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

try:
    toggleGreen()
    time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()