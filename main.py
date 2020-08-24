from raspi_board import Board
from bme280 import BME280
from gps import GPS
from measure_recorder import MeasureRecorder
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
gps = GPS()
bme280 = BME280(1013.25)

measureRecorder = MeasureRecorder('measures.csv', 2, board, gps, bme280)
measureRecorder.start_measures()

# init wifi
board.disableWifi(gps.altitude())
board.enableWifi(gps.altitude())

# register listeners on events
gps.subscribe_rise_above(4000, board.disableWifi)
gps.subscribe_fall_below(4000, board.enableWifi)



