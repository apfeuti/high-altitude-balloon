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
    _bme280 = adafruit_bme280.Adafruit_BME280_I2C(_i2c)

    def __init__(self, sea_level_pressure=1013.25):
        """
        parameter sea_level_pressure: the current pressure (hPa) at sea-level for your current location. Used to calibre the altitude-barometer
        """
        
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
    


#bme280 = BME280(1013.25)
#while True:
#    print("\nTemperature: %0.2f C" % bme280.temp())
#    print("Humidity: %0.3f %%" % bme280.humidity())
#    print("Pressure: %0.5f hPa" % bme280.pressure())
#    print("Altitude = %0.2f meters" % bme280.altitude())
#    time.sleep(2)