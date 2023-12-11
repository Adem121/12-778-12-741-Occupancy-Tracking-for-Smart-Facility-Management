import network
import time
import utime
from machine import Pin
from umqtt.simple import MQTTClient
# from umqtt import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to the network
wlan.connect('CMU-DEVICE')
time.sleep(5)
print(wlan.isconnected())

sensor_pin = Pin(0, Pin.IN)
sensor_temp = machine.ADC(4)

mqtt_server = 'io.adafruit.com'
client_id = 'client'
topic_pub = b'Ademtaiyr/feeds/welcome-feed'
   
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user="Ademtaiyr", password="aio_isMT98jVUPgtuDfcc2jiqQeYoLvt", keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

# specify coordinates of sensor
SENSOR_X_Y = (3.6, 2.1)

while True:
    try:
        # Attempt to connect to MQTT
        client = mqtt_connect()

        # Main loop for sensor reading and publishing
        while True:
            # Positive readings from sound sensor are 0, while for vibration sensor it is 1. If using sound sensor, uncomment the following line
            # if sensor_pin.value() == 0:'
            # If using vibration sensor, uncomment the following line
            if sensor_pin.value() == 1:
                print("Signal detected!")
                reading = sensor_temp.read_u16() * 3.3 / 65535
                temperature = 27 - (reading - 0.706) / 0.001721
                # If using sound sensor, uncomment the following line
                # client.publish(topic_pub, f'{SENSOR_X_Y}, Sound, {temperature}')
                # If using vibration sensor, uncomment the following line
                client.publish(topic_pub, f'{SENSOR_X_Y}, Vibration, {temperature}')
                utime.sleep_ms(1000)
    # Error handling for automatic reconnection in case of error
    except OSError as e:
        # Handle ECONNRESET error due to MQTT Broker limitations which cause sensors to disconnect
        if e.args[0] == 104:
            print("Caught ECONNRESET error. Reconnecting...")
            time.sleep(2)
        else:
            print("Unhandled OSError:", e)
            reconnect()
    except Exception as e:
        print("Unhandled exception:", e)
        reconnect()