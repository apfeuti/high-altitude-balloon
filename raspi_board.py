import os
import logging

class Board:
    """Provides temperature and voltages from the Raspberry PI board (values from operating-system)"""

    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)

    def temp(self):
        temp = os.popen("vcgencmd measure_temp").readline()
        return float(temp.replace("temp=","").replace("'C",""))

    def volt_core(self):
        return self._volt("core")

    def volt_sdram_c(self):
        return self._volt("sdram_c")

    def volt_sdram_i(self):
        return self._volt("sdram_i")

    def volt_sdram_p(self):
        return self._volt("sdram_p")
    
    def throttled(self):
        throttled = os.popen("vcgencmd get_throttled").readline()
        return throttled.replace("throttled=","").replace("\n","")

    def disableWifi(self, altitude):
        self._logger.info("Disabling Wifi at altitude: " + str(altitude))
        #self._logger.info(os.popen("sudo wpa_cli terminate").readline())
        self._logger.info(os.popen("sudo ifconfig wlan0 down").readline())

    def enableWifi(self, altitude):
        self._logger.info("Enabling Wifi at altitude: " + str(altitude))
        self._logger.info(os.popen("sudo iwconfig wlan0 mode ad-hoc channel 1 essid high-alt-balloon").readline())
        self._logger.info(os.popen("sudo ifconfig wlan0 up").readline())

    def _volt(self, type):
        volt = os.popen("vcgencmd measure_volts " + type).readline()
        return float(volt.replace("volt=","").replace("V",""))