import RPi.GPIO as GPIO
import time

LED_PIN_GR = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)

def toggleGreen():
    GPIO.output(LED_PIN, GPIO.HIGH)


toggleGreen()
time.sleep(1000)
GPIO.cleanup()