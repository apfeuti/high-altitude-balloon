# High-altitude-balloon
Software on a Raspberry Pi zero W for a high-altitude ballon mission

## Install

1. Enable I2C
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c


2. Install pip3

   ```bash
   $ sudo apt-get install python3-pip
   ```

3. Install Pyhton-Lib for BME280 Sensor (also install dependencies like CircuitPython)

   https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test

   ```bash
   $ sudo pip3 install adafruit-circuitpython-bme280
   ```

4. Camera

   raspi-config -> Inteface Options -> Camera -> enable
   
   With the camera running, the whole Raspberry was freezing somewhat between 20 and 120 minutes. Googling around lead to this solution:

   https://raspberrypi.stackexchange.com/questions/41534/raspberry-pi-camera-randomly-freezes-crashes-soc

   Add this two line at the end of
   ```
   /boot/config.txt
   
   over_voltage=4
   force_turbo=1
   ```

   ```bash
   $ sudo apt-get install python3-picamera
   $ pip3 install piexif

   Optional too see exif-infos on Raspberry shell
   $ sudo apt-get install exif
   ```

5. GPS

   https://learn.adafruit.com/adafruit-ultimate-gps/overview

   raspi-config -> Inteface Options -> Serial -> No console login, Yes serial port hardware

   ```bash
   $ sudo pip3 install adafruit-circuitpython-gps
   ```
