from machine import Pin
from time import sleep

sim_temp = 24 # Simulated temperature in Celsius

# Pin assignments; L6 is on top and L1 is on bottom
pin_numbers = [10, 11, 12, 13, 14, 15]
pins = [Pin(pin, Pin.OUT) for pin in pin_numbers]
L1, L2, L3, L4, L5, L6 = pins

temp_ranges = [0, 10, 20, 30, 40, 50, 60] # Endpoints in degrees Celsius

# Lights up a certain amount depending on temperature
for i in range(len(temp_ranges) - 1):
    if sim_temp < temp_ranges[0]: # Checks if temperature is below ranges
        for a in range(i+1):
            pins[a].value(False)

    elif sim_temp > temp_ranges[-1]: # Checks if temperature is above ranges
        for b in range(i+1):
            pins[b].value(True)

    elif sim_temp >= temp_ranges[i] and sim_temp < temp_ranges[i + 1]: # Checks what bounds the temperature falls into
        for j in range(i + 1):
            pins[j].value(True)  # Turn on the LEDs
        for j in range(i + 1, len(pins)):
            pins[j].value(False)  # Turn off the LEDs
