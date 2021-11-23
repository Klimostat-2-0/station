import RPi.GPIO as GPIO
import mh_z19
from datetime import datetime
import Adafruit_DHT
import requests
import json
import os
from datetime import datetime

PATH = "/home/pi/station/"
URL = open(PATH + '.url', 'r').readline().strip()

LED_PIN_GR = 7
LED_PIN_YE = 12
CO2_PIN = 14
SENSE_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)
DHTSensor = Adafruit_DHT.DHT11


def is_cnx_active(timeout):
    try:
        requests.head(URL, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def toggle_green():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)


def toggle_yellow():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)


def get_co2():
    return mh_z19.read_from_pwm(CO2_PIN)


def get_temperature_humidity():
    _humid, _temper = Adafruit_DHT.read_retry(DHTSensor, SENSE_PIN)
    return _humid, _temper


def send_data(data):
    # TODO: Make request to Azure IOT
    r = requests.post(
        url=URL,
        data=data
    )


def write_to_log(line):
    open(PATH + 'klimostat.log', 'a').write(f"{datetime.now()} - {line} \n")


def write_to_cache(obj):
    with open(PATH + 'cache.json', 'a') as outfile:
        outfile.write(obj)


def post_cache():
    if os.path.exists(PATH + 'cache.json'):
        with open(PATH + 'cache.json') as f:
            for jsonLine in f:
                obj = json.loads(jsonLine)
                send_data(obj)
            os.remove(PATH + 'cache.json')


def make_measurement():
    time = str(datetime.now())
    humidity, temperature = get_temperature_humidity()
    co2 = get_co2()['co2']
    station = open(PATH + '.station', 'r').readline().strip()
    req = {
        "timestamp": time,
        "temperature": temperature,
        "humidity": humidity,
        "co2": co2,
        "station": station
    }

    if not is_cnx_active(1):
        write_to_log("Couldn't reach API")
        json_object = json.dumps(req, indent=0).replace("\n", "") + "\n"
        write_to_cache(json_object)
    else:
        post_cache()
        send_data(req)


try:
    make_measurement()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
