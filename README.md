# Nick-s-Thermo-Bot
Code repository for Nick's Thermo-Bot, a device that reads an Airtable value from OpenCV to determine units, measures temperature, and displays the output through in three ways: through an LED thermometer, an LCD display, and on the connected PC.

main.py: This function integrates all the sub-functions of the thermo-bot, which are elaborated upon in each of the following test files. The exception is that it does not include pyscript_color_sending.py, as that is meant for use with the Pyscript website. It does not need any of the following test files to run.

pyscript_color_sending.py: This function needs to be pasted in the appropriate Pyscript website found here (https://pyscript.com/@nmarti13/me35-midterm-camera/latest), where it uses OpenCV to detect the color seen (red for Celsius, blue for Kelvin), and then uploads the value to an Airtable when given the correct access key.

color_reading.py: This function reads the Airtable value as red or blue.

temperature_reading.py: This function implements the Steinhart-Hart model of a thermistor given three calibrated temperatures and resistances to get an accurate temperature reading from the voltage output of the thermistor.

screen_test.py: This function simply outputs text to the LCD screen

light_test.py: This function turns on a certain amount of lights on the LED thermometer given some simulated temperature.

internet_test.py: This function simply tests connectivity of the Pi Pico for the purposes of internet communications (i.e., for the Airtable API).

adafruit_test.py: This function allows testing of the MQTT sending of data to the Adafruit dashboard

LIBRARIES:
None of the following libraries were written by Nicholas Martin. They are easily available online and meant for public use.

lcd_api.py and pico_i2c_lcd.py are two externally sourced libraries only used for the correct operation of the LCD display.

main.py also uses a few common libraries: machine, uasyncio, urequests, ujson
