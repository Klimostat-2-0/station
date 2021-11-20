import RPi.GPIO as GPIO
import mh_z19
import time
import board
import adafruit_dht

LED_PIN_GR = 7
LED_PIN_YE = 12
CO2_PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)
dhtDevice = adafruit_dht.DHT22(board.D21)

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

def toggleYellow():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)

def getCO2():
    mh_z19.read_from_pwm(CO2_PIN)

def getTempHum():
    while temperature_c is None and humidity is None:
        print("loop")
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        time.sleep(2.0)

try:
    toggleGreen()
    toggleYellow()
    getCO2()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()