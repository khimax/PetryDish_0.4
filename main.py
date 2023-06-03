import pygame
import random
import math
import os.path
import tkinter as tk
from PIL import Image, ImageTk

def remove_focus(event):
    window.focus_set()
def SpaceBar():
    global IsEnabled
    if IsEnabled == True:
        IsEnabled = False
        canvas.itemconfig(go_Button, image=goOff_image)
        canvas.itemconfig(stop_Button, image=stopOn_image)
        canvas.coords(stop_Button, 78 + 4, 290)
    elif IsEnabled == False:
        IsEnabled = True
        canvas.itemconfig(go_Button, image=goOn_image)
        canvas.itemconfig(stop_Button, image=stopOff_image)
        canvas.coords(stop_Button, 78, 290)
def Stop_click(event):
    global IsEnabled
    if IsEnabled==True:
        IsEnabled = False
        canvas.itemconfig(go_Button, image=goOff_image)
        canvas.itemconfig(stop_Button, image=stopOn_image)
        canvas.coords(stop_Button, 78+4, 290)
def Go_click(event):
    global IsEnabled
    if IsEnabled==False:
        IsEnabled = True
        canvas.itemconfig(go_Button, image=goOn_image)
        canvas.itemconfig(stop_Button, image=stopOff_image)
        canvas.coords(stop_Button, 78, 290)
def speedFocusOut(event):
    global breeding_interval
    global SpeedChanged
    global speed_value
    if SpeedChanged == False:
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, int(1000/breeding_interval))
        print(breeding_interval)
    SpeedChanged = False
def timerFocusOut(event):
    global timer
    timer_entry.delete(0, tk.END)
    timer_entry.insert(0, int(timer))
def resetPressed_click(event):
    canvas.itemconfig(resetButton, image=reset_image)
def reset_click(event):
    global bacteria_list
    canvas.itemconfig(resetButton, image=resetPressed_image)
    bacteria_list.empty()
    dish_surface.fill(empty)
    dish_surface.blit(DishImg, (-1, 0))
def reset_r(event):
    global bacteria_list
    canvas.itemconfig(resetButton, image=resetPressed_image)
    bacteria_list.empty()
    dish_surface.fill(empty)
    dish_surface.blit(DishImg, (-1, 0))
    canvas.itemconfig(resetButton, image=resetPressed_image)
def handle_key_release(event):
    if event.keysym == "r":
        canvas.itemconfig(resetButton, image=reset_image)
    elif event.keysym == "space":
        SpaceBar()

def speed_click(event):
    global breeding_interval
    global last_speed
    global SpeedChanged
    global speed_value
    last_speed = breeding_interval
    try:
        speed_value = float(speed_entry.get())
        breeding_interval = 1000/speed_value
        last_speed = breeding_interval
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, int(speed_value))
        SpeedChanged = True
    except ZeroDivisionError:
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, int(1000/last_speed))
        breeding_interval = last_speed
    except ValueError:
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, int(1000/last_speed))
        breeding_interval = last_speed
def time_click(event):
    global timer
    timerLocal = int(timer)
    try:
        timer = int(timer_entry.get())
    except ValueError:
        timer_entry.delete(0, tk.END)
        timer_entry.insert(0, timerLocal)

def quit_click(event):
    window.destroy()
    pygame.quit()

def x_click():
    window.destroy()
    pygame.quit()
def breed_bacteria():
    new_bacteria_count = int(len(bacteria_list) * breeding_rate)
    for _ in range(new_bacteria_count):
        # Generate random positions within the breeding area
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, radius)
        x = area_center_x + int(distance * math.cos(angle))
        y = area_center_y + int(distance * math.sin(angle))

        # Add the new bacteria sprite if it is within the breeding area
        if math.sqrt((x - area_center_x) ** 2 + (y - area_center_y) ** 2) <= radius:
            bacteria = Bacteria(x, y)
            bacteria_list.add(bacteria)

# Define a class for the bacteria sprite
class Bacteria(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(center=(x, y))

        # Check if the bacteria sprite is out of bounds and wrap it around if necessary
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2

        # Calculate the distance between the sprite center and the area center
        distance = math.sqrt((center_x - area_center_x) ** 2 + (center_y - area_center_y) ** 2)

        # Check if the sprite center is outside the circular area
        if distance > radius:
            # Wrap the sprite around the circular area
            angle = math.atan2(center_y - area_center_y, center_x - area_center_x)
            new_x = area_center_x + int(radius * math.cos(angle))
            new_y = area_center_y + int(radius * math.sin(angle))
            self.rect.x = new_x - self.rect.width // 2
            self.rect.y = new_y - self.rect.height // 2

window = tk.Tk()
window.geometry("128x384")
window.resizable(False, False)
window.geometry("+200+300")
dish_width = 405
dish_height = 410

# Define the colors used for the dish and bacteria
bacteria_color = (0, 255, 0)

# Define the initial number of bacteria and the breeding rate
initial_bacteria = 1
breeding_rate = 1

# Define the radius of the circular area (smaller than half of dish_width or dish_height)
radius = 200

# Define the time interval between breeding cycles (in milliseconds)
breeding_interval = 1000
timer = 0

# Initialize Pygame and create the Petri dish surface
pygame.init()
dish_surface = pygame.display.set_mode((dish_width, dish_height))
pygame.display.set_caption("Petri Dish")

# Create a list to hold the bacteria sprites
bacteria_list = pygame.sprite.Group()

# Calculate the center coordinates of the circular area
area_center_x = (dish_width // 2)
area_center_y = (dish_height // 2)

# Script direction for importing files
script_dir = os.path.dirname(os.path.abspath(__file__))

# Import images
quit_image = tk.PhotoImage(file=os.path.join(script_dir, "Quit.png"))
quitEnter_image = tk.PhotoImage(file=os.path.join(script_dir, "QuitPressed.png"))
timer_image = tk.PhotoImage(file=os.path.join(script_dir, "Timer.png"))
speed_image = tk.PhotoImage(file=os.path.join(script_dir, "Speed.png"))
count_image = tk.PhotoImage(file=os.path.join(script_dir, "Count.png"))
reset_image = tk.PhotoImage(file=os.path.join(script_dir, "Reset.png"))
resetPressed_image = tk.PhotoImage(file=os.path.join(script_dir, "ResetPressed.png"))
goOn_image = tk.PhotoImage(file=os.path.join(script_dir, "GoOn.png"))
goOff_image = tk.PhotoImage(file=os.path.join(script_dir, "GoOff.png"))
stopOff_image = tk.PhotoImage(file=os.path.join(script_dir, "StopOff.png"))
stopOn_image = tk.PhotoImage(file=os.path.join(script_dir, "StopOn.png"))

# Dish image importing
DishImg = pygame.image.load(os.path.join(script_dir, "Dish.png"))
dish_surface.blit(DishImg, (-1, 0))

# Creating canvas
canvas = tk.Canvas(window, width = 128, height = 384)
canvas.pack(side=tk.TOP, padx=0, pady=0)
bgImage = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "List.png")))
bg = canvas.create_image(0, 0, image=bgImage, anchor=tk.NW)
canvas.bind("<Button-1>", remove_focus)

# Timer
timeButton = canvas.create_image(0, 173, image=timer_image, anchor=tk.NW)
timer_entry = tk.Entry(window, width=3, bd=0, fg="#336d92")
timer_entry.insert(0, 0)
timer_window = canvas.create_window(17, 173+20, anchor="nw", window=timer_entry)
timer_entry.bind('<Return>', time_click)
timer_entry.bind("<FocusOut>", timerFocusOut)

# Breeding speed
speedButton = canvas.create_image(0, 108, image=speed_image, anchor=tk.NW)
speed_entry = tk.Entry(window, width=3, bd=0, fg="#336d92")
speed_entry.insert(0, 1)
speed_window = canvas.create_window(17, 108+20, anchor="nw", window=speed_entry)
speed_entry.bind('<Return>', speed_click)
speed_entry.bind("<FocusOut>", speedFocusOut)
last_speed = breeding_interval
SpeedChanged = False
speed_value = 1

# Reset
resetButton = canvas.create_image(14, 334, image=reset_image, anchor=tk.NW)
canvas.tag_bind(resetButton, "<Button-1>", reset_click)
canvas.tag_bind(resetButton, "<ButtonRelease-1>", resetPressed_click)
window.bind("r", reset_click)
window.bind("<KeyRelease>", handle_key_release)

# Count
CounterImg = canvas.create_image(0, 42, image=count_image, anchor=tk.NW)
counterText = canvas.create_text(29, 42+28, text=str(len(bacteria_list)))

# Pause
go_Button = canvas.create_image(78, 250, image=goOn_image, anchor=tk.NW)
stop_Button = canvas.create_image(78, 290, image=stopOff_image, anchor=tk.NW)
canvas.tag_bind(go_Button, "<Button-1>", Go_click)
canvas.tag_bind(stop_Button, "<Button-1>", Stop_click)

# Create the initial bacteria sprites and add them to the list
for i in range(initial_bacteria):
    x = random.randint(0, dish_width-5)
    y = random.randint(0, dish_height-5)
    bacteria = Bacteria(x, y)
    bacteria_list.add(bacteria)

# Initialize the timer and breeding cycle counter
breeding_timer = pygame.time.get_ticks()
cycle_count = 0
empty = pygame.Color(0, 0, 0, 0) #The last 0 indicates 0 alpha, a transparent color
# Start the Pygame main loop
IsEnabled = True
running = True
while running:
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Check if it's time to breed new bacteria
    current_time = pygame.time.get_ticks()
    # Breed new bacteria according to the breeding rate and reset the breeding timer
    if IsEnabled==True:
        if current_time - breeding_timer >= breeding_interval:
            if timer >= 1:
                breed_bacteria()
                timer -= 1
                timer_entry.delete(0, tk.END)
                timer_entry.insert(0, timer)

            breeding_timer = current_time
            cycle_count += 1
    if len(bacteria_list)==0:
        # Create the initial bacteria sprites and add them to the list
        for i in range(initial_bacteria):
            x = random.randint(0, dish_width - 5)
            y = random.randint(0, dish_height - 5)
            bacteria = Bacteria(x, y)
            bacteria_list.add(bacteria)

    # Clear the dish surface and draw the bacteria sprites
    bacteria_list.draw(dish_surface)
    canvas.itemconfig(counterText, text=str(len(bacteria_list)))
    # Update the bacteria sprites
    bacteria_list.update()

    # Update the display
    pygame.display.update()
    window.update()