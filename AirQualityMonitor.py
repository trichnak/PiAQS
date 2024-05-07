# This script adapted from https://github.com/rydercalmdown/pi_air_quality_monitor.git AirQualityMonitor.py

import os
import datetime
import serial
import redis
import aqi

redis_client = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)


class AirQualityMonitor():

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0')

    def get_measurement(self):
        self.data = []
        for index in range(0,10):
            datum = self.ser.read()
            self.data.append(datum)
        self.pmtwo = int.from_bytes(b''.join(self.data[2:4]), byteorder='little') / 10
        self.pmten = int.from_bytes(b''.join(self.data[4:6]), byteorder='little') / 10
        myaqi = aqi.to_aqi([(aqi.POLLUTANT_PM25, str(self.pmtwo)),
                            (aqi.POLLUTANT_PM10, str(self.pmten))])
        self.aqi = float(myaqi)

        self.meas = {
            "timestamp": datetime.datetime.now(),
            "pm2.5": self.pmtwo,
            "pm10": self.pmten,
            "aqi": self.aqi,
    }
        
        return self.meas