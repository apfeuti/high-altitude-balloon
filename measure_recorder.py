import time
import threading
import csv
import os.path
import datetime

class MeasureRecorder:
    """Records the measures and writes the to csv-file"""
    
    def __init__(self, data_file, measure_frequency_sec, board, gps, bme280InCapsule, bme280Outside):
        self._data_file = data_file
        self._measure_frequency_sec = measure_frequency_sec
        self._board = board
        self._gps = gps
        self._bme280InCapsule = bme280InCapsule
        self._bme280Outside = bme280Outside
        
    def start_measures(self):
        thread = threading.Thread(target=self._start)
        thread.start()
        
    
    
    def _start(self):
        if not os.path.exists(self._data_file):
            header = ["time_utc", "board_temp", "board_volts_core", "board_volts_sdram_c", "board_volts_sdram_i", "board_volts_sdram_p", "board_throttled",
                "gps_utc", "gps_latitude", "gps_longitude", "gps_altitude", "gps_speed", "gps_heading",
                "capsule_temp", "capsule_humidity", "capsule_pressure", "capsule_baro_altitude",
                "out_temp", "out_humidity", "out_pressure", "out_baro_altitude"]
            with open(self._data_file, 'wt') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(header)
        
        while (True):
            with open(self._data_file, 'a') as csvfile:
                now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(timespec='milliseconds')
                data = [now,
                        self._board.temp(),
                        self._board.volt_core(),
                        self._board.volt_sdram_c(),
                        self._board.volt_sdram_i(),
                        self._board.volt_sdram_p(),
                        self._board.throttled(),                  #0x5 means: under voltage, currently throttled. See https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=147781&start=50#p972790
                        time.strftime('%Y-%m-%dT%H:%M:%SZ', self._gps.utc()),
                        "{:0.6f}".format(self._gps.latitude()),
                        "{:0.6f}".format(self._gps.longitude()),
                        "{:0.2f}".format(self._gps.altitude()),
                        #"{:0.2f}".format(self._gps.ascending_rate()),
                        "{:0.2f}".format(self._gps.speed()),
                        "{:0.2f}".format(self._gps.heading()),
                        "{:0.2f}".format(self._bme280InCapsule.temp()),
                        "{:0.2f}".format(self._bme280InCapsule.humidity()),
                        "{:0.5f}".format(self._bme280InCapsule.pressure()),
                        "{:0.2f}".format(self._bme280InCapsule.altitude()),
                        "{:0.2f}".format(self._bme280Outside.temp()),
                        "{:0.2f}".format(self._bme280Outside.humidity()),
                        "{:0.5f}".format(self._bme280Outside.pressure()),
                        "{:0.2f}".format(self._bme280Outside.altitude())
                        ]
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(data)

            time.sleep(self._measure_frequency_sec)
        
        