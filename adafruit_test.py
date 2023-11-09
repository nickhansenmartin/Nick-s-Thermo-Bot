

import network
from umqtt import MQTTClient
import time

# Replace these with your specific details
WIFI_SSID = 'Tufts_Wireless'
WIFI_PASSWORD = ''
ADA_IO_URL = 'io.adafruit.com'
ADA_IO_USERNAME = 'nmarti13'
ADA_IO_KEY = '(placeholder)'
FEED_KEY = 'temp'

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for connection with a timeout
max_wait = 10
while max_wait > 0:
    if wifi.isconnected():
        print("Connected to WiFi")
        break
    max_wait -= 1
    time.sleep(1)

# Create an MQTT client
client = MQTTClient(ADA_IO_USERNAME, ADA_IO_URL, user=ADA_IO_USERNAME, password=ADA_IO_KEY, ssl=False)

# Connect to Adafruit IO MQTT broker
try:
    client.connect()
except Exception as e:
    print("Could not connect to MQTT broker. Check your Adafruit IO Key.")
    raise e

# Send data to the feed
value_to_send = 1
topic = bytes('{}/feeds/{}.csv'.format(ADA_IO_USERNAME, FEED_KEY), 'utf-8')
client.publish(topic, bytes(str(value_to_send), 'utf-8'))

print("Data sent to Adafruit IO!")

# Disconnect from MQTT broker
client.disconnect()

# Turn off WiFi to save power
wifi.active(False)
