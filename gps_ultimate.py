from altitude_measurable import AltitudeMeasurable
import serial
import threading
import adafruit_gps


class GPSUltimate(AltitudeMeasurable):
    """Reads the GPS-Sensor
    https://www.adafruit.com/product/746
    https://learn.adafruit.com/adafruit-ultimate-gps/overview
    """

    def __init__(self):

        # Create a serial connection for the GPS connection using default speed and
        # a slightly higher timeout (GPS modules typically update once a second).
        # These are the defaults you should use for the GPS FeatherWing.
        # For other boards set RX = GPS module TX, and TX = GPS module RX pins.
        #uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

        # for a computer, use the pyserial library for uart access
        self._uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)

        # If using I2C, we'll create an I2C interface to talk to using default pins
        #i2c = board.I2C()

        # Create a GPS module instance.
        self._gps = adafruit_gps.GPS(self._uart, debug=False)  # Use UART/pyserial
        #gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

        # Initialize the GPS module by changing what data it sends and at what rate.
        # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
        # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
        # the GPS module behavior:
        #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

        # Turn on the basic GGA and RMC info (what you typically want)
        self._gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Turn on just minimum info (RMC only, location):
        # gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything:
        # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on everything (not all of it is parsed!)
        # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

        # Set update rate to once a second (1hz) which is what you typically want.
        self._gps.send_command(b"PMTK220,1000")
        # Or decrease to once every two seconds by doubling the millisecond value.
        # Be sure to also increase your UART timeout above!
        # gps.send_command(b'PMTK220,2000')
        # You can also speed up the rate, but don't go too fast or else you can lose
        # data during parsing.  This would be twice a second (2hz, 500ms delay):
        # gps.send_command(b'PMTK220,500')

        super().__init__()
        thread = threading.Thread(target=self._start, name="GPSUltimateThread")
        thread.start()

    def altitude(self):
        self._gps.update()
        return self._gps.altitude_m

    def latitude(self):
        self._gps.update()
        return self._gps.latitude

    def longitude(self):
        self._gps.update()
        return self._gps.longitude

    def speed(self):
        """km/h over ground """
        self._gps.update()
        return self._gps.speed_knots * 1.852 # knots (nautic-mile / h) to km/h

    def heading(self):
        self._gps.update()
        return self._gps.track_angle_deg

    def utc(self):
        self._gps.update()
        return self._gps.timestamp_utc

    def has_3d_fix(self):
        self._gps.update()
        return self._gps.has_3d_fix
