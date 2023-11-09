from machine import ADC, Pin, I2C
import uasyncio as asyncio
import math
from pico_i2c_lcd import I2cLcd
import urequests as requests
import ujson
from umqtt import MQTTClient

# AIRTABLE READING #
# Replace with the Airtable API key, base ID, table name, and record ID
API_KEY = 'patAZ83Nmip4h0IzH.5f34bd1c4d93fa3a0bcdbe47c6b9ecf5702498d78f308f7872cb81f481f63342'
BASE_ID = 'appo4v9qUBWpJUbl2'
TABLE_ID = 'tblyvGSPiqA2AINcY'
RECORD_ID = 'rec7ODEleus0mmgRQ'
# Define the URL for the Airtable API
url = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/{RECORD_ID}'

color_val = ''
async def airtable_read():
    global color_val
    # Define your request headers
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }
    try:
        # Make a get request to the API
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            record_data = ujson.loads(response.text)
            color_val = record_data['fields']['unit']
            print('Color Detected: ' + color_val)

    except Exception as e:
        print(f'Error: {e}')

# TEMPERATURE READING #
TempC = 0 # Temperature in Celsius
thermistor = ADC(Pin(26)) # Sets analog to digital conversion pin
Vin = 3.3 # 3.3V being delivered from Pico
Ro = 10000  # 10kOhm Resistor used for 10kOhm thermistor
# Experimentally determined constants for thermistor model
A = 0.01197054312
B = -0.001705399141
C = 0.000009061030683

async def temp_read():
    while True:
        global TempC
        global color_val
        # Get voltage value from ADC thermistor pin
        therm_value = thermistor.read_u16()
        Vout = (3.3/65535)*therm_value

        # Calculate resistance
        Rt = (Vout * Ro) / (Vin - Vout)

        # Steinhart - Hart model of a thermistor
        TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

        # Convert from Kelvin to Celsius
        TempC = TempK - 273.15

        # Prints results every 4 seconds
        if color_val == 'Blue':
            print('Temperature, Kelvin: ' + str(round(TempK, 2)))
        elif color_val == 'Red':
            print('Temperature, degrees Celsius: ' + str(round(TempC, 2)))

        await asyncio.sleep(5)

# WRITE TO SCREEN #
# Creates i2c and lcd objects
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

async def screen():
    global TempC
    global color_val
    while True:
        lcd.blink_cursor_on()
        lcd.putstr("Nick's Thermo Bot"+"\n")
        if color_val == 'Blue':
            TempK = TempC + 273.15
            lcd.putstr("Temperature: "+ "\n"+ str(round(TempK, 2)) + " K")
        elif color_val == 'Red':
            lcd.putstr("Temperature: "+ "\n"+ str(round(TempC, 2)) + " C")
        await asyncio.sleep(1)
        lcd.clear()

# TEMPERATURE LEDS #
# Pin assignments; L6 is on top and L1 is on bottom
pin_numbers = [10, 11, 12, 13, 14, 15]
pins = [Pin(pin, Pin.OUT) for pin in pin_numbers]
L1, L2, L3, L4, L5, L6 = pins
temp_ranges = [0, 10, 20, 30, 40, 50, 60] # Endpoints in degrees Celsius

async def leds():
    while True:
        # Lights up a certain amount depending on temperature
        for i in range(len(temp_ranges) - 1):
            await asyncio.sleep(1)
            # Checks if temperature is below ranges
            if TempC < temp_ranges[0]:
                for a in range(i+1):
                    pins[a].value(False)

            # Checks if temperature is above ranges
            elif TempC > temp_ranges[-1]:
                for b in range(i+1):
                    pins[b].value(True)

            # Checks what bounds the temperature falls into
            elif TempC >= temp_ranges[i] and TempC < temp_ranges[i + 1]:
                for j in range(i + 1):
                    pins[j].value(True)  # Turn on the LEDs
                for j in range(i + 1, len(pins)):
                    pins[j].value(False)  # Turn off the correct LEDs

# ADAFRUIT DASHBOARD #
ADA_IO_URL = 'io.adafruit.com'
ADA_IO_USERNAME = 'nmarti13'
ADA_IO_KEY = 'aio_ZNdu93nhSPHRWyT7W7kwb4XTDJoY'
FEED_KEY1 = 'temp'
FEED_KEY2 = 'units'
async def adafruit():
    global TempC
    global color_val

    # Create an MQTT client and connect
    client = MQTTClient(ADA_IO_USERNAME, ADA_IO_URL, user=ADA_IO_USERNAME, password=ADA_IO_KEY, ssl=False)
    client.connect()

    # Send data to the feed
    if color_val == 'Blue':
        TempK = TempC + 273.15
        tempval = TempK
        unitval = 'Kelvin'
    elif color_val == 'Red':
        tempval = TempC
        unitval = 'Celsius'

    topic1 = bytes('{}/feeds/{}.csv'.format(ADA_IO_USERNAME, FEED_KEY1), 'utf-8')
    client.publish(topic1, bytes(str(tempval), 'utf-8'))

    topic2 = bytes('{}/feeds/{}.csv'.format(ADA_IO_USERNAME, FEED_KEY2), 'utf-8')
    client.publish(topic2, bytes(str(unitval), 'utf-8'))

# MAIN FUNCTION #
async def main():
    asyncio.create_task(airtable_read())
    asyncio.create_task(temp_read())
    asyncio.create_task(screen())
    asyncio.create_task(leds())
    asyncio.create_task(adafruit())
    await asyncio.sleep(120)

asyncio.run(main())

# Turn off all the LEDs at the end of the program
for pin in pins:
    pin.value(False)
