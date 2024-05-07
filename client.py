# Import necessary libraries
import pygame  # Library for game development
import matplotlib.pyplot as plt  # Library for creating static, animated, and interactive visualizations in python
from network import Network  # Custom library for network operations
import datetime  # Library for date and time operations
import csv  # Library for reading and writing CSV files
from _thread import *  # Library for threading operations
import numpy as np  # Library for numerical operations

# Define file paths for data and graphs
DATA_FILE = 'figures/data_entries.csv'  # File path for data entries
MINUTE_FILE = 'figures/minute_avg.csv'  # File path for minute average data
HOUR_FILE = 'figures/hour_avg.csv'  # File path for hour average data
DAY_FILE = 'figures/day_avg.csv'  # File path for day average data

DATA_GRAPH = 'figures/data_entries.png'  # File path for data graph
MINUTE_GRAPH = 'figures/minute_avg.png'  # File path for minute average graph
HOUR_GRAPH = 'figures/hour_avg.png'  # File path for hour average graph
DAY_GRAPH = 'figures/day_avg.png'  # File path for day average graph

# Define screen dimensions
SCREEN_WIDTH = 1080  # Screen width in pixels
SCREEN_HEIGHT = 720  # Screen height in pixels

# Define button dimensions
BUTTON_WIDTH = 150  # Button width in pixels
BUTTON_HEIGHT = 100  # Button height in pixels

# Define colors
BLACK = (0, 0, 0)  # RGB value for black color
WHITE = (255, 255, 255)  # RGB value for white color
GREEN = (0, 255, 0)  # RGB value for green color
BLUE = (0, 0, 255)  # RGB value for blue color
RED = (255, 0, 0)  # RGB value for red color
YELLOW = (255, 255, 0)  # RGB value for yellow color
LIME = (50, 205, 50)  # RGB value for lime color
ORANGE = (255, 165, 0)  # RGB value for orange color
GREY = (128, 128, 128)  # RGB value for grey color

# Initialize Pygame
pygame.init()  # Initialize Pygame modules
clock = pygame.time.Clock()  # Create a clock object to control the frame rate

# Define fonts
font = pygame.font.Font(None, 74)  # Create a font object with size 74
small_font = pygame.font.Font(None, 36)  # Create a font object with size 36

# Set up the display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the display mode with specified width and height
pygame.display.set_caption("Air Quality Monitor")  # Set the window title

# Create a Button class
class Button:
    def __init__(self, text, x, y, color):
        self.text = text  # Button text
        self.x = x  # Button x-coordinate
        self.y = y  # Button y-coordinate
        self.color = color  # Button color
        self.width = BUTTON_WIDTH  # Button width
        self.height = BUTTON_HEIGHT  # Button height

    # Method to draw the button on the screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))  # Draw a rectangle for the button
        font = pygame.font.SysFont("comicsans", 40)  # Create a font object for the button text
        text = small_font.render(self.text, 1, (0, 0, 0))  # Render the button text
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), (self.y + round(self.height / 2) - round(text.get_height() / 2))))  # Draw the button text on the screen

    # Method to check if the button has been clicked
    def click(self, pos):
        x1 = pos[0]  # Get the x-coordinate of the mouse click position
        y1 = pos[1]  # Get the y-coordinate of the mouse click position
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:  # Check if the click position is within the button area
            return True
        else:
            return False

# Create buttons for the main menu
main_btns = [Button("Live Data", SCREEN_WIDTH / 3 - BUTTON_WIDTH / 2, 2 * SCREEN_HEIGHT / 4 - BUTTON_HEIGHT / 2, YELLOW), 
             Button("Hour View", 2 * SCREEN_WIDTH / 3 - BUTTON_WIDTH / 2, 2 * SCREEN_HEIGHT / 4 - BUTTON_HEIGHT / 2, YELLOW), 
             Button("Day View", SCREEN_WIDTH / 3 - BUTTON_WIDTH / 2, 3 * SCREEN_HEIGHT / 4 - BUTTON_HEIGHT / 2, YELLOW), 
             Button("Week View", 2 * SCREEN_WIDTH / 3 - BUTTON_WIDTH / 2, 3 * SCREEN_HEIGHT / 4 - BUTTON_HEIGHT / 2, YELLOW)]  # Create a list of buttons for the main menu
back_btn = [Button("Back", SCREEN_WIDTH / 8 - BUTTON_WIDTH / 2, SCREEN_HEIGHT / 6 - BUTTON_HEIGHT / 2, YELLOW)]  # Create a button for going back

# Create a Client class
class Client():
    def __init__(self):
        self.client_no = None  # Client number
        self.network = Network()  # Network object
        self.data_entries = None  # Data entries
        self.minute_avg = None  # Minute average data
        self.hour_avg = None  # Hour average data
        self.day_avg = None  # Day average data
        self.last_step = datetime.datetime.now()  # Last step time
        self.current_step = None  # Current step time

    # Method to handle different menu options
    def menu_action(self, selected_option):
        try:
            if selected_option == "Live Data":
                print("Live Data selected")  # Print a message indicating that Live Data is selected
                self.display_live_data()  # Call the method to display live data
            elif selected_option == "Hour View": 
                print("Hour View selected")  # Print a message indicating that Hour View is selected
                self.display_hour_view()  # Call the method to display hour view
            elif selected_option == "Day View":
                print("Day View selected")  # Print a message indicating that Day View is selected
                self.display_day_view()  # Call the method to display day view
            elif selected_option == "Week View":
                print("Week View selected")  # Print a message indicating that Week View is selected
                self.display_week_view()  # Call the method to display week view
            elif selected_option == "Back":
                print("Back selected")  # Print a message indicating that Back is selected
                main()  # Call the main function
        except TypeError as e:
            print(e)  # Print any TypeError exceptions

    # Method to display live data
    def display_live_data(self):
        running = True
        while running:
            plt.clf()  # Clear the current figure
            clock.tick(60)  # Tick the clock to control the frame rate
            self.data_handler()  # Call the method to handle data

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in back_btn:
                        if btn.click(pos):        
                            client.menu_action(btn.text)

            # Initialize arrays to store data
            aqi = np.array([])  # Array to store AQI data
            pm25 = np.array([])  # Array to store PM2.5 data
            pm10 = np.array([])  # Array to store PM10 data
            timestamp = np.array([])  # Array to store timestamp data

            try:
                # Calculate time passed
                x = np.flip(np.array(range(len(self.data_entries))) * 10)  # Calculate the x-values for the plot

                # Extract data from entries
                for entry in self.data_entries:
                    aqi = np.append(aqi, float(entry['aqi']))  # Append AQI data to the array
                    pm25 = np.append(pm25, float(entry['pm2.5']))  # Append PM2.5 data to the array
                    pm10 = np.append(pm10, float(entry['pm10']))  # Append PM10 data to the array
                    timestamp = np.append(timestamp, entry['timestamp'])  # Append timestamp data to the array

                # Plot the data
                plt.plot(x, aqi, color='red')  # Plot AQI data
                plt.plot(x, pm25, color='green')  # Plot PM2.5 data
                plt.plot(x, pm10, color='blue')  # Plot PM10 data

                # Add labels and title
                plt.xlabel("Time Passed (seconds)")  # Set the x-axis label
                plt.ylabel("Data from past ten minutes")  # Set the y-axis label
                plt.title('Live Data')  # Set the title

                # Add legend
                plt.legend(["AQI", "PM 2.5", "PM 10"], loc="lower right")  # Add a legend to the plot

                # Save the plot
                plt.savefig(DATA_GRAPH)  # Save the plot to a file

                # Load the saved plot and redraw the window
                img = pygame.image.load(DATA_GRAPH).convert()  # Load the saved plot
                self.redrawWindow(back_btn, img=img)  # Redraw the window with the plot
                continue

            except:
                pass

            # Redraw the window with waiting message
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in back_btn:
                        if btn.click(pos):        
                            client.menu_action(btn.text)

            self.redrawWindow(back_btn, is_waiting=True)  # Redraw the window with a waiting message

    # Method to display hour view
    def display_hour_view(self):
        running = True
        while running:
            plt.clf()  # Clear the current figure
            clock.tick(60)  # Tick the clock to control the frame rate
            self.data_handler()  # Call the method to handle data

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in back_btn:
                        if btn.click(pos):        
                            client.menu_action(btn.text)

            aqi = np.array([])  # Array to store AQI data
            pm25 = np.array([])  # Array to store PM2.5 data
            pm10 = np.array([])  # Array to store PM10 data
            timestamp = np.array([])  # Array to store timestamp data

            try:
                x = np.flip(np.array(range(len(self.minute_avg))))  # Calculate the x-values for the plot

                for entry in self.minute_avg:
                    aqi = np.append(aqi, float(entry['aqi']))  # Append AQI data to the array
                    pm25 = np.append(pm25, float(entry['pm2.5']))  # Append PM2.5 data to the array
                    pm10 = np.append(pm10, float(entry['pm10']))  # Append PM10 data to the array
                    timestamp = np.append(timestamp, entry['timestamp'])  # Append timestamp data to the array

                plt.plot(x, aqi, color='red')  # Plot AQI data
                plt.plot(x, pm25, color='green')  # Plot PM2.5 data
                plt.plot(x, pm10, color='blue')  # Plot PM10 data

                plt.xlabel("Time Passed (minutes)")  # Set the x-axis label
                plt.ylabel("Data from the past hour")  # Set the y-axis label
                plt.title('Hour View')  # Set the title

                plt.legend(["AQI", "PM 2.5", "PM 10"], loc="lower right")  # Add a legend to the plot

                plt.savefig(MINUTE_GRAPH)  # Save the plot to a file

                img = pygame.image.load(MINUTE_GRAPH).convert()  # Load the saved plot
                self.redrawWindow(back_btn, img=img)  # Redraw the window with the plot
                continue

            except:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in back_btn:
                        if btn.click(pos):        
                            client.menu_action(btn.text)

            self.redrawWindow(back_btn, is_waiting=True)  # Redraw the window with a waiting message

    # Method to display day view
    def display_day_view(self):
        running = True
        while running:
            plt.clf()  # Clear the current figure
            clock.tick(60)  # Tick the clock to control the frame rate
            self.data_handler()  # Call the method to handle data

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in back_btn:
                        if btn.click(pos):        
                            client.menu_action(btn.text)

            aqi = np.array([])  # Array to store AQI data
            pm25 = np.array([])  # Array to store PM2.5 data
            pm10 = np.array([])  # Array to store PM10 data
            timestamp = np.array([])  # Array to store timestamp data

            try:
                x = np.flip(np.array(range(len(self.hour_avg))))  # Calculate the x-values for the plot

                for entry in self.hour_avg:
                    aqi = np.append(aqi, float(entry['aqi']))  # Append AQI data to the array
                    pm25 = np.append(pm25, float(entry['pm2.5']))  # Append PM2.5 data to the array
                    pm10 = np.append(pm10, float(entry['pm10']))  # Append PM10 data to the array
                    timestamp = np.append(timestamp, entry['timestamp'])  # Append timestamp data to the array

                plt.plot(x, aqi, color='red')  # Plot AQI data
                plt.plot(x, pm25, color='green')  # Plot PM2.5 data
                plt.plot(x, pm10, color='blue')  # Plot PM10 data

                plt.xlabel("Time Passed (hours)")  # Set the x-axis label
                plt.ylabel("Data from the past day")  # Set the y-axis label
                plt.title('Day View')  # Set the title

                plt.legend(["AQI", "PM 2.5", "PM 10"], loc="lower right")  # Add a legend to the plot

                plt.savefig(HOUR_GRAPH)  # Save the plot to a file

                img = pygame.image.load(HOUR_GRAPH).convert()  # Load the saved plot
                self.redrawWindow(back_btn, img=img)  # Redraw the window with the plot
                continue

            except:
                pass

            self.redrawWindow(back_btn, is_waiting=True)  # Redraw the window with a waiting message

    # Method to display week view
    def display_week_view(self):
        running = True
        while running:
            plt.clf()  # Clear the current figure
            clock.tick(60)  # Tick the clock to control the frame rate
            self.data_handler()  # Call the method to handle data

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in back_btn:
                        if btn.click(pos):        
                            client.menu_action(btn.text)

            aqi = np.array([])  # Array to store AQI data
            pm25 = np.array([])  # Array to store PM2.5 data
            pm10 = np.array([])  # Array to store PM10 data
            timestamp = np.array([])  # Array to store timestamp data

            try:
                x = np.flip(np.array(range(len(self.day_avg))))  # Calculate the x-values for the plot

                for entry in self.day_avg:
                    aqi = np.append(aqi, float(entry['aqi']))  # Append AQI data to the array
                    pm25 = np.append(pm25, float(entry['pm2.5']))  # Append PM2.5 data to the array
                    pm10 = np.append(pm10, float(entry['pm10']))  # Append PM10 data to the array
                    timestamp = np.append(timestamp, entry['timestamp'])  # Append timestamp data to the array

                plt.plot(x, aqi, color='red')  # Plot AQI data
                plt.plot(x, pm25, color='green')  # Plot PM2.5 data
                plt.plot(x, pm10, color='blue')  # Plot PM10 data

                plt.xlabel("Time Passed (days)")  # Set the x-axis label
                plt.ylabel("Data from the past week")  # Set the y-axis label
                plt.title('Week View')  # Set the title

                plt.legend(["AQI", "PM 2.5", "PM 10"], loc="lower right")  # Add alegend to the plot

                plt.savefig(DAY_GRAPH)  # Save the plot to a file

                img = pygame.image.load(DAY_GRAPH).convert()  # Load the saved plot
                self.redrawWindow(back_btn, img=img)  # Redraw the window with the plot
                continue

            except:
                pass

            self.redrawWindow(back_btn, is_waiting=True)  # Redraw the window with a waiting message

    # Method to redraw the window
    def redrawWindow(self, btns, img=None, is_main=False, is_waiting=False):
        win.fill((128, 128, 128))  # Fill the window with a grey color

        if is_main:
            text = font.render("Air Quality Monitor", 1, (0, 0, 0))  # Render the title text
            win.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 4 - text.get_height() / 2))  # Draw the title text on the screen

        if is_waiting:
            text = font.render("Waiting for data...", 1, (0, 0, 0))  # Render the waiting text
            win.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 4 - text.get_height() / 2))  # Draw the waiting text on the screen

        if not img == None:
            win.blit(img, (SCREEN_WIDTH / 2 - img.get_size()[0] / 2, SCREEN_HEIGHT / 2 - img.get_size()[1] / 2))  # Draw the image on the screen

        for btn in btns:
            btn.draw(win)  # Draw the buttons on the screen

        pygame.display.update()  # Update the display

    # Method to handle data
    def data_handler(self):
        self.current_step = datetime.datetime.now()  # Get the current time

        if self.current_step.second % 10 == 0 and self.current_step.second != self.last_step.second:  # Check if 10 seconds have passed
            try:
                (self.data_entries, self.minute_avg, self.hour_avg, self.day_avg) = self.network.send("get")  # Send a request to get data
                write_data(DATA_FILE, self.data_entries)  # Write data to a file
                write_data(MINUTE_FILE, self.minute_avg)  # Write minute average data to a file
                write_data(HOUR_FILE, self.hour_avg)  # Write hour average data to a file
                write_data(DAY_FILE, self.day_avg)  # Write day average data to a file
            except:
                pass

        self.last_step = self.current_step  # Update the last step time

# Function to write data to a file
def write_data(file, data):
    try:
        with open(file, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=data[0].keys())  # Create a DictWriter object
            fc.writeheader()  # Write the header
            fc.writerows(data)  # Write the data
    except:
        pass

client = Client()
client_no = int(client.network.getP())
print("Client No.: ", client_no)
client.client_no = client_no

# Main function
def main():
    run = True

    while run:
        clock.tick(60)  # Tick the clock to control the frame rate
        client.data_handler()  # Call the method to handle data

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in main_btns:
                    if btn.click(pos):        
                        client.menu_action(btn.text)

        try:
            client.redrawWindow(main_btns, is_main=True)  # Redraw the window with the main menu
        except pygame.error:
            pass

main()