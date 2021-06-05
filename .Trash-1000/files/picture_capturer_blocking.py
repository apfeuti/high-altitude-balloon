import time
from datetime import datetime
import multiprocessing
import logging
#from exif import Image
from picamera import PiCamera


class PictureCapturer:
    """ Takes pictures with the pi-camera """

    def __init__(self, capturing_frequency_sec):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._capturing_frequency_sec = capturing_frequency_sec
        self._stop_capturing = False
        self._camera_warmup_sec = 1

    def start_capturing(self):
        self._logger.info("Start capturing pictures with frequency %f sec", self._capturing_frequency_sec)

        # Threading and multiprocessing does not work with picamera. For some reason the whole raspberry freezes after ca 20 minutes.
        # Caution: This is blocking!
        while self._stop_capturing == False:
            with PiCamera() as camera:
                camera.resolution = (2592, 1944)
                time.sleep(self._camera_warmup_sec)
                filename = './data/pictures/hab-{}.jpg'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                camera.capture(filename)
            
            time.sleep(self._capturing_frequency_sec - self._camera_warmup_sec - 1)  #-1, ca time to take the picture

        self._logger.info("Stopped capturing pictures")
        
    def stop_capturing(self, landing_altitude):
        self._logger.info("Stop capturing pictures at altitude {}".format(landing_altitude))
        self._stop_capturing = True

            