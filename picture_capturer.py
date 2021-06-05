import time
from datetime import datetime
import threading
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
        self._stop = False
        thread = threading.Thread(target=self._start, name="PictureCapturerThread")
        thread.start()


    def _start(self):
        self._logger.info("Start capturing pictures with frequency %f sec", self._capturing_frequency_sec)

        while self._stop_capturing == False:
            try:
                with PiCamera() as camera:
                    camera.resolution = (2592, 1944)
                    time.sleep(self._camera_warmup_sec)
                    filename = './data/pictures/hab-{}.jpg'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                    camera.capture(filename)
            except:
                self._logger.exception("Exception in picture_capture-loop")
            
            time.sleep(self._capturing_frequency_sec - self._camera_warmup_sec - 1)  #-1, ca time to take the picture

        self._logger.info("Stopped capturing pictures")
        
    def stop_capturing(self, landing_altitude):
        self._logger.info("Stop capturing pictures at altitude {}".format(landing_altitude))
        self._stop_capturing = True

            