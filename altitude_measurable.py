import time
import logging

class AltitudeMeasurable:
    """Abstract base-class for sensors which can report altitude. Clients can register on several events, reltated to the altitude"""
    
    
    
    def __init__(self):
        
        self._logger = logging.getLogger(type(self).__name__)
        
        self._is_ascending = None
        self._landing_time = None
        self._landing_altitude = None
    
        self._current_altitude = None
        self._current_altitude = self._altitude()
    
        self._N = 5 # nbr of elements to calculate moving-avg
    
        # observers are notified when some events occurs
    
        # dictionary: map altitude -> callback
        self._observers_fall_below = {}
    
        # dictionary: map altitude -> callback
        self._observers_rise_above = {}
    
        self._observers_burst = []
    
        self._observers_landed = []
        
    
    def _altitude():
        """overriden by subclass"""
        pass
    
    
    def _start(self):
        altitude_diffs = []

        while True:
            prev_is_ascending = self._is_ascending

            last_altitude = self._current_altitude
            self._current_altitude = self._altitude()

            altitude_diffs.append(self._current_altitude - last_altitude)
            altitude_diffs = altitude_diffs[-1 * self._N:] # only keep N-last elements
            moving_avg = self._moving_avg(altitude_diffs)
            if moving_avg >= 2:
                self._is_ascending = True
            elif moving_avg <= -2:
                self._is_ascending = False
            else:
                self._is_ascending = None # undefined, probably by starting-place or after landing

            if prev_is_ascending != self._is_ascending:
                self._logger.info("Altitude: %.2f. State change from is_ascending %s to %s", self._current_altitude, str(prev_is_ascending), str(self._is_ascending))

            if prev_is_ascending == True and self._is_ascending != True:
                self._logger.info("Altitude: %.2f. Burst!", self._current_altitude)
                observersCopy = self._observers_burst.copy()
                for callback in self._observers_burst:
                    callback(self._current_altitude)
                    # clear registered callback. Sending event only once!
                    observersCopy.remove(callback)
                    
                self._observers_burst = observersCopy
                    
            observersCopy = self._observers_rise_above.copy()
            for altitude_key in list(filter(lambda x: self._current_altitude > x and self._is_ascending == True, self._observers_rise_above.keys())):
                callback = self._observers_rise_above[altitude_key]
                callback(self._current_altitude)
                # clear registered callback. Sending event only once!
                observersCopy.pop(altitude_key)
                
            self._observers_rise_above = observersCopy
                    
            observersCopy = self._observers_fall_below.copy()
            for altitude_key in list(filter(lambda x: self._current_altitude < x and self._is_ascending == False, self._observers_fall_below.keys())):
                callback = self._observers_fall_below[altitude_key]
                callback(self._current_altitude)
                # clear registered callback. Sending event only once!
                observersCopy.pop(altitude_key)
                
            self._observers_fall_below = observersCopy
                
            if prev_is_ascending == False and self._is_ascending == None:
                self._logger.info("Altitude: %.2f. Landed.", self._current_altitude)
                self._landing_altitude = self._current_altitude
                observersCopy = self._observers_landed.copy()
                for callback in self._observers_landed:
                    callback(self._landing_altitude)
                    # clear registered callback. Sending event only once!
                    observersCopy.remove(callback)
                    
                self._observers_landed = observersCopy

            time.sleep(0.0001)
            
      
    def altitude(self):
        return self._current_altitude
            
    def landing_time(self):
        return self._landing_time

    def landing_altitude(self):
        return self._landing_altitude
    
    def subscribe_rise_above(self, altitude, callback):
        self._observers_rise_above.update({altitude: callback})
            
    def subscribe_burst(self, callback):
        self._observers_burst.append(callback)
    
    def subscribe_fall_below(self, altitude, callback):
        self._observers_fall_below.update({altitude: callback})
        
    def subscribe_landed(self, callback):
        self._observers_landed.append(callback)
        
    
    def _moving_avg(self, mylist):
        if len(mylist) < self._N:
            return 0

        cumsum = [0]

        for i, x in enumerate(mylist, 1):
            cumsum.append(cumsum[i-1] + x)
            if i>=self._N:
                moving_ave = (cumsum[i] - cumsum[i - self._N]) / self._N
                #can do stuff with moving_ave here
                #moving_aves.append(moving_ave)

        return moving_ave
    