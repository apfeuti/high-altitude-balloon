import time
from datetime import datetime
import threading
import logging
import piexif
from fractions import Fraction
from picamera import PiCamera


class PictureCapturer:
    """ Takes pictures with the pi-camera """

    def __init__(self, capturing_frequency_sec, gps):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._capturing_frequency_sec = capturing_frequency_sec
        self._gps = gps
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
                    
                    altitude = self._gps.altitude()
                    altitude = altitude if altitude != None else 0
                    filename = './data/pictures/hab_{}_{}.jpg'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), int(altitude))
                    
                    camera.capture(filename)

                    lat = self._gps.latitude()
                    lat = lat if lat != None else 0

                    lng = self._gps.longitude()
                    lng = lng if lng != None else 0

                    utc = self._gps.utc()
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%SZ', utc) if utc != None else None
                    self._addGpsExif(filename, lat, lng, altitude, timestamp)
            except:
                self._logger.exception("Exception in picture_capture-loop")
            
            time.sleep(self._capturing_frequency_sec - self._camera_warmup_sec - 1)  #-1, ca time to take the picture

        self._logger.info("Stopped capturing pictures")
        
    def stop_capturing(self, landing_altitude):
        self._logger.info("Stop capturing pictures at altitude {}".format(landing_altitude))
        self._stop_capturing = True

    # taken from https://gist.github.com/c060604/8a51f8999be12fc2be498e9ca56adc72
    def _addGpsExif(self, file_name, lat, lng, altitude, timestamp):
        """Adds GPS position as EXIF metadata
        Keyword arguments:
        file_name -- image file
        lat -- latitude (as float)
        lng -- longitude (as float)
        altitude -- altitude (as float)
        """
        lat_deg = self._to_deg(lat, ["S", "N"])
        lng_deg = self._to_deg(lng, ["W", "E"])

        exiv_lat = (self._change_to_rational(lat_deg[0]), self._change_to_rational(lat_deg[1]), self._change_to_rational(lat_deg[2]))
        exiv_lng = (self._change_to_rational(lng_deg[0]), self._change_to_rational(lng_deg[1]), self._change_to_rational(lng_deg[2]))

        gps_ifd = {
            piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
            piexif.GPSIFD.GPSAltitudeRef: 0 if altitude >= 0 else 1,
            piexif.GPSIFD.GPSAltitude: self._change_to_rational(round(altitude)),
            piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
            piexif.GPSIFD.GPSLatitude: exiv_lat,
            piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
            piexif.GPSIFD.GPSLongitude: exiv_lng,
        }

        exif_dict = {"GPS": gps_ifd}
        
        # taken from https://stackoverflow.com/questions/33031663/how-to-change-image-captured-date-in-python
        if timestamp != None:
            t1 = {'0th': {
                    piexif.ImageIFD.DateTime: timestamp
                }
            }

            t2 = {'Exif': {
                    piexif.ExifIFD.DateTimeOriginal: timestamp,
                    piexif.ExifIFD.DateTimeDigitized: timestamp,
                }
            }

            exif_dict.update(t1)
            exif_dict.update(t2)

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, file_name)

    def _to_deg(self, value, loc):
        """convert decimal coordinates into degrees, munutes and seconds tuple
        Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
        return: tuple like (25, 13, 48.343 ,'N')
        """
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg =  int(abs_value)
        t1 = (abs_value-deg)*60
        min = int(t1)
        sec = round((t1 - min)* 60, 5)
        return (deg, min, sec, loc_value)


    def _change_to_rational(self, number):
        """convert a number to rantional
        Keyword arguments: number
        return: tuple like (1, 2), (numerator, denominator)
        """
        f = Fraction(str(number))
        return (f.numerator, f.denominator)

            