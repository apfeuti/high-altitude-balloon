from altitude_measurable import AltitudeMeasurable
import threading
import random
import datetime
import time

class GPSMock(AltitudeMeasurable):
    """Provides measures about GPS-positioning"""

    _ascending_rate = 5 # m/s
    
    _start_altitude = 451

    _current_altitude = None

    _prev_time = None

    _counter = 0

    def __init__(self):
        super().__init__()
        thread = threading.Thread(target=self._start, name="GPSMockThread")
        thread.start()


    def altitude(self):
        # simulate no fix
        self._counter += 1
        if (self._counter < 10):
            return None
        elif (self._counter == 10):
            self._prev_time = datetime.datetime.utcnow()

        if (self._current_altitude == None):
            self._current_altitude = self._start_altitude
            return self._current_altitude
        
        time_factor = 1 # simulation is x time faster than reality
        jitter = random.uniform(-2.0, 2.0)
        landing_altitude = 700
        burst_altitude = 34000

        if self._landing_time == None:
            seconds_since_prev = (datetime.datetime.utcnow() - self._prev_time).total_seconds()
            self._current_altitude = self._current_altitude + seconds_since_prev * (self._ascending_rate + jitter) * time_factor

            if self._current_altitude <= landing_altitude and self._is_ascending == False:
                self._landing_time = datetime.datetime.utcnow()
        else:
            self._current_altitude = self._current_altitude + jitter

        if self._current_altitude >= burst_altitude and self._ascending_rate > 0:
            self._ascending_rate *= -1

        self._prev_time = datetime.datetime.utcnow()
        return self._current_altitude
    

    def latitude(self):
        return 47.0746

    def longitude(self):
        return 7.3077

    def speed(self):
        return 57.834

    def heading(self):
        return 257.334

    def utc(self):
        return time.gmtime()
