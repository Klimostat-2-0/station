import RPi.GPIO as GPIO
import time
import adafruit_dht, board

LED_PIN_GR = 7
LED_PIN_YE = 12

dht22gpiopin = 'D21'
dhtboard = getattr(board, dht22gpiopin)

dhtDevice = adafruit_dht.DHT22(board.D21, use_pulseio=False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)

def toggleGreen():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)

def toggleYellow():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)

def getSurroundings():
    while True:
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
            # Errors happen fairly often, DHT's are hard to read, just keep going
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
    getSurroundings()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()