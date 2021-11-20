import RPi.GPIO as GPIO
import mh_z19
import time

LED_PIN_GR = 7
LED_PIN_YE = 12
CO2_PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

def toggleYellow():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)

def getCO2():
    mh_z19.read_from_pwm(CO2_PIN)


try:
    toggleGreen()
    toggleYellow()
    getCO2()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()