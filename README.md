Group Members: Tanner Richnak

Goal of the project: Use a Raspberry Pi 3 to build an air quality monitor and build a python app that receives data from the Raspberry Pi over a local network.  Display options: Live data feed with data from the past ten minutes, average measurement over a minute for the past hour, average measurement over an hour for the past day, average measurement over a day for the past week.

Details of Code:
    How to run: Run server.py on Raspberry Pi and client.py on host machine.
    Required libraries:
        pygame
        matplotlib
        datetime
        csv
        _thread
        numpy
        pickle
        socket
        serial
        redis
        aqi
    Environment: 
        Raspberry Pi 3: Ubuntu 20.04, Python 3.8.10
            SDS011 Sensor
        Host Machine: Ubuntu 20.04, Python 3.8.10
    Input/Output:
        No input required
        Outputs .csv files of collected data as well as line graph visualizations of collected data
            Note legend on graphs:
                AQI - Air Quality Index
                PM 2.5 - parts per million < 2.5 µm
                PM 10 - parts per million < 10 µm
    Extra comments:
        Important: Make sure to replace server IP address in server.py (line 6) and network.py (line 8) to your local raspberry pi IP address.