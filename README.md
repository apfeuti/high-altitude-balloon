# High-altitude-balloon
Software on a Raspberry Pi zero W for a high-altitude ballon mission

## Install

1. Enable I2C
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c


2. Install pip3
sudo apt-get install python3-pip

3. Install Pyhton-Lib for BME280 Sensor (also install dependencies like CircuitPython)
https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test
sudo pip3 install adafruit-circuitpython-bme280

4. Camera
raspi-config -> Inteface Options -> Camera -> enable
sudo apt-get install python3-picamera
pip3 install exif

5. GPS
https://learn.adafruit.com/adafruit-ultimate-gps/overview
raspi-config -> Inteface Options -> Serial -> No console login, Yes serial port hardware
sudo pip3 install adafruit-circuitpython-gps
