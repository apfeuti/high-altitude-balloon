import os

class Board:
    """Provides temperature and voltages from the Raspberry PI board (values from operating-system)"""

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

    def _volt(self, type):
        volt = os.popen("vcgencmd measure_volts core").readline()
        return float(volt.replace("volt=","").replace("V",""))