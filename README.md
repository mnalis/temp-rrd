Creates RRD graphs for current and historic temperatures and humidity, to be
viewed in web browser.

Created to be used on Raspberry Pi with following hardware:

- RaspberryPi internal temperature sensor
  libraspberrypi-bin for Raspbian repository

- USB TEMPer temperature sensor
  https://github.com/mnalis/TEMPer-DX

- DHT11 temperature and humidity sensor
  https://github.com/adafruit/Adafruit_Python_DHT

but is intended to be easily extendable and run on any GNU/Linux OS.

If you do not have outside sensor (or it is impractical to connect it to
RaspberryPi), you have the option to pull outside temperature from 
http://openweathermap.org/

Follow INSTALL.txt for installation instructions.
