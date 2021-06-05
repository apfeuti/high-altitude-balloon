from raspi_board import Board
from bme280 import BME280
from gps_ultimate import GPSUltimate
from picture_capturer import PictureCapturer
import csv
import os.path
import datetime
import time
import logging

# logging timestamp with millis AND timezone is tricky. See https://stackoverflow.com/questions/43667155/datetime-with-milliseconds-or-microseconds-and-timezone-offset
tz = time.strftime('%z')
loggingFormat = '%(asctime)s' + tz + ' %(threadName)s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(format=loggingFormat, filename='balloon.log', level=logging.DEBUG)

# log also to console
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter(loggingFormat)
consoleHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(consoleHandler)

board = Board()
bme280 = BME280(1013.25)


print("board-Temp:" + str(board.temp()))
print("volts-core:" + str(board.volt_core()))
print("volts-sdram_c:" + str(board.volt_sdram_c()))
print("volts-sdram_i:" + str(board.volt_sdram_i()))
print("volts-sdram_p:" + str(board.volt_sdram_p()))
print("board-throttled:" + board.throttled())
print("")
print("out_temp:" + str(bme280.temp()))
print("out_humidity:" + str(bme280.humidity()))
print("out_pressure:" + str(bme280.pressure()))
print("baro_altitude:" + str(bme280.altitude()))


""" class LandingObserver:
    def notifyx(self, landing_altitude):
        print("LANDED at " + str(landing_altitude))
        
    def disable_wifi(self, altitude):
        print("Disable Wifi at altitude " + str(altitude))
        
    def burst(self, altitude):
        print("BURST at altitude " + str(altitude))
    
    def enable_wifi(self, altitude):
        print("Enable Wifi at altitude " + str(altitude))

landingObserver = LandingObserver()

gps = GPS()
gps.subscribe_landed(landingObserver.notifyx)
gps.subscribe_rise_above(4000, landingObserver.disable_wifi)
gps.subscribe_fall_below(4000, landingObserver.enable_wifi)
gps.subscribe_burst(landingObserver.burst)


class BaroObserver:
    def landed(self, landing_altitude):
        print("Baro-LANDED at " + str(landing_altitude))
        
    def above(self, burst_altitude):
        print("Baro-above at " + str(burst_altitude))

baroObserver = BaroObserver()
bme280.subscribe_landed(baroObserver.landed)
bme280.subscribe_rise_above(4242, baroObserver.above)


class LandingObserver2:
    def notifyx(self, landing_altitude):
        print("XLaNdEd at " + str(landing_altitude))
        
    def disable_wifi(self, altitude):
        print("xDisable Wifi at altitude " + str(altitude))
        
    def burst(self, altitude):
        print("xBURST at altitude " + str(altitude))
    
    def enable_wifi(self, altitude):
        print("xEnable Wifi at altitude " + str(altitude))

landingObserver = LandingObserver2()
gps2 = GPS()
gps2.subscribe_landed(landingObserver.notifyx)

gps2.subscribe_rise_above(20560, landingObserver.disable_wifi)
gps2.subscribe_fall_below(18669, landingObserver.enable_wifi)
gps2.subscribe_burst(landingObserver.burst)


data_file = 'measures.csv'

if not os.path.exists(data_file):
    header = ["time_utc", "board_temp", "board_volts_core", "board_volts_sdram_c", "board_volts_sdram_i", "board_volts_sdram_p", "board_throttled",
                "gps_latitude", "gps_longitude", "gps_altitude", "gps_ascending_rate", "gps_speed", "gps_heading",
                "out_temp", "out_humidity", "out_pressure", "baro_altitude"]
    with open('measures.csv', 'wt') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)

do_measure = False

while (do_measure):
    with open(data_file, 'a') as csvfile:
        now = datetime.datetime.utcnow().replace(microsecond=0).replace(tzinfo=datetime.timezone.utc).isoformat()

        data = [now,
                board.temp(),
                board.volt_core(),
                board.volt_sdram_c(),
                board.volt_sdram_i(),
                board.volt_sdram_p(),
                board.throttled(),                  #0x5 means: under voltage, currently throttled. See https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=147781&start=50#p972790
                "{:0.6f}".format(gps.latitude()),
                "{:0.6f}".format(gps.longitude()),
                "{:0.2f}".format(gps.altitude()),
                "{:0.2f}".format(gps.ascending_rate()),
                "{:0.2f}".format(gps.speed()),
                "{:0.2f}".format(gps.heading()),
                "{:0.2f}".format(bme280.temp()),
                "{:0.2f}".format(bme280.humidity()),
                "{:0.5f}".format(bme280.pressure()),
                "{:0.2f}".format(bme280.altitude())]
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(data)

    time.sleep(2) """

gps = GPSUltimate()
pictureCapturer = PictureCapturer(5, gps)
pictureCapturer.start_capturing()
time.sleep(20)
pictureCapturer.stop_capturing(gps.altitude())
