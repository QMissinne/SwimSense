import pygame as pg
from pygame.locals import *
import random
from random import random, randint
import math
from math import pi
from math import cos, sin, radians, degrees, atan2

# initialise pygame:
pg.init()

# -----------------------------------------------------------------------------
# Setup:
# -----------------------------------------------------------------------------
vec = pg.math.Vector2
clock = pg.time.Clock()

#Parameters:
OBSTACLE_RANGE = 25

# Display:
GRID = False
OBSTACLES = False
WIDTH = 1200
HEIGHT = 800
FPS = 60
BACKGROUND = (26, 193, 221)

# Fish setup:
RECT_FISH = False
RADIUS = False
CLOSEST_OBSTACLE = False
F_COUNT = 50
F_SPEED = 120

# Shark setup:
S_COUNT = 3
S_SPEED = 100
S_RANGE = 10
RECT_SHARK = False

FramePerSec = pg.time.Clock()

displaysurface = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE)
displaysurface.fill(BACKGROUND) #(26, 193, 221)
pg.display.set_caption("The Reef")
# -----------------------------------------------------------------------------
# Grid Class:
# -----------------------------------------------------------------------------
class Grid():
    """
    The grid class is used to seperate the environment into a grid of cells
    which will allow for the fish to find their neighbours more efficiently, and
    later be used for the reward function of the shark. The grid will be defined
    as a dictionary of cells, with each cell containing a list of fish objects.
    """
    def __init__(self):
        self.cell_size = 50
        self.grid = {}

    def get_cell(self, pos):
        return (int(pos.x / self.cell_size), int(pos.y / self.cell_size))
    
    def visualize_grid(self):
        for x in range(0, WIDTH, self.cell_size):
            pg.draw.line(displaysurface, (0, 0, 0), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, self.cell_size):
            pg.draw.line(displaysurface, (0, 0, 0), (0, y), (WIDTH, y))
    
grid = Grid()

# -----------------------------------------------------------------------------
# Obstacle Class: - TO DO AFTER FISH MOVEMENT ENCODED! - 
# -----------------------------------------------------------------------------
class Obstacle(pg.sprite.Sprite):
    """
    The obstacle class is used to define the obstacles within the reef. 
    This will create a barrier for the fish to navigate around, and potentially
    allow the shark to trap the fish. The obstacles will be defined as differently
    colored blocks within the reef (bright colors for the coral and darker colors
    for the stone - it is important to note that the coral and the stone will
    share the same behavior).
    """
    def __init__(self, x , y):
        super().__init__()
        self.surf = pg.Surface((10, 10)).convert()
        self.surf.fill((0,0, 0))
        self.color = pg.Color(0, 0, 0)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.pos = vec(self.rect.center)
        self.obstacle_positions = []

    def create_obstacles():
        obstacle_positions = [(650, 190), (660, 190), (670, 190), (680, 190), (690, 190), (700, 190),
                              (630, 200), (640, 200), (650, 200), (660, 200), (670, 200), (680, 200), (690, 200),
                              (700, 200), (710, 200), (610, 210), (620, 210), (630, 210), (640, 210), (650, 210),
                              (660, 210), (670, 210), (680, 210), (690, 210), (700, 210), (710, 210), (720, 210),
                              (620, 220), (630, 220), (640, 220), (650, 220), (660, 220), (670, 220), (680, 220),
                              (620, 230), (630, 230), (640, 230), (650, 230), (660, 230), (670, 230), (680, 230),
                              (610, 240), (620, 240), (630, 240), (640, 240), (650, 240), (660, 240), (670, 240),
                              (630, 250), (640, 250), (650, 250), (660, 250),
                              
                              (400, 200), (410, 200), (420, 200), (430, 200), (440, 200), (450, 200), (460, 200),
                              (380, 210), (390, 210), (400, 210), (410, 210), (420, 210), (430, 210), (440, 210),
                              (380, 220), (390, 220), (400, 220), (410, 220), (420, 220), (430, 220), (440, 220),
                              (370, 230), (380, 230), (390, 230), (400, 230), (410, 230), (420, 230), (430, 230),
                              (370, 240), (380, 240), (390, 240), (400, 240), (410, 240), (420, 240), (430, 240),
                              (360, 250), (370, 250), (380, 250), (390, 250), (400, 250), (410, 250), (420, 250),
                              (430, 250), (440, 250),
                              (350, 260), (360, 260), (370, 260), (380, 260), (390, 260), (400, 260), (410, 260),
                              (420, 260), (430, 260), (440, 260), (450, 260),
                              (340, 270), (350, 270), (360, 270), (370, 270), (380, 270), (390, 270), (400, 270),
                              (410, 270), (420, 270), (430, 270), (440, 270), (450, 270), (460, 270), (470, 270),
                              (360, 280), (370, 280), (380, 280), (390, 280), (400, 280), (410, 280), (420, 280),
                              (430, 280), (440, 280), (450, 280), (460, 280), (470, 280), (480, 280), (490, 280),
                              (370, 290), (380, 290), (390, 290), (400, 290), (410, 290), (420, 290), (430, 290),
                              (440, 290), (450, 290), (460, 290), (470, 290), (480, 290), (490, 290), (500, 290),
                              (380, 300), (390, 300), (400, 300), (410, 300), (420, 300), (430, 300), (440, 300),
                              (450, 300), (460, 300), (470, 300), (480, 300), (490, 300), (500, 300), (510, 300),
                              (400, 310), (410, 310), (420, 310), (430, 310), (440, 310), (450, 310), (460, 310),
                              (470, 310), (480, 310), (490, 310), (500, 310), (510, 310), (520, 310),
                              (400, 320), (410, 320), (420, 320), (430, 320), (440, 320), (450, 320), (460, 320),
                              (470, 320), (480, 320), (490, 320), (500, 320), (510, 320), (520, 320), (530, 320),
                              (410, 330), (420, 330), (430, 330), (440, 330), (450, 330), (460, 330), (470, 330),
                              (480, 330), (490, 330), (500, 330), (510, 330), (520, 330), (530, 330), (540, 330),
                              (550, 330), (560, 330),
                              (420, 340), (430, 340), (440, 340), (450, 340), (460, 340), (470, 340), (480, 340),
                              (490, 340), (500, 340), (510, 340), (520, 340), (530, 340), (540, 340), (550, 340),
                              (560, 340), (570, 340), (580, 340),
                              (430, 350), (440, 350), (450, 350), (460, 350), (470, 350), (480, 350), (490, 350),
                              (500, 350), (510, 350), (520, 350), (530, 350), (540, 350), (550, 350), (560, 350),
                              (570, 350), (580, 350), (590, 350),
                              (440, 360), (450, 360), (460, 360), (470, 360), (480, 360), (490, 360), (500, 360),
                              (510, 360), (520, 360), (530, 360), (540, 360), (550, 360), (560, 360), (570, 360),
                              (580, 360), (590, 360), (600, 360), (610, 360), (620, 360),
                              (450, 370), (460, 370), (470, 370), (480, 370), (490, 370), (500, 370), (510, 370),
                              (520, 370), (530, 370), (540, 370), (550, 370), (560, 370), (570, 370), (580, 370),
                              (590, 370), (600, 370), (610, 370), (620, 370), (630, 370), (640, 370), (650, 370),
                              (430, 380), (440, 380), (450, 380), (460, 380), (470, 380), (480, 380), (490, 380),
                              (500, 380), (510, 380), (520, 380), (530, 380), (540, 380), (550, 380), (560, 380), 
                              (570, 380), (580, 380), (590, 380), (600, 380), (610, 380), (620, 380), (630, 380),
                              (640, 380), (650, 380), (660, 380), (670, 380), (680, 380), (690, 380),
                              (410, 390), (420, 390), (430, 390), (440, 390), (450, 390), (460, 390), (470, 390),
                              (480, 390), (490, 390), (500, 390), (510, 390), (520, 390), (530, 390), (540, 390),
                              (550, 390), (560, 390), (570, 390), (580, 390), (590, 390), (600, 390), (610, 390),
                              (620, 390), (630, 390), (640, 390), (650, 390), (660, 390), (670, 390), (680, 390),
                              (400, 400), (410, 400), (420, 400), (430, 400), (440, 400), (450, 400), (460, 400),
                              (470, 400), (480, 400), (490, 400), (500, 400), (510, 400), (520, 400), (530, 400),
                              (540, 400), (550, 400), (560, 400), (570, 400), (580, 400), (590, 400), (600, 400),
                              (610, 400), (620, 400), (630, 400), (640, 400), (650, 400),
                              (380, 410), (390, 410), (400, 410), (410, 410), (420, 410), (430, 410), (440, 410),
                              (450, 410), (460, 410), (470, 410), (480, 410), (490, 410), (500, 410), (510, 410),
                              (520, 410), (530, 410), (540, 410), (550, 410), (560, 410), (570, 410), (580, 410),
                              (410, 420), (420, 420), (430, 420), (440, 420), (450, 420), (460, 420), (470, 420),
                              (430, 430),
                              
                              (850, 250), (860, 250), (870, 250), (880, 250), (890, 250), (900, 250), (910, 250),
                              (840, 260), (850, 260), (860, 260), (870, 260), (880, 260), (890, 260), (900, 260),
                              (800, 270), (810, 270), (820, 270), (830, 270), (840, 270), (850, 270), (860, 270),
                              (870, 270), (880, 270), (890, 270), (900, 270), (910, 270), (920, 270), (930, 270),
                              (820, 280), (830, 280), (840, 280), (850, 280), (860, 280), (870, 280), (880, 280),
                              (890, 280), (900, 280), (910, 280), (920, 280), (930, 280), (940, 280), (950, 280),
                              (810, 290), (820, 290), (830, 290), (840, 290), (850, 290), (860, 290), (870, 290),
                              (880, 290), (890, 290), (900, 290), (910, 290), (920, 290), (930, 290), (940, 290),
                              (950, 290), (960, 290), (970, 290),
                              (820, 300), (830, 300), (840, 300), (850, 300), (860, 300), (870, 300), (880, 300),
                              (890, 300), (900, 300), (910, 300), (920, 300), (930, 300), (940, 300), (950, 300),
                              (820, 310), (830, 310), (840, 310), (850, 310), (860, 310), (870, 310), (880, 310),
                              (890, 310), (900, 310), (910, 310), (920, 310), (930, 310), (940, 310), (950, 310),
                              (860, 320), (870, 320), (880, 320), (890, 320), (900, 320), (910, 320), (920, 320),
                              (930, 320),
                              (880, 330), (890, 330), (900, 330), (910, 330), (920, 330),
                              (900, 340), (910, 340), (920, 340),
                              
                              (890, 410), (900, 410), (910, 410), (920, 410),
                              (860, 420), (870, 420), (880, 420), (890, 420), (900, 420), (910, 420), (920, 420),
                              (850, 430), (860, 430), (870, 430), (880, 430), (890, 430), (900, 430), (910, 430),
                              (820, 440), (830, 440), (840, 440), (850, 440), (860, 440), (870, 440), (880, 440),
                              (890, 440), (900, 440), (910, 440),
                              (800, 450), (810, 450), (820, 450), (830, 450), (840, 450), (850, 450), (860, 450),
                              (870, 450), (880, 450), (890, 450), (900, 450), (910, 450), (920, 450), (930, 450),
                              (750, 460), (760, 460), (770, 460), (780, 460), (790, 460), (800, 460), (810, 460),
                              (820, 460), (830, 460), (840, 460), (850, 460), (860, 460), (870, 460), (880, 460),
                              (890, 460), (900, 460), (910, 460), (920, 460), (930, 460),
                              (720, 470), (730, 470), (740, 470), (750, 470), (760, 470), (770, 470), (780, 470),
                              (790, 470), (800, 470), (810, 470), (820, 470), (830, 470), (840, 470), (850, 470),
                              (860, 470), (870, 470), (880, 470), (890, 470), (900, 470), (910, 470), (920, 470),
                              (710, 480), (720, 480), (730, 480), (740, 480), (750, 480), (760, 480), (770, 480),
                              (780, 480), (790, 480), (800, 480), (810, 480), (820, 480), (830, 480), (840, 480),
                              (850, 480), (860, 480), (870, 480), (880, 480), (890, 480), (900, 480), (910, 480),
                              (680, 490), (690, 490), (700, 490), (710, 490), (720, 490), (730, 490), (740, 490),
                              (750, 490), (760, 490), (770, 490), (780, 490), (790, 490), (800, 490), (810, 490),
                              (820, 490), (830, 490), (840, 490), (850, 490), (860, 490), (870, 490), (880, 490),
                              (650, 500), (660, 500), (670, 500), (680, 500), (690, 500), (700, 500), (710, 500),
                              (720, 500), (730, 500), (740, 500), (750, 500), (760, 500), (770, 500), (780, 500),
                              (790, 500), (800, 500), (810, 500), (820, 500), (830, 500), (840, 500), (850, 500),
                              (630, 510), (640, 510), (650, 510), (660, 510), (670, 510), (680, 510), (690, 510),
                              (700, 510), (710, 510), (720, 510), (730, 510), (740, 510), (750, 510), (760, 510),
                              (770, 510), (780, 510), (790, 510), (800, 510), (810, 510), (820, 510), (830, 510),
                              (550, 520), (560, 520), (570, 520), (580, 520), (590, 520), (600, 520), (610, 520),
                              (620, 520), (630, 520), (640, 520), (650, 520), (660, 520), (670, 520), (680, 520),
                              (690, 520), (700, 520), (710, 520), (720, 520), (730, 520), (740, 520), (750, 520),
                              (760, 520), (770, 520), (780, 520), (790, 520), (800, 520), (810, 520), (820, 520),
                              (500, 530), (510, 530), (520, 530), (530, 530), (540, 530), (550, 530), (560, 530),
                              (570, 530), (580, 530), (590, 530), (600, 530), (610, 530), (620, 530), (630, 530),
                              (640, 530), (650, 530), (660, 530), (670, 530), (680, 530), (690, 530), (700, 530),
                              (710, 530), (720, 530), (730, 530), (740, 530), (750, 530), (760, 530), (770, 530),
                              (780, 530), (790, 530), (800, 530), (810, 530), (820, 530), (830, 530), (840, 530),
                              (530, 540), (540, 540), (550, 540), (560, 540), (570, 540), (580, 540), (590, 540),
                              (600, 540), (610, 540), (620, 540), (630, 540), (640, 540), (650, 540), (660, 540),
                              (670, 540), (680, 540), (690, 540), (700, 540), (710, 540), (720, 540), (730, 540),
                              (740, 540), (750, 540), (760, 540), (770, 540), (780, 540), (790, 540), (800, 540),
                              (810, 540), (820, 540), (830, 540), (840, 540), (850, 540), (860, 540), (870, 540),
                              (880, 540),
                              (580, 550), (590, 550), (600, 550), (610, 550), (620, 550), (630, 550), (640, 550),
                              (650, 550), (660, 550), (670, 550), (680, 550), (690, 550), (700, 550), (710, 550),
                              (720, 550), (730, 550), (740, 550), (750, 550), (760, 550), (770, 550), (780, 550),
                              (790, 550), (800, 550), (810, 550), (820, 550), (830, 550), (840, 550), (850, 550),
                              (650, 560), (660, 560), (670, 560), (680, 560), (690, 560), (700, 560), (710, 560),
                              (720, 560), (730, 560), (740, 560), (750, 560), (760, 560), (770, 560), (780, 560),]
        return [Obstacle(x, y) for x, y in obstacle_positions], obstacle_positions


# -----------------------------------------------------------------------------
# Fish Class
# -----------------------------------------------------------------------------
class Fish(pg.sprite.Sprite):
    """
    Fish class used to describe the fish swarming behaviour according to
    the boids algorithm. the fish will move according to the following rules:
    - seperation: steer to avoid crowding local flockmates; 
    - alignment: steer towards the average heading of local flockmates;
    - cohesion: steer to move towards the average position of local flockmates;
    The fish will also need to avoid the obstacles presented within the reef
    (as fish cannot swim through stone or coral).
    """
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((20, 20), pg.SRCALPHA).convert_alpha()
        self.original_surf = self.surf
        self.color = (0, 0, 255)
        points = ((4, 18), (10, 2), (16, 18), (10, 12), (4, 18))
        pg.draw.polygon(self.surf, self.color, points)
        self.rect = self.surf.get_rect()
        self.rect.center = (10, 10)
        self.angle = randint(-180, 180)

        self.repulsion_vector = vec(0, 0)
        self.tangent_vector = vec(0, 0)
             
    def update(self, dt, speed):
        self.wrap()

        self.obstacle_avoidance()
        turn_direction = 0
        x_position = 0
        y_position = 0
        sin_angle = 0
        cos_angle = 0
        nearby_fishes = sorted([fish for fish in fishes if vec(fish.rect.center).distance_to(self.rect.center) < 100 and fish != self], 
                               key=lambda i: vec(i.rect.center).distance_to(self.rect.center))
        del nearby_fishes[5:]

        school_count = len(nearby_fishes)
        if school_count > 1:
            nearest_fish = vec(nearby_fishes[0].rect.center)
            for fish in nearby_fishes:
                x_position += fish.rect.centerx
                y_position += fish.rect.centery
                sin_angle += sin(radians(fish.angle))
                cos_angle += cos(radians(fish.angle))
            target_vector = (x_position / school_count, y_position / school_count)
            average_angle = degrees(atan2(sin_angle, cos_angle))
            self.boid_logic(nearest_fish, average_angle, target_vector)
            turn_direction = self.boid_logic(nearest_fish, average_angle, target_vector)
        self.move(dt, school_count, turn_direction, speed)
        self.rect.center = self.pos

    def boid_logic(self, nearest_fish, average_angle, target_vector):
        threshold_nearest_fish = 10
        if vec(self.rect.center).distance_to(vec(nearest_fish)) < threshold_nearest_fish:
            target_vector = nearest_fish
        else:
            target_vector = self.rect.center

        difference = vec(target_vector[0] - self.rect.center[0], target_vector[1] - self.rect.center[1])
        target_distance, target_angle = difference.as_polar()

        if target_distance < 20:
            target_angle = average_angle
        else:
            target_angle = self.angle

        angle_difference = (target_angle - self.angle)
        if abs(angle_difference) > 1:
            turn_direction = angle_difference
        else:
            turn_direction = 0

        if target_distance < 50 and target_vector == nearest_fish:
            if turn_direction < 0:
                turn_direction = turn_direction + 180
            else:
                turn_direction = turn_direction - 180
        return turn_direction

    def move(self, dt, school_count, turn_direction, speed=F_SPEED):
        turn_rate = 1
        if school_count == 0:
            self.angle += randint(-5, 5)
        
        if turn_direction != 0:
            self.angle += turn_rate * abs(turn_direction) / turn_direction + randint(-5, 5)
        
        steering_angle = self.obstacle_avoidance()
        self.angle += steering_angle

        self.rect = self.surf.get_rect(center=self.rect.center)
        self.dir = vec(1, 0).rotate(-self.angle).normalize()
        new_pos = self.pos + self.dir * (speed + (5 - school_count)**2) * dt
        self.pos = new_pos
        self.angle = degrees(atan2(-self.dir.y, self.dir.x))
        self.surf = pg.transform.rotate(self.original_surf, self.angle - 90)
        self.rect = self.surf.get_rect(center=self.rect.center)
        

    def wrap(self):
        if self.rect.left < 0:
            self.rect.right = WIDTH
            self.pos.x = self.rect.centerx
        if self.rect.right > WIDTH:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.centery
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
            self.pos.y = self.rect.centery

    def obstacle_avoidance(self, OBSTACLE_RANGE=OBSTACLE_RANGE, TANGENT_WEIGHT = 0.1):
        obstacle_range = 30
        steering_angle = 0
        if OBSTACLES == True:           
            for obstacle in obstacles:
                distance = vec(obstacle.pos).distance_to(self.rect.center)
                if distance < obstacle_range:
                    direction_to_obstacles = vec(obstacle.pos) - self.pos
                    tangent_vector = vec(-direction_to_obstacles.y, direction_to_obstacles.x)
                    obstacle_angle = tangent_vector.as_polar()[1]
                    steering_force = TANGENT_WEIGHT * (obstacle_range - distance)
                    steering_angle += obstacle_angle * steering_force
        return steering_angle

    def find_nearest_obstacle(self, obstacles):
        min_distance = float('inf')
        nearest_obstacle = None

        for obstacle in obstacles:
            distance = vec(obstacle.pos).distance_to(self.pos)
            if distance < min_distance:
                min_distance = distance
                nearest_obstacle = obstacle
        return nearest_obstacle.pos if nearest_obstacle else None

    def lerp(self, a, b, t):
        return a + (b - a) * t
    
    def draw(self, surface=displaysurface):
        surface.blit(self.surf, self.rect)

fish = Fish()

# -----------------------------------------------------------------------------
# Shark Class
# -----------------------------------------------------------------------------
class Shark(pg.sprite.Sprite):
    """
    The sharks will swim around the reef and attempt to catch the fish. The sharks
    will move according to the following rules:
    - seek: steer towards a school of fish
    - persuit: steer to intercept a fish
    - avoid: steer to avoid obstacles
    """

    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((40, 40), pg.SRCALPHA).convert_alpha()
        self.original_surf = self.surf
        self.color = (255, 0, 0)
        points = ((8, 36), (20, 4), (32, 36), (20, 24), (8, 36))
        pg.draw.polygon(self.surf, self.color, points)
        self.rect = self.surf.get_rect()
        self.rect.center = (20, 20)
        self.angle = randint(-180, 180)

    def update(self, S_RANGE=S_RANGE):
        self.wrap()
        nearby_school = [fish for fish in fishes if vec(fish.rect.center).distance_to(self.rect.center) < S_RANGE]
        if nearby_school:
            self.hunt(nearby_school)
        else:
            self.angle += randint(-5, 5)
        self.move(dt, speed=S_SPEED)

    def move(self, dt, speed=S_SPEED):
        self.dir = vec(1, 0).rotate(-self.angle).normalize()
        new_pos = self.pos + self.dir * speed * dt
        self.pos = new_pos
        self.angle = degrees(atan2(-self.dir.y, self.dir.x))
        self.surf = pg.transform.rotate(self.original_surf, self.angle - 90)
        self.rect = self.surf.get_rect(center=self.rect.center)

    def hunt(self, nearby_school):
        pass

    def wrap(self):
        if self.rect.left < 0:
            self.rect.right = WIDTH
            self.pos.x = self.rect.centerx
        if self.rect.right > WIDTH:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.centery
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
            self.pos.y = self.rect.centery

    def draw(self, surface=displaysurface):
        surface.blit(self.surf, self.rect)

shark = Shark()
# -----------------------------------------------------------------------------
# Spawn Fish and Shark:
# -----------------------------------------------------------------------------
def is_position_in_obstacle(pos, obstacles):
    for obstacle in obstacles:
        if pos [0] > obstacle.rect.left - 20 and pos[0] < obstacle.rect.right + 20:
            if pos[1] > obstacle.rect.top - 20 and pos[1] < obstacle.rect.bottom + 20:
                return True
    return False

def spawn_fish(obstacles):
    while True:
        pos = randint(0, WIDTH), randint(0, HEIGHT)
        if not is_position_in_obstacle(pos, obstacles):
            fish = Fish()
            fish.rect.center = pos
            fish.pos = vec(pos)
            return fish

def spawn_shark(obstacles):
    while True:
        pos = randint(0, WIDTH), randint(0, HEIGHT)
        if not is_position_in_obstacle(pos, obstacles):
            shark = Shark()
            shark.rect.center = pos
            shark.pos = vec(pos)
            return shark
# -----------------------------------------------------------------------------
# Game Loop:
# -----------------------------------------------------------------------------
obstacles, obstacle_positions = Obstacle.create_obstacles()

fishes = []
sharks = []

for _ in range(F_COUNT):
    new_fish = spawn_fish(obstacles)
    fishes.append(new_fish)

for _ in range(S_COUNT):
    new_shark = spawn_shark(obstacles)
    sharks.append(new_shark)

while True:
    dt = clock.tick(FPS) / 1000
    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            pg.exit()

    displaysurface.fill(BACKGROUND)
    if OBSTACLES == True:
        for obstacle in obstacles:
            displaysurface.blit(obstacle.surf, obstacle.rect)
            # pg.draw.circle(displaysurface, (255, 0, 0), obstacle.rect.center, OBSTACLE_RANGE, 2)

    for fish in fishes:
        fish.draw(displaysurface)
        fish.update(dt, F_SPEED)
        if RECT_FISH == True:
            pg.draw.rect(displaysurface, (0, 255, 0), fish.rect, 2)
        if RADIUS == True:
            pg.draw.circle(displaysurface, (255, 0, 0), (int(fish.pos.x), int(fish.pos.y)), 50, 2)
        if CLOSEST_OBSTACLE == True:
            if OBSTACLES == True:
                pg.draw.line(displaysurface, (0, 255, 0), fish.pos, fish.find_nearest_obstacle(obstacles), 2)
    
    for shark in sharks:
        shark.draw(displaysurface)
        shark.update(S_SPEED)
        if RECT_SHARK == True:
            pg.draw.rect(displaysurface, (0, 255, 0), shark.rect, 2)
        if CLOSEST_OBSTACLE == True:
            if OBSTACLES == True:
                pg.draw.line(displaysurface, (0, 255, 0), shark.pos, shark.find_nearest_obstacle(obstacles), 2)

    if GRID == True:
        grid.visualize_grid()

    pg.display.update()
    FramePerSec.tick(FPS)