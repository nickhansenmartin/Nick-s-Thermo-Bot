import network
import time

ssid = 'Tufts_Wireless'
password = ''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)

print('Connection successful')
print(station.ifconfig())
