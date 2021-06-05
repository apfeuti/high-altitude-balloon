import time
import datetime
import logging

class AltitudeMeasurable:
    """Abstract base-class for sensors which can report altitude. Clients can register on several events, related to the altitude"""
    
    
    def __init__(self):
        
        self._logger = logging.getLogger(type(self).__name__)
        
        self._is_ascending = None
        self._landing_time = None
        self._landing_altitude = None
    
        self._ascending_rates = [0]
    
        self._N = 5 # nbr of elements to calculate moving-avg for ascending-rate
    
        # observers are notified when some events occurs
    
        # dictionary: map altitude -> callback
        self._observers_fall_below = {}
    
        # dictionary: map altitude -> callback
        self._observers_rise_above = {}
    
        self._observers_burst = []
    
        self._observers_landed = []
        
    
    def altitude():
        """overriden by subclass"""
        pass
    
    
    def _start(self):
        prev_altitude = None
        prev_time = datetime.datetime.utcnow()

        while True:
            try:
                prev_is_ascending = self._is_ascending

                current_altitude = self.altitude()

                now = datetime.datetime.utcnow()
                seconds_since_prev = (now - prev_time).total_seconds()
                prev_time = now

                if not current_altitude is None and not prev_altitude is None:
                    if (seconds_since_prev > 0):
                        current_ascending_rate = (current_altitude - prev_altitude) / seconds_since_prev # m/s : > 0 ascending, < 0 descending
                    else:
                        current_ascending_rate = 0

                    self._ascending_rates.append(current_ascending_rate)
                    self._ascending_rates = self._ascending_rates[-1 * self._N:] # only keep N-last elements
                    moving_avg = self._moving_avg(self._ascending_rates)
                    if moving_avg >= 1: # m/s
                        self._is_ascending = True
                    elif moving_avg <= -1:
                        self._is_ascending = False
                    else:
                        self._is_ascending = None # undefined, probably by starting-place or after landing

                    if prev_is_ascending != self._is_ascending:
                        self._logger.info("Altitude: %.2f. State change from is_ascending %s to %s", current_altitude, str(prev_is_ascending), str(self._is_ascending))

                    if prev_is_ascending == True and self._is_ascending != True:
                        self._logger.info("Altitude: %.2f. Burst!", current_altitude)
                        observersCopy = self._observers_burst.copy()
                        for callback in self._observers_burst:
                            callback(current_altitude)
                            # clear registered callback. Sending event only once!
                            observersCopy.remove(callback)
                            
                        self._observers_burst = observersCopy
                            
                    observersCopy = self._observers_rise_above.copy()
                    for altitude_key in list(filter(lambda x: current_altitude > x and self._is_ascending == True, self._observers_rise_above.keys())):
                        callback = self._observers_rise_above[altitude_key]
                        callback(current_altitude)
                        # clear registered callback. Sending event only once!
                        observersCopy.pop(altitude_key)
                        
                    self._observers_rise_above = observersCopy
                            
                    observersCopy = self._observers_fall_below.copy()
                    for altitude_key in list(filter(lambda x: current_altitude < x and self._is_ascending == False, self._observers_fall_below.keys())):
                        callback = self._observers_fall_below[altitude_key]
                        callback(current_altitude)
                        # clear registered callback. Sending event only once!
                        observersCopy.pop(altitude_key)
                        
                    self._observers_fall_below = observersCopy
                        
                    if prev_is_ascending == False and self._is_ascending == None:
                        self._landing_altitude = current_altitude
                        self._landing_time = now
                        self._logger.info("Altitude: %.2f. Landed.", self._landing_altitude)
                        observersCopy = self._observers_landed.copy()
                        for callback in self._observers_landed:
                            callback(self._landing_altitude)
                            # clear registered callback. Sending event only once!
                            observersCopy.remove(callback)
                            
                        self._observers_landed = observersCopy

                prev_altitude = current_altitude
            except:
                self._logger.exception("Exception in altitude_measurable-loop")
                
            time.sleep(2)
            
    def ascending_rate(self):
        return self._ascending_rates[-1] # last element is the most recent one

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

        return moving_ave
    