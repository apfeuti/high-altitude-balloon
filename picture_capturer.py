import time
import datetime
import threading
import logging
from exif import Image
from picamera import PiCamera


class PictureCapturer:
    """ Takes pictures with the pi-camera """

    def __init__(self, capturing_frequency_sec):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._camera = PiCamera()
        self._camera.resolution = (2592, 1944)
        self._capturing_frequency_sec = capturing_frequency_sec
        self._stop = False

    def start_capturing(self):
        self._stop = False
        self._logger.info("Start capturing pictures with frequency %f sec", self._capturing_frequency_sec)
        thread = threading.Thread(target=self._start)
        thread.start()

    def stop_capturing(self):
        self._stop = True
        self._logger.info("Stop capturing pictures")

    def _start(self):
        for filename in self._camera.capture_continuous('hab-{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
            #with open(filename, 'rb') as image_file:
            #    my_image = Image(image_file)
                #my_image.gps_latitude = '47.0'
                #my_image.gps_longitude = '7.2'
                #my_image.gps_altitude = '1380'
                # my_image.foo = 'bar'
                #my_image.model = "EXIF Package"
                #my_image.set("gps_altitude", "199.034")  # in meters
                #my_image.gps_altitude_ref = GpsAltitudeRef.ABOVE_SEA_LEVEL

            #with open(filename + '_exif', 'wb') as image_with_exif:
            #    image_with_exif.write(my_image.get_file())

            time.sleep(self._capturing_frequency_sec)
            if self._stop:
                break
