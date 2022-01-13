import asyncio

from azure.iot.device.iothub.models import message
import RPi.GPIO as GPIO
import mh_z19
import Adafruit_DHT
import requests
import json
import os
from datetime import datetime
from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient

PATH = "/home/pi/station/"
URL = open(PATH + '.url', 'r').readline().strip()
# Used to connect the device to the IOT Hub
CONNECTION_STRING = open(PATH + '.conKey', 'r').readline().strip()
# Create instance of the device client
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
PAYLOAD = '{{"timestamp": {timestamp}, "temperature": {temperature}, "humidity": {humidity}, "co2": {co2}, "station": {station}}}'

LED_PIN_GR = 7
LED_PIN_YE = 12
CO2_PIN = 14
SENSE_PIN = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_GR, GPIO.OUT)
GPIO.setup(LED_PIN_YE, GPIO.OUT)
DHTSensor = Adafruit_DHT.DHT22


def is_cnx_active(timeout):
    try:
        requests.head(URL + 'station', timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def yellow_on():
    GPIO.output(LED_PIN_YE, GPIO.HIGH)


def yellow_off():
    GPIO.output(LED_PIN_YE, GPIO.LOW)


def green_on():
    GPIO.output(LED_PIN_GR, GPIO.HIGH)


def green_off():
    GPIO.output(LED_PIN_GR, GPIO.LOW)


def get_co2():
    return mh_z19.read_from_pwm(CO2_PIN)


def get_temperature_humidity():
    _humid, _temper = Adafruit_DHT.read_retry(DHTSensor, SENSE_PIN)
    return round(_humid, 2), round(_temper, 2)


async def send_telemetry(data, client):
    await client.connect()
    try:
        payload = PAYLOAD.format(timestamp=data.get("timestamp"), temperature=data.get("temperature"), humidity=data.get("humidity"), co2=data.get("co2"), station=data.get("station"))
        message = Message(payload)
        #message = Message(data)
        message.content_type = "application/json"

        if client.connected:
            print(f"Sending message: {message}")
            await client.send_message(message)
            print("Message successfully sent!")
        else:
            await client.disconnect()
            client = IoTHubDeviceClient.create_from_connection_string(
                CONNECTION_STRING)
            print("Disconnected client.")
            await client.connect()
            print(f"Sending message: {message}")
            await client.send_message(message)
            print("Message successfully sent!")

    except Exception as error:
        print(error.args[0])
    finally:
        await client.disconnect()
        print("Disconnected client.")


def send_data(data):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(send_telemetry(data, client))

        # API request
        r = requests.post(
            url=URL + 'measurement',
            data=data
        )
    except Exception as error:
        print(error.args[0])


def collect_station_limit():
    try:
        if is_cnx_active(1):
            r = requests.get(
                url=URL + f"station/limit/{open(PATH + '.station', 'r').readline().strip()}"
            )
            open(PATH + '.limit', 'w').write(str(json.loads(r.content)['co2_limit']))
            open(PATH + '.reset', 'w').write(str(json.loads(r.content)['co2_reset']))
        else:
            write_to_log("Could not get limit - cnx down")
    except:
        write_to_log("Could not get limit - exception")


def write_to_log(line):
    open(PATH + 'klimostat.log', 'a').write(f"{datetime.now()} - {line} \n")


def write_to_cache(obj):
    with open(PATH + 'cache.json', 'a') as outfile:
        outfile.write(obj)


def post_cache():
    if os.path.exists(PATH + 'cache.json'):
        with open(PATH + 'cache.json') as f:
            for jsonLine in f:
                try:
                    obj = json.loads(jsonLine)
                    send_data(obj)
                except json.decoder.JSONDecodeError:
                    write_to_log('Cache line could not be parsed: ' + jsonLine)
                    pass
                finally:
                    os.remove(PATH + 'cache.json')


def handle_co2_value(value):
    global STATE_YELLOW, STATE_GREEN
    if value >= int(open(PATH + '.limit', 'r').read().strip()):
        green_off()
        yellow_on()
    if value <= int(open(PATH + '.reset', 'r').read().strip()):
        yellow_off()
        green_on()
    if not GPIO.input(LED_PIN_GR) and not GPIO.input(LED_PIN_YE):
        green_off()
        yellow_on()


def make_measurement():
    time = str(datetime.utcnow()) + 'Z'
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
        write_to_log("Couldn't reach API - cnx down");
        json_object = json.dumps(req, indent=0).replace("\n", "") + "\n"
        write_to_cache(json_object)
    else:
        post_cache()
        send_data(req)
    return co2


try:
    collect_station_limit()
    co2 = make_measurement()
    handle_co2_value(co2)
except KeyboardInterrupt:
    GPIO.cleanup()
