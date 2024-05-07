import datetime
from AirQualityMonitor import AirQualityMonitor 
import csv

# Define constants for maximum lengths of data lists
DATA_MAXLEN = 60  # Maximum length of data_entries list (10 minutes)
MINUTE_MAXLEN = 60  # Maximum length of minute_avg list (1 hour)
HOUR_MAXLEN = 24  # Maximum length of hour_avg list (1 day)
DAY_MAXLEN = 7  # Maximum length of day_avg list (1 week)

# Define file paths for storing data
DATA_FILE = 'figures/data_entries.csv'
MINUTE_FILE = 'figures/minute_avg.csv'
HOUR_FILE = 'figures/hour_avg.csv'
DAY_FILE = 'figures/day_avg.csv'

class AQMController():
    def __init__(self):
        # Initialize instance variables
        self.data_entries = []  # List to store data collected every 10 seconds
        self.minute_avg = []  # List to store minute-averaged data
        self.hour_avg = []  # List to store hour-averaged data
        self.day_avg = []  # List to store day-averaged data
        self.running = True  # Flag to indicate whether the controller is running
        self.aqm = AirQualityMonitor()  # Instance of AirQualityMonitor class

        # Load existing data from files into instance variables
        self.load_data() 

    def load_data(self):
        # Load data from files into instance variables using csv.DictReader
        with open(MINUTE_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            self.minute_avg = [row for row in csv_reader]

        with open(HOUR_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            self.hour_avg = [row for row in csv_reader]

        with open(DAY_FILE, 'r') as file:
            csv_reader = csv.DictReader(file)
            self.day_avg = [row for row in csv_reader]

    def write_data(self, file, data):
        # Write data to a file using csv.DictWriter
        try:
            with open(file, 'w', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file, 
                                    fieldnames=data[0].keys(),

                                )
                fc.writeheader()
                fc.writerows(data)
        except:
            pass

    def calculate_avg(self, data_to_avg, data_to_avg_maxlen, data_storage, data_storage_maxlen):
        # Calculate average of a list of data entries
        pm25 = pm10 = aqi = 0
        try:
            for entry in data_to_avg:
                pm25 += entry['pm2.5']
                pm10 += entry['pm10']
                aqi += entry['aqi']
        except TypeError:
            return

        if len(data_to_avg) < data_to_avg_maxlen:  # If data list is not at maximum length, use current length to calculate average
            averager = len(data_to_avg)
        else:
            averager = data_to_avg_maxlen

        avg = {
            "timestamp": datetime.datetime.now(),
            "pm2.5": pm25/averager,
            "pm10": pm10/averager,
            "aqi": aqi/averager,
        }

        try:
            if len(data_storage) == data_storage_maxlen:
                data_storage.pop(0)
            data_storage.append(avg)
        except:
            pass

        return data_storage

    def controller(self):
        # Main loop of the controller
        while self.running:
            current_time = datetime.datetime.now()
            
            if current_time.second % 10 == 0 and current_time.microsecond < 100:  # Check if it's a 10-second interval
                print("here")
                if len(self.data_entries) == DATA_MAXLEN:
                    self.data_entries.pop(0)
                    self.data_entries.append(self.aqm.get_measurement())
                    self.write_data(DATA_FILE,self.data_entries)

                    if current_time.second == 0:  # Check if it's a 1-minute interval
                        print(current_time.hour,':',current_time.minute)
                        self.minute_avg = self.calculate_avg(self.data_entries[-6:], DATA_MAXLEN, self.minute_avg, MINUTE_MAXLEN)
                        self.write_data(MINUTE_FILE,self.minute_avg)

                        if current_time.minute == 0:  # Check if it's a 1-hour interval
                            self.hour_avg = self.calculate_avg(self.minute_avg, MINUTE_MAXLEN, self.hour_avg, HOUR_MAXLEN)
                            self.write_data(HOUR_FILE,self.hour_avg)

                            if current_time.hour == 0:  # Check if it's a 1-day interval
                                self.day_avg = self.calculate_avg(self.hour_avg, HOUR_MAXLEN, self.day_avg, DAY_MAXLEN)
                                self.write_data(DAY_FILE,self.day_avg)