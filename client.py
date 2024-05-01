import pygame
import matplotlib.pyplot as plt
from network import Network
import datetime
import csv
from _thread import *
import numpy as np

DATA_FILE = 'figures/data_entries.csv'
MINUTE_FILE = 'figures/minute_avg.csv'
HOUR_FILE = 'figures/hour_avg.csv'
DAY_FILE = 'figures/day_avg.csv'

DATA_GRAPH = 'figures/data_entries.png'
MINUTE_GRAPH = 'figures/minute_avg.png'
HOUR_GRAPH = 'figures/hour_avg.png'
DAY_GRAPH = 'figures/day_avg.png'

# Define screen dimensions
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Define button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 100

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIME = (50,205,50)
ORANGE = (255,165,0)
GREY = (128,128,128)

pygame.init()
clock = pygame.time.Clock()

# define fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Air Quality Monitor")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = small_font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), (self.y + round(self.height/2) - round(text.get_height()/2))))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
        
main_btns = [Button("Live Data", SCREEN_WIDTH/3 - BUTTON_WIDTH/2, 2*SCREEN_HEIGHT/4 - BUTTON_HEIGHT/2, YELLOW), 
            Button("Hour View", 2*SCREEN_WIDTH/3 - BUTTON_WIDTH/2, 2*SCREEN_HEIGHT/4 - BUTTON_HEIGHT/2, YELLOW), 
            Button("Day View", SCREEN_WIDTH/3 - BUTTON_WIDTH/2, 3*SCREEN_HEIGHT/4 - BUTTON_HEIGHT/2, YELLOW), 
            Button("Week View", 2*SCREEN_WIDTH/3 - BUTTON_WIDTH/2, 3*SCREEN_HEIGHT/4 - BUTTON_HEIGHT/2, YELLOW)]
back_btn = [Button("Back", SCREEN_WIDTH/8 - BUTTON_WIDTH/2, SCREEN_HEIGHT/6 - BUTTON_HEIGHT/2, YELLOW)]

class Client():
    def __init__(self):
        self.client_no = None
        self.network = Network()
        self.data_entries = None
        self.minute_avg = None
        self.hour_avg = None
        self.day_avg = None 
        self.last_step = datetime.datetime.now()
        self.current_step = None
        
    def menu_action(self,selected_option):
        try:
            if selected_option == "Live Data":
                print("Live Data selected") 
                self.display_live_data()
            elif selected_option == "Hour View": 
                print("Hour View selected") 
                self.display_hour_view()
            elif selected_option == "Day View":
                print("Day View selected") 
                self.display_day_view()
            elif selected_option == "Week View":
                print("Week View selected") 
                self.display_week_view()
            elif selected_option == "Back":
                print("Back selected") 
                main()
        except TypeError as e:
            print(e)

    def display_live_data(self):
        running = True
        while running:
            plt.clf()
            clock.tick(60)
            self.data_handler()
            aqi = np.array([])
            pm25 = np.array([])
            pm10 = np.array([])
            timestamp = np.array([])
            try:
                x = np.array(range(len(self.data_entries)))*10
            
                for entry in self.data_entries:
                    aqi=np.append(aqi,entry['aqi'])
                    pm25=np.append(pm25,entry['pm2.5'])
                    pm10=np.append(pm10,entry['pm10'])
                    timestamp=np.append(timestamp,entry['timestamp'])
            

                plt.plot(x, aqi, color = 'red')
                plt.plot(x, pm25, color = 'green')
                plt.plot(x, pm10, color = 'blue')

                plt.xlabel("Time (seconds)")
                plt.ylabel("Sensor Data")
                plt.title('Live Data')

                plt.legend(["aqi", "pm25", "pm10"], loc="lower right")

                plt.savefig(DATA_GRAPH)

                img = pygame.image.load(DATA_GRAPH).convert()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in back_btn:
                            if btn.click(pos):        
                                client.menu_action(btn.text)
                
                self.redrawWindow(back_btn,img = img)
            except:
                pass


    def display_hour_view(self):
        running = True
        while running:
            plt.clf()
            clock.tick(60)
            self.data_handler()
            aqi = np.array([])
            pm25 = np.array([])
            pm10 = np.array([])
            timestamp = np.array([])
            plot = plt.plot()
            try:
                x = np.array(range(len(self.minute_avg)))
            
                for entry in self.minute_avg:
                    aqi=np.append(aqi,entry['aqi'])
                    pm25=np.append(pm25,entry['pm2.5'])
                    pm10=np.append(pm10,entry['pm10'])
                    timestamp=np.append(timestamp,entry['timestamp'])
            

                plot(x, aqi, color = 'red')
                plot(x, pm25, color = 'green')
                plt.plot(x, pm10, color = 'blue')

                plt.xlabel("Time (minutes)")
                plt.ylabel("Data from the past hour")
                plt.title('Hour View')

                plt.legend(["aqi", "pm25", "pm10"], loc="lower right")

                plt.savefig(MINUTE_GRAPH)

                img = pygame.image.load(MINUTE_GRAPH).convert()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in back_btn:
                            if btn.click(pos):        
                                client.menu_action(btn.text)
                
                self.redrawWindow(back_btn,img = img)
            except:
                pass

    def display_day_view(self):
        running = True
        while running:
            plt.clf()
            clock.tick(60)
            self.data_handler()
            aqi = np.array([])
            pm25 = np.array([])
            pm10 = np.array([])
            timestamp = np.array([])
            try:
                x = np.array(range(len(self.hour_avg)))
            
                for entry in self.hour_avg:
                    aqi=np.append(aqi,entry['aqi'])
                    pm25=np.append(pm25,entry['pm2.5'])
                    pm10=np.append(pm10,entry['pm10'])
                    timestamp=np.append(timestamp,entry['timestamp'])
            

                plt.plot(x, aqi, color = 'red')
                plt.plot(x, pm25, color = 'green')
                plt.plot(x, pm10, color = 'blue')

                plt.xlabel("Time (hours)")
                plt.ylabel("Data from the past day")
                plt.title('DAy View')

                plt.legend(["aqi", "pm25", "pm10"], loc="lower right")

                plt.savefig(HOUR_GRAPH)

                img = pygame.image.load(HOUR_GRAPH).convert()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in back_btn:
                            if btn.click(pos):        
                                client.menu_action(btn.text)
                
                self.redrawWindow(back_btn,img = img)
            except:
                pass

    def display_week_view(self):
        running = True
        while running:
            plt.clf()
            clock.tick(60)
            self.data_handler()
            aqi = np.array([])
            pm25 = np.array([])
            pm10 = np.array([])
            timestamp = np.array([])
            try:
                x = np.array(range(len(self.day_avg)))
            
                for entry in self.day_avg:
                    aqi=np.append(aqi,entry['aqi'])
                    pm25=np.append(pm25,entry['pm2.5'])
                    pm10=np.append(pm10,entry['pm10'])
                    timestamp=np.append(timestamp,entry['timestamp'])
            

                plt.plot(x, aqi, color = 'red')
                plt.plot(x, pm25, color = 'green')
                plt.plot(x, pm10, color = 'blue')

                plt.xlabel("Time (days)")
                plt.ylabel("Data from the past week")
                plt.title('Hour View')

                plt.legend(["aqi", "pm25", "pm10"], loc="lower right")

                plt.savefig(DAY_GRAPH)

                img = pygame.image.load(DAY_GRAPH).convert()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in back_btn:
                            if btn.click(pos):        
                                client.menu_action(btn.text)
                
                self.redrawWindow(back_btn,img = img)
            except:
                pass

    def redrawWindow(self, btns, img = None, is_main = False):
        win.fill((128,128,128))

        if is_main:
            text = font.render("Air Quality Monitor", 1, (0,0,0))
            win.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/4 - text.get_height()/2))

        if not img == None:
            win.blit(img,(SCREEN_WIDTH/2 - img.get_size()[0]/2,SCREEN_HEIGHT/2 - img.get_size()[1]/2))

        for btn in btns:
            btn.draw(win)

        pygame.display.update()

    def data_handler(self):
        self.current_step = datetime.datetime.now()
        
        if self.current_step.second % 10 == 0 and self.current_step.second != self.last_step.second: # ten second interval 
            # try:
                (self.data_entries, self.minute_avg, self.hour_avg, self.day_avg) = self.network.send("get")
                write_data(DATA_FILE, self.data_entries)
                write_data(MINUTE_FILE, self.minute_avg)
                write_data(HOUR_FILE, self.hour_avg)
                write_data(DAY_FILE, self.day_avg)
            # except:
            #     pass
        self.last_step = self.current_step

                
def write_data(file, data):
    try:
        # print("Writing data to ", file)
        with open(file, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, 
                                fieldnames=data[0].keys(),

                            )
            fc.writeheader()
            fc.writerows(data)  
    except:
        pass

client = Client()
client_no = int(client.network.getP())
print("Client No.: ", client_no)
client.client_no = client_no  

def main():
    run = True

    while run:
        clock.tick(60)
        client.data_handler()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in main_btns:
                    if btn.click(pos):        
                        client.menu_action(btn.text)

        client.redrawWindow(main_btns, is_main=True)
    
main()