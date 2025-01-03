import pygame
import math
import random
from Rotating_Circle import create_rotating_circle
from Circle_in_Circle import create_Circle_in_Circle
from Stacking_Circles import create_Stacking_Circles
from opening_circle import create_Circle_in_Circle2

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Fonts and images
font1 = pygame.font.Font('Blissful Thinking.otf', 70)
font2 = pygame.font.Font('Blissful Thinking.otf', 60)
play = pygame.image.load('play.png')
circ = pygame.image.load('circ.png')
resized_circ = pygame.transform.scale(circ, (60, 60))
resized_image = pygame.transform.scale(play, (200, 200))  # Resized play button image
obstacles1 = [] # obstacle array only for opeing screen

# Predefined fake obstacles for main game
fake_obstacles = [create_rotating_circle(0), create_Circle_in_Circle(0), create_Stacking_Circles(0)]

# Initialize obstacle pool for opening screen
def initialize_obstacles1():
    obstacle_pools = []
    start_x = 250
    obstacle_pools.append(create_Circle_in_Circle2(start_x))  # First obstacle
    return obstacle_pools


# Initialize obstacles for opening screen
obstacles1 = initialize_obstacles1()
center = obstacles1[0][0][0].image_rect.center

# Screen settings
screen_x = 500
screen_y = 800
fps = 60

# Colors
BLACK = (39, 39, 39)
WHITE = (255, 255, 255)
RED = (144, 13, 255)
GREEN = (50, 219, 240)
BLUE = (255, 1, 129)
YELLOW = (250, 225, 0)

# Game settings
base_y = 100
radius = 10
max_jump = 15
move = False
start_x = 200
start_score = 0
obstacle_limit = 6
game_colors = [RED, YELLOW, BLUE, GREEN]
obstacles = []
rotation_speed = math.radians(1)
current_score = 0
font = pygame.font.Font(None, 100)
game_start = False
game_over = False
player_die = False
scoreSound = False

# Sounds
pygame.mixer.music.load("background.mp3")
click_sound = pygame.mixer.Sound("click.mp3")
jump_sound = pygame.mixer.Sound("jump.mp3")
die_sound = pygame.mixer.Sound("die.mp3")
score_sound = pygame.mixer.Sound("scoring.mp3")
color_change_sound = pygame.mixer.Sound("colorChange.mp3")

# Generate random obstacles for main game
def random_obstacles(start_x):
    global obstacles
    random1 = random.randint(0, 2)
    random2 = random.randint(0, 2)
    random3 = random.randint(0, 2)

    # Create obstacles based on random selection
    next_start_y = start_x - fake_obstacles[random1][0][0].total_obstacle_length() - 200
    obstacle = create_obstacle(random1, next_start_y)
    obstacles.append(obstacle)

    next_start_y = obstacle[0][0].base_y - fake_obstacles[random2][0][0].total_obstacle_length() - 200
    obstacles.append(create_obstacle(random2, next_start_y))

    next_start_y = next_start_y - fake_obstacles[random3][0][0].total_obstacle_length() - 200
    obstacles.append(create_obstacle(random3, next_start_y))

# Initialize obstacle pool for main game
def initialize_obstacles():
    obstacle_pool = []
    start_x = 200
    obstacle_pool.append(create_rotating_circle(start_x - 200 * 0))  # First obstacle
    obstacle_pool.append(create_Circle_in_Circle(obstacle_pool[0][0][0].base_y - fake_obstacles[1][0][0].total_obstacle_length() - 200))
    obstacle_pool.append(create_Stacking_Circles(obstacle_pool[1][0][0].base_y - fake_obstacles[2][0][0].total_obstacle_length() - 200))
    return obstacle_pool

obstacles = initialize_obstacles() #get obstacles for main game
# Function to create obstacles based on type
def create_obstacle(obstacle_type, start_y):
    """
    Helper function to create obstacles based on their type.
    obstacle_type: int (0 = Rotating Circle, 1 = Circle in Circle, 2 = Stacking Circles)
    start_y: Starting y-position for the obstacle
    """
    if obstacle_type == 0:
        return create_rotating_circle(start_y)
    elif obstacle_type == 1:
        return create_Circle_in_Circle(start_y)
    elif obstacle_type == 2:
        return create_Stacking_Circles(start_y)

# Player class definition
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.temp_y = y
        self.radius = radius
        self.color = color
        self.max_jump = 9
        self.temp_max_jump = 9
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.up = False

    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        if self.up and not player_die:
            self.y -= 50
            jump_sound.play()
            self.up = False
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def gravity(self):
        if not self.up:
            self.y += 3
        if player_die:
            self.y += 5
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def max_distance(self):
        global move
        if self.y - (self.temp_y - self.max_jump) <= 0:
            return True

# Setup the screen and clock
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Color Switch")
clock = pygame.time.Clock()

# Player instance
player = Player(250, 600, RED)

# Function to update score
def score():
    global current_score
    for obstacle in obstacles:
        for circle in obstacle:
            for arc in circle:
                if player.rect.colliderect(arc.image_rect) and not arc.star_die and not arc.star_remove and arc.first_arc:
                    score_sound.play()
                    arc.star_die = True
                    current_score += 1

# Function to change color
def color_changer():
    num = random.randint(0, 3)
    for obstacle in obstacles:
        for circle in obstacle:
            for arc in circle:
                if player.rect.colliderect(arc.color_changer_image_rect) and arc.color_alive and arc.first_arc:
                    color_change_sound.play()
                    player.color = game_colors[num]
                    arc.color_alive = False
                    break

# Function to display the score
def display_score():
    score_text = font1.render(str(int(current_score)), True, WHITE)
    screen.blit(score_text, (425, 10))  # Display score

# Display opening screen
def display_opening_screen():
    score_text = font1.render(str("C    L    R"), True, WHITE)
    next_text = font1.render(str("SWITCH"), True, WHITE)
    screen.blit(score_text, (100 + 25, 100 - 50))
    screen.blit(resized_circ, (143 + 25, 105 - 50))
    screen.blit(resized_circ, (240 + 25, 105 - 50))
    screen.blit(next_text, (100 + 35, 115))
    for obstacle in obstacles1:
        for circle in obstacle:
            for arc in circle:
                arc.rotate()
                arc.display(screen)

    screen.blit(resized_image, (center[0] - 90, center[1] - 100))

# Display game over screen
def display_gameOver_screen():
    overlay = pygame.Surface((screen_x, screen_y))
    overlay.set_alpha(150)  # Set transparency (0-255, 255 is fully opaque)
    overlay.fill((50, 50, 50))  # Fill with gray color
    screen.blit(overlay, (0, 0))
    score_text = font1.render(str("GAME OVER"), True, WHITE)
    screen.blit(score_text, (70, 250))
    restart_text = font2.render(str("Press G to restart"), True, WHITE)
    screen.blit(restart_text, (35, 350))

# Restart the game
def restart():
    global obstacles, current_score, player, player_die, game_start, game_over
    obstacles = initialize_obstacles()
    current_score = 0
    player = Player(250, 600, RED)
    player_die = False
    game_start = False
    game_over = False

# Music and sound settings
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

# Game loop
running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if game_over:
        jump_sound.stop()
        die_sound.play()
        player_die = True
        game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.up = True
            if event.key == pygame.K_g and player_die:
                restart()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and (mouse_x >= (center[0] - 90) and mouse_x <= (center[0] - 90) + 200) and (mouse_y >= (center[1] - 100) and mouse_y <= (center[1] - 100) + 200):
                click_sound.play()
                game_start = True  # Start the game

    if game_start:
        screen.fill(BLACK)
        score()
        color_changer()
        player.max_distance()
        player.gravity()
        player.move()
        player.display()

        obstacles = [obs for obs in obstacles if obs[0][0].base_y < 900]

        if len(obstacles) < obstacle_limit and obstacles[-2][0][0].base_y >= 100:
            last_base_y = obstacles[-1][0][0].base_y
            start_x = last_base_y
            random_obstacles(start_x)

        for obstacle in obstacles:
            for circle in obstacle:
                for arc in circle:
                    arc.star_move()
                    if player.max_distance() and not player.up:
                        arc.move()
                    if arc.collision(player):
                        game_over = True
                    arc.get_coords(player.color)
                    arc.rotate()
                    arc.display(screen)

        display_score()

        if player_die:
            display_gameOver_screen()
    else:
        screen.fill(BLACK)
        display_opening_screen()

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
