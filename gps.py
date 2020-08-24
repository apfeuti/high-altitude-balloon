from altitude_measurable import AltitudeMeasurable
import threading
import random
import datetime

class GPS(AltitudeMeasurable):
    """Provides measures about GPS-positioning"""

    _ascending_rate = 5 # m/s
    
    _start_altitude = 440

    def __init__(self):
        super().__init__()
        thread = threading.Thread(target=self._start)
        thread.start()


    def _altitude(self):
        if (self._current_altitude == None):
            return self._start_altitude
        
        cycle_time = 20 # second
        jitter = random.uniform(-2.0, 2.0)
        landing_altitude = 700
        burst_altitude = 34000

        if self._landing_time == None:
            altitude = self._current_altitude + cycle_time * (self._ascending_rate + jitter)

            if self._current_altitude <= landing_altitude and self._is_ascending == False:
                self._landing_time = datetime.datetime.utcnow()
        else:
            altitude = self._current_altitude + jitter

        if altitude >= burst_altitude:
            self._ascending_rate *= -1

        return altitude
    

    def ascending_rate(self):
        return self._ascending_rate

    def latitude(self):
        return 47.0746

    def longitude(self):
        return 7.3077

    def speed(self):
        return 57.834

    def heading(self):
        return 257.334


# gps = GPS()