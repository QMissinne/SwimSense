import pygame as pg
from pygame.locals import *
import random
from random import random, randint
import math
from math import pi
from math import cos, sin, radians, degrees, atan2

import time
import matplotlib.pyplot as plt

# initialise pygame:
pg.init()

# -----------------------------------------------------------------------------
# Setup:
# -----------------------------------------------------------------------------
vec = pg.math.Vector2
clock = pg.time.Clock()

# Display:
GRID = False
OBSTACLES = False
WIDTH = 1200
HEIGHT = 800
FPS = 60
BACKGROUND = (26, 193, 221)

# Obstacle Parameters:
O_RANGE = 100
O_RADIUS = 25
O_COUNT = 1

# Fish setup:
RECT_FISH = True
RADIUS = True
CLOSEST_OBSTACLE = False
F_COUNT = 50
F_SPEED = 100
F_RANGE = 100

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
    purely for visualisation purposes.
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
# Obstacle Class:
# -----------------------------------------------------------------------------
class Obstacle(pg.sprite.Sprite):
    """
    The obstacle class is used to define the obstacles within the reef. 
    This will create a barrier for the fish to navigate around. The obstacles 
    will be defined as black circles with a radius of O_Radius (variable).
    """
    def __init__(self, x , y, radius=O_RADIUS):
        super().__init__()
        self.surf = pg.Surface((radius*2, radius*2), pg.SRCALPHA).convert_alpha()
        pg.draw.circle(self.surf, (0, 0, 0), (radius, radius), radius)
        self.rect = self.surf.get_rect(center=(x, y))
        self.pos = vec(x, y)

    def create_obstacles():
            obstacles = []
            obstacle_positions = []
            for _ in range(O_COUNT):
                x = randint(0, WIDTH)
                y = randint(0, HEIGHT)
                obstacle = Obstacle(x, y)
                obstacles.append(obstacle)
                obstacle_positions.append((x, y))
            return obstacles, obstacle_positions


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
    The fish will also need to avoid the obstacles presented within the reef.
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
        self.vel = vec(F_SPEED, 0).rotate(-self.angle)
        self.in_obstacle = [False for _ in range(O_COUNT)]
        self.school_count = 0

             
    def update(self, dt, speed, F_RANGE=F_RANGE):
        self.wrap()
        turn_direction = 0
        x_position = 0
        y_position = 0
        sin_angle = 0
        cos_angle = 0
        nearby_fishes = sorted([fish for fish in fishes if vec(fish.rect.center).distance_to(self.rect.center) < F_RANGE and fish != self], 
                               key=lambda i: vec(i.rect.center).distance_to(self.rect.center))
        del nearby_fishes[5:]

        self.school_count = len(nearby_fishes)
        if self.school_count > 1:
            nearest_fish = vec(nearby_fishes[0].rect.center)
            for fish in nearby_fishes:
                x_position += fish.rect.centerx
                y_position += fish.rect.centery
                sin_angle += sin(radians(fish.angle))
                cos_angle += cos(radians(fish.angle))
            target_vector = (x_position / self.school_count, y_position / self.school_count)
            average_angle = degrees(atan2(sin_angle, cos_angle))
            self.boid_logic(nearest_fish, average_angle, target_vector)
            turn_direction = self.boid_logic(nearest_fish, average_angle, target_vector)
        self.move(dt, self.school_count, turn_direction, speed)
        self.rect.center = self.pos

    def boid_logic(self, nearest_fish, average_angle, target_vector):
        threshold_nearest_fish = 10
        if vec(self.rect.center).distance_to(vec(nearest_fish)) < threshold_nearest_fish:
            target_vector = nearest_fish
        else:
            target_vector = self.rect.center

        difference = vec(target_vector[0] - self.rect.center[0], target_vector[1] - self.rect.center[1])
        target_distance, target_angle = difference.as_polar()

        if target_distance < F_RANGE:
            target_angle = average_angle
        else:
            target_angle = self.angle

        angle_difference = (target_angle - self.angle)
        if abs(angle_difference) > 1:
            turn_direction = angle_difference
        else:
            turn_direction = 0

        if target_distance < F_RANGE and target_vector == nearest_fish:
            if turn_direction < 0:
                turn_direction = turn_direction + 180
            else:
                turn_direction = turn_direction - 180
        return turn_direction

    def move(self, dt, school_count, turn_direction, speed=F_SPEED):
        turn_rate = 2
        if school_count == 0:
            self.angle += randint(-5, 5)
        
        if turn_direction != 0:
            self.angle += turn_rate * abs(turn_direction) / turn_direction
        
        steering_angle = self.obstacle_avoidance()
        diff_angle =  self.angle - steering_angle
        if abs(diff_angle) > 70 and abs(diff_angle) < 90:
            scaling_factor = 1.75
        else:
            scaling_factor = 1.2
        if self.angle > 90  and self.angle < -90:
            self.angle += diff_angle*scaling_factor
        else:
            self.angle -= diff_angle*scaling_factor

        self.rect = self.surf.get_rect(center=self.rect.center)
        self.dir = vec(1, 0).rotate(-self.angle).normalize()
        new_pos = self.pos + self.dir * (speed + (5 - school_count)**2) * dt
        self.pos = new_pos
        self.angle = degrees(atan2(-self.dir.y, self.dir.x))
        self.surf = pg.transform.rotate(self.original_surf, self.angle - 90)
        self.rect = self.surf.get_rect(center=self.rect.center)

    def obstacle_avoidance(self, OBSTACLE_RANGE=O_RANGE):
        steering_angle = self.angle
        sin_obstacle = 0
        cos_obstacle = 0
        if OBSTACLES == True:           
            for i_obstacle, obstacle in enumerate(obstacles):
                distance = obstacle.pos.distance_to(self.rect.center)
                if distance < O_RANGE:
                    # if self.in_obstacle[i_obstacle] == False:
                    #     self.in_obstacle[i_obstacle] = True
                    direction_to_obstacles = obstacle.pos - self.pos
                    tangent_vector = vec(- direction_to_obstacles.y, direction_to_obstacles.x) # counterclockwise
                    scalar_prod = tangent_vector.x * cos(radians(self.angle)) + tangent_vector.y * sin(radians(self.angle))
                    if scalar_prod < 0:
                        tangent_vector = - tangent_vector
                    obstacle_angle = tangent_vector.as_polar()[1]
                    sin_obstacle += sin(radians(obstacle_angle))
                    cos_obstacle += cos(radians(obstacle_angle))
                    steering_angle = degrees(atan2(sin_obstacle, cos_obstacle))
                # else:
                #    self.in_obstacle[i_obstacle] = False
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

fish = Fish()

# -----------------------------------------------------------------------------
# Spawn Fish:
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
        
# -----------------------------------------------------------------------------
# Performance Evaluation:
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Game Loop:
# -----------------------------------------------------------------------------
O_RADIUS_values = list(range(10, 100, 10))
all_collision_counts = []

for O_RADIUS in O_RADIUS_values:
    O_RADIUS_collision_counts = []
    for _ in range(10):
        print(F"Running simulation with O_RADIUS = {O_RADIUS}")
        for _ in range(O_COUNT):
            obstacles, obstacle_positions = Obstacle.create_obstacles()

        fishes = []

        for _ in range(F_COUNT):
            new_fish = spawn_fish(obstacles)
            fishes.append(new_fish)

        start_time = time.time()
        collision_count = 0

        while time.time() - start_time < 60:
            dt = clock.tick(FPS) / 1000
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    pg.exit()

            displaysurface.fill(BACKGROUND)

            if OBSTACLES == True:
                for obstacle in obstacles:
                    displaysurface.blit(obstacle.surf, obstacle.rect)
                    pg.draw.circle(displaysurface, (255, 0, 0), obstacle.rect.center, O_RANGE, 2)

            for fish in fishes:
                fish.draw(displaysurface)
                fish.update(dt, F_SPEED)
                if RECT_FISH == True:
                    pg.draw.rect(displaysurface, (0, 255, 0), fish.rect, 2)
                if RADIUS == True:
                    pg.draw.circle(displaysurface, (255, 0, 0), (int(fish.pos.x), int(fish.pos.y)), F_RANGE, 2)
                if CLOSEST_OBSTACLE == True:
                    if OBSTACLES == True:
                        pg.draw.line(displaysurface, (0, 255, 0), fish.pos, fish.find_nearest_obstacle(obstacles), 2)

                for obstacle in obstacles:
                    if fish.rect.colliderect(obstacle.rect):
                        collision_count += 1

            if GRID == True:
                grid.visualize_grid()

            pg.display.update()
            FramePerSec.tick(FPS)

        O_RADIUS_collision_counts.append(collision_count)
        
    all_collision_counts.append(O_RADIUS_collision_counts)
    print(all_collision_counts)

average_collision_counts = [sum(counts) / len(counts) for counts in all_collision_counts]
print(f"averaged collision count is: {average_collision_counts}")

plt.plot(O_RADIUS_values, average_collision_counts)
plt.xlabel('O_RADIUS')
plt.ylabel('Averaged Collision Count')
plt.title('Collision Evaluation')
plt.show()