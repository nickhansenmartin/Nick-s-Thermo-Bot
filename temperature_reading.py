from machine import ADC, Pin
from time import sleep
import math

thermistor = ADC(Pin(26)) # Sets analog to digital conversion pin

Vin = 3.3 # 3.3V being delivered from Pico
Ro = 10000  # 10kOhm Resistor used for 10kOhm thermistor

# Experimentally Determined Constants
A = 0.01197054312
B = -0.001705399141
C = 0.000009061030683

while True:
    # Get voltage value from ADC thermistor pin
    therm_value = thermistor.read_u16()
    Vout = (3.3/65535)*therm_value

    # Calculate resistance
    Rt = (Vout * Ro) / (Vin - Vout)

    # Steinhart - Hart model of a thermistor
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = TempK - 273.15

    #Prints results every 4 seconds
    print('Celsius: ' + str(round(TempC, 2)))
    print('Kelvin: ' + str(round(TempK, 2)))
    sleep(4)
