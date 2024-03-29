from raspi_board import Board
from bme280 import BME280
from gps_ultimate import GPSUltimate
from picture_capturer import PictureCapturer
from measure_recorder import MeasureRecorder
import time
import calendar
import sys
import os
import logging
from pathlib import Path

# make data directory
Path("./data/log").mkdir(parents=True, exist_ok=True)
Path("./data/pictures").mkdir(parents=True, exist_ok=True)

# logging timestamp with millis AND timezone is tricky. See https://stackoverflow.com/questions/43667155/datetime-with-milliseconds-or-microseconds-and-timezone-offset
tz = time.strftime('%z')
loggingFormat = '%(asctime)s' + tz + ' %(threadName)s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(format=loggingFormat, filename='./data/log/balloon.log', level=logging.DEBUG)

# log also to console
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter(loggingFormat)
consoleHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(consoleHandler)

# delay start - this gives the possibilty to ssh-login through the home-wifi and kill the process before real start
startup_delay = 0
try:
    startup_delay = int(sys.argv[1])
except:
    # do nothing
    pass
    
logger.info("Balloon main-script started before startup-delay of {} seconds".format(startup_delay))
time.sleep(startup_delay)
logger.info("Balloon main-script started after startup-delay")

board = Board()

from gps_mock import GPSMock
#gps = GPSMock()
gps = GPSUltimate()

while gps.altitude() is None:
    logger.info("GPS-altitude is None - waiting for fix")
    time.sleep(1)

# we cannot immediately read the time from the gps - it seems to be invalid for a certain time
# waiting improves the altitude-accuracy as well
time.sleep(60)

gps_local_time = time.localtime(calendar.timegm(gps.utc())) # convert time_struct UTC to time_struct local-time
logger.info("GPS got fix. Setting system-time to {}".format(time.strftime('%Y-%m-%d %H:%M:%S %z', gps_local_time)))
# first, we have to (manualy, outside of this script) disable automatic network-time sync: sudo timedatectl set-ntp false
# to enable it again: sudo timedatectl set-ntp true
# https://raspberrytips.com/time-sync-raspberry-pi/
output_timedatectl = os.popen("sudo timedatectl set-time '{}'".format(time.strftime('%Y-%m-%d %H:%M:%S', gps_local_time))).readline()
# timestamps in logfile up to here are not accurate - since the time on the OS is NOT set before here!
logger.info("Output from sudo timedatectl set-time: {}".format(output_timedatectl))

logger.info("GPS initial altitude: " + str(gps.altitude()))

gps.startThread()

# 1hPa reduction per 8.3m altitude (seems that https://www.meteoschweiz.admin.ch/home/messwerte.html?param=messwerte-luftdruck-qfe-10min uses this formula).
# For a more dedicated formula see https://de.wikipedia.org/wiki/Barometrische_Höhenformel, section Reduktion auf Meereshöhe

ADDRESS_IN_CAPSULE = 0x77
qfe = BME280.pressureStatic(ADDRESS_IN_CAPSULE) # do NOT make an intance here, which would create a thread.
qff = qfe + (gps.altitude() / 8.3 ) - 1.1 # - correction-factor. Determined empiric
bme280InCapsule = BME280(qff, ADDRESS_IN_CAPSULE)
bme280InCapsule.startThread("BME280CapsuleThread")

ADDRESS_OUTSIDE = 0x76 # wire SDO to GND
qfe = BME280.pressureStatic(ADDRESS_OUTSIDE) # do NOT make an intance here, which would create a thread.
qff = qfe + (gps.altitude() / 8.3 ) - 1.15 # - correction-factor. Determined empiric
bme280Outside = BME280(qff, ADDRESS_OUTSIDE)
bme280Outside.startThread("BME280OutsideThread")


measureRecorder = MeasureRecorder('./data/log/measures.csv', 2, board, gps, bme280InCapsule, bme280Outside)
measureRecorder.start_measures()

# init wifi
#try:
    #board.disableWifi(gps.altitude())
    #time.sleep(5) # give some time to disable wifi
    #board.enableWifi(gps.altitude())
#except:
 #   logger.exception("Exception by setting-up Wifi")

# register listeners on events
#gps.subscribe_rise_above(4000, board.disableWifi)
#gps.subscribe_fall_below(4000, board.enableWifi)

pictureCapturer = PictureCapturer(5, gps)
gps.subscribe_landed(pictureCapturer.stop_capturing)
pictureCapturer.start_capturing()

logger.info("Main finished")
