# SwimSense
SwimSense is a python script which simulates the swarming behaviour displayed by fish according to the boids algorithm. The fish move according to the following three rules:
1. Seperation: steer to avoid crowding local flockmates
2. Alignment: steer towards the average heading of local flockmates
3. Cohesion:  steer to move towards the acerage position of local flockmates

Furthermore, the fish are also encoded to avoid any obstacles present in the reef.

## Pre-Requisites:
This script requires the following modules:
- python3
- PyGame

### Installation:
#### Python3:
visit the official python website and download the installer for your specific operational system. Run the installer and follow the instructions.

Website : https://www.python.org/downloads/

#### PyGame:
run the following line in your terminal:

```pip install pygame```

This should install PyGame, if there any issues, visit the PyGame website for complete instructions.

Website: https://www.pygame.org/wiki/GettingStarted

## Running the scripts
To run any of the scripts, navigate to the directory containing the script in your terminal and run the following command:

```
python SwimSense_Generic.py
```

```
python SwimSense_swarm.py
```
```
python SwimSense_obstacle.py
```

### SwimSense_Generic:
This version of the file is made for the user to play around with values, and try different simulations without downloading or storing any data points. This is essentially the 'sandbox' of SwimSense.

### SwimSense_swarm:
Running this code will initiate the code in order to accumulate the data for the swarming evaluation presented in the final report for the course AE4350.

### SwimSense_obstacle: 
Running this code will initiate the code to accumulate the data for the obstacle avoidance evaluation presented in the final report for the course AE4350.

## Costomizations:
There are several values within the code which can be tweaked and varied in order to see different types of behaviour, an overview of them is provided here:
```
Grid = True # allows the grid to be visualised in the environment
Obstacles = False # determines if this run uses obstacles (True) or not (False)
WIDTH = 1200 # width of the display window
HEIGHT = 800 # height of the display window
FPS = 60 # frames per second
BACKGROUND = (26, 193, 221) # background color

# Obstacle Parameters:
O_RANGE = 100 # range from which fish can detect the obstacle
O_RADIUS = 25 # radius of the circular obstacles
O_COUNT = 1 # ammount of obstacles present

# Fish setup:
RECT_FISH = True # display fish rect
RADIUS = True # display fish radius of influence
CLOSEST_OBSTACLE = False # display a line to the closest obstacle
F_COUNT = 50 # ammount of fish present
F_SPEED = 100 # how fast the fish move
F_RANGE = 100  # determine the radius of the range of influence for the fish

# within the fish class:
threshold_nearest_fish = 10 # threshold for the nearest fish
turn_rate = 2 # rate at which the fish can change angle
```
