import datetime
from queue import Queue
from AirQualityMonitor import AirQualityMonitor
import pickle
import csv

DATA_MAXLEN = 60 # data collection every 10 seconds, save data from past 10 minutes
MINUTE_MAXLEN = 60 # save data from past hour
HOUR_MAXLEN = 24 # save data from past day
DAY_MAXLEN = 7 # save data from past week

DATA_FILE = 'figures/data_entries.csv'
MINUTE_FILE = 'figures/minute_avg.csv'
HOUR_FILE = 'figures/hour_avg.csv'
DAY_FILE = 'figures/day_avg.csv'

class AQMController():
    def __init__(self):
        self.data_entries = [] 
        self.minute_avg = []
        self.hour_avg = []
        self.day_avg = [] 
        self.running = True
        self.aqm = AirQualityMonitor()

        self.load_data()

    def load_data(self):
        with open(MINUTE_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            self.minute_avg = [row for row in csv_reader]
        # print("Loading data from", MINUTE_FILE)
        # print("Loaded Data: ", self.minute_avg)

        with open(HOUR_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            self.hour_avg = [row for row in csv_reader]
        # print("Loading data from", HOUR_FILE)
        # print("Loaded Data: ", self.hour_avg)
        

        with open(DAY_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            self.day_avg = [row for row in csv_reader]
        # print("Loading data from", DAY_FILE)
        # print("Loaded Data: ", self.day_avg)

    def write_data(self, file, data):
        # print("Writing data to ", file)
        with open(file, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, 
                                fieldnames=data[0].keys(),

                            )
            fc.writeheader()
            fc.writerows(data)

    def calculate_avg(self, data_to_avg, data_to_avg_maxlen, data_storage, data_storage_maxlen):
        pm25 = pm10 = aqi = 0
        try:
            for entry in data_to_avg:
                pm25 += entry['pm2.5']
                pm10 += entry['pm10']
                aqi += entry['aqi']
        except TypeError:
            return

        avg = {
            "timestamp": datetime.datetime.now(),
            "pm2.5": pm25/data_to_avg_maxlen,
            "pm10": pm10/data_to_avg_maxlen,
            "aqi": aqi/data_to_avg_maxlen,
        }
        if len(data_storage) == data_storage_maxlen:
            data_storage.pop(0)
        data_storage.append(avg)

        return data_storage

    def controller(self):
        while self.running:
            current_time = datetime.datetime.now()
            
            if current_time.second % 10 == 0 and current_time.microsecond < 100: # ten second interval 
            # if current_time.microsecond < 100:
                if len(self.data_entries) == DATA_MAXLEN:
                    self.data_entries.pop(0)
                self.data_entries.append(self.aqm.get_measurement())
                self.write_data(DATA_FILE,self.data_entries)

                if current_time.second == 0 and len(self.data_entries) == DATA_MAXLEN: # one minute interval
                    print("Minute")
                    self.minute_avg = self.calculate_avg(self.data_entries, DATA_MAXLEN, self.minute_avg, MINUTE_MAXLEN)
                    self.write_data(MINUTE_FILE,self.minute_avg)

                    if current_time.minute == 0 and len(self.minute_avg) == MINUTE_MAXLEN: # one hour interval
                        print("Hour")
                        self.hour_avg = self.calculate_avg(self.minute_avg, MINUTE_MAXLEN, self.hour_avg, HOUR_MAXLEN)
                        self.write_data(HOUR_FILE,self.hour_avg)

                        if current_time.hour == 0 and len(self.hour_avg) == HOUR_MAXLEN: # one day interval
                            print("Day")
                            self.day_avg = self.calculate_avg(self.hour_avg, HOUR_MAXLEN, self.day_avg, DAY_MAXLEN)
                            self.write_data(DAY_FILE,self.day_avg)

# AQMController()