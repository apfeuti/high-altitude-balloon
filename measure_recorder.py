import time
import threading
import csv
import os.path
import datetime
import logging

class MeasureRecorder:
    """Records the measures and writes the to csv-file"""
    
    def __init__(self, data_file, measure_frequency_sec, board, gps, bme280InCapsule, bme280Outside):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._data_file = data_file
        self._measure_frequency_sec = measure_frequency_sec
        self._board = board
        self._gps = gps
        self._bme280InCapsule = bme280InCapsule
        self._bme280Outside = bme280Outside
        
    def start_measures(self):
        thread = threading.Thread(target=self._start, name="MeasurerRecorderThread")
        thread.start()
        
    
    
    def _start(self):
        if not os.path.exists(self._data_file):
            header = ["time_utc", "board_temp", "board_volts_core", "board_volts_sdram_c", "board_volts_sdram_i", "board_volts_sdram_p", "board_throttled",
                "gps_utc", "gps_latitude", "gps_longitude", "gps_altitude", "gps_speed_km/h", "gps_heading", "gps_ascending_rate_m/s",
                "capsule_temp", "capsule_humidity", "capsule_pressure", "capsule_baro_altitude", "capsule_ascending_rate_m/s",
                "out_temp", "out_humidity", "out_pressure", "out_baro_altitude", "out_ascending_rate_m/s"]
            with open(self._data_file, 'wt') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(header)
        
        while (True):
            try:
                with open(self._data_file, 'a') as csvfile:
                    startSample = datetime.datetime.utcnow()

                    gps_time = "n/a"
                    gps_latitude = 0
                    gps_longitude = 0
                    gps_altitude = 0
                    gps_speed = 0
                    gps_heading = 0
                    gps_ascending_rate = 0
                    try:
                        gps_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', self._gps.utc())
                        gps_latitude = self._gps.latitude()
                        gps_longitude = self._gps.longitude()
                        gps_altitude = self._gps.altitude()
                        gps_speed = self._gps.speed()
                        gps_heading = self._gps.heading()
                        gps_ascending_rate = self._gps.ascending_rate()
                    except:
                        self._logger.exception("Error reading gps-sensor")


                    capsule_temp = 0
                    capsule_humidity = 0
                    capsule_pressure = 0
                    capsule_altitude = 0
                    capsule_ascending_rate = 0
                    try:
                        capsule_temp = self._bme280InCapsule.temp()
                        capsule_humidity = self._bme280InCapsule.humidity()
                        capsule_pressure = self._bme280InCapsule.pressure()
                        capsule_altitude = self._bme280InCapsule.altitude()
                        capsule_ascending_rate = self._bme280InCapsule.ascending_rate()
                    except:
                        self._logger.exception("Error reading capsule-bme280-sensor")

                    
                    outside_temp = 0
                    outside_humidity = 0
                    outside_pressure = 0
                    outside_altitude = 0
                    outside_ascending_rate = 0
                    try:
                        outside_temp = self._bme280Outside.temp()
                        outside_humidity = self._bme280Outside.humidity()
                        outside_pressure = self._bme280Outside.pressure()
                        outside_altitude = self._bme280Outside.altitude()
                        outside_ascending_rate = self._bme280Outside.ascending_rate()
                    except:
                        self._logger.exception("Error reading outside-bme280-sensor")

                    data = [startSample.replace(tzinfo=datetime.timezone.utc).isoformat(timespec='milliseconds'),
                            self._board.temp(),
                            self._board.volt_core(),
                            self._board.volt_sdram_c(),
                            self._board.volt_sdram_i(),
                            self._board.volt_sdram_p(),
                            self._board.throttled(),                  #0x5 means: under voltage, currently throttled. See https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=147781&start=50#p972790
                            gps_time,
                            "{:0.6f}".format(gps_latitude),
                            "{:0.6f}".format(gps_longitude),
                            "{:0.2f}".format(gps_altitude),
                            "{:0.2f}".format(gps_speed),
                            "{:0.2f}".format(gps_heading),
                            "{:0.2f}".format(gps_ascending_rate),
                            "{:0.2f}".format(capsule_temp),
                            "{:0.2f}".format(capsule_humidity),
                            "{:0.5f}".format(capsule_pressure),
                            "{:0.2f}".format(capsule_altitude),
                            "{:0.2f}".format(capsule_ascending_rate),
                            "{:0.2f}".format(outside_temp),
                            "{:0.2f}".format(outside_humidity),
                            "{:0.5f}".format(outside_pressure),
                            "{:0.2f}".format(outside_altitude),
                            "{:0.2f}".format(outside_ascending_rate)
                            ]
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(data)
                    endSample = datetime.datetime.utcnow()
                    timeToReadSensors = (endSample - startSample).total_seconds()
                    sleepTime = self._measure_frequency_sec
                    if (timeToReadSensors < self._measure_frequency_sec):
                        sleepTime -= timeToReadSensors

            except:
                self._logger.exception("Exception in measure_recorder-loop")

            time.sleep(sleepTime)
        
        