from altitude_measurable import AltitudeMeasurable
import time
import threading
import board
import busio
import adafruit_bme280

class BME280(AltitudeMeasurable):
    """Provides temperature, pressure and humidity from BME280-sensor
    https://www.adafruit.com/product/2652
    https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout """

    # Create library object using Bus I2C port
    _i2c = busio.I2C(board.SCL, board.SDA)

    def __init__(self, sea_level_pressure=1013.25, address=0x77):
        """
        parameter sea_level_pressure: the current pressure (hPa) at sea-level for your current location. Used to calibre the altitude-barometer
        address=0x77 is default. address=0x76 alternative SDO to GND
        """
        
        self._bme280 = adafruit_bme280.Adafruit_BME280_I2C(self._i2c, address)
        self._bme280.sea_level_pressure = sea_level_pressure
        super().__init__()
        
        thread = threading.Thread(target=self._start)
        thread.start()
        

    def temp(self):
        return self._bme280.temperature

    def humidity(self):
        return self._bme280.humidity

    def pressure(self):
        return self._bme280.pressure

    def _altitude(self):
        return self._bme280.altitude
    
    @classmethod
    def pressureStatic(cls, address=0x77):
        """pressure of default (0x77) sensor"""
        bme280Tmp = adafruit_bme280.Adafruit_BME280_I2C(cls._i2c, address)
        return bme280Tmp.pressure
    


# bme280 = BME280(1013.25, 0x76)
# while True:
#    print("\nTemperature: %0.2f C" % bme280.temp())
#    print("Humidity: %0.3f %%" % bme280.humidity())
#    print("PressureStatic: %0.5f hPa" % bme280.pressureStatic(0x76))
#    print("Pressure: %0.5f hPa" % bme280.pressure())
#    print("Altitude = %0.2f meters" % bme280.altitude())
#    time.sleep(2)