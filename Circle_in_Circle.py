import pygame
import math
from Rotating_Circle import create_rotating_circle
pygame.init()

BLACK = (39, 39, 39)
WHITE = (255, 255, 255)
RED = (144, 13, 255)
GREEN = (50, 219, 240)
BLUE = (255, 1, 129)
YELLOW = (250, 225, 0)
screen_x = 500
screen_y = 800
fps = 60
radius = 200
base_x = (screen_x - radius * 2) // 2
smallRadius = radius - 20
smallerRadius = smallRadius - 20
rotation_speed = math.radians(1)
small_rotation_speed = math.radians(3)
star = pygame.image.load('star sprite.png')
color_changer = pygame.image.load('colorChange.png')

class Arc:
    def __init__(self, color, base_x, base_y, start_angle, stop_angle, widthh, big, small, smaller, first):
        self.first_arc = first
        self.image = star
        self.resized_image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.resized_image.get_rect()
        self.color_changer_image = color_changer
        self.color_changer_resized_image = pygame.transform.scale(self.color_changer_image, (40, 40))
        self.color_changer_image_rect = self.color_changer_resized_image.get_rect()
        self.color = color
        self.base_x = base_x
        self.base_y = base_y
        self.temp_base_y = base_y
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.widthh = widthh
        self.coordsList = []
        self.big = big
        self.alive = True
        self.small = small
        self.smaller = smaller
        if self.big:
            self.rect = pygame.Rect(self.base_x, self.base_y, radius * 2, radius * 2)
        if self.small:
            self.rect = pygame.Rect(self.base_x + 20, self.base_y + 20, smallRadius * 2, smallRadius * 2)
        if self.smaller:
            self.rect = pygame.Rect(self.base_x + 20 + 20, self.base_y + 20 + 20, smallerRadius * 2, smallerRadius * 2)

        self.center = self.rect.center
        self.image_rect.center = self.center
        self.color_changer_image_rect.center = (self.center[0], (self.center[1] - radius) + self.total_obstacle_length() + 100)
        self.x = self.rect.topleft[0]
        self.y = self.rect.topleft[1]
        self.star_die = False
        self.star_remove = False
        self.og_y = self.image_rect.centery
        self.color_alive = True

    def display(self, screen):
        if self.alive:
            pygame.draw.arc(screen, self.color, self.rect, self.start_angle, self.stop_angle, self.widthh)
            if not self.star_remove and self.big and self.first_arc:
                screen.blit(self.resized_image, self.image_rect)
            if self.first_arc and self.color_alive and self.big:
                screen.blit(self.color_changer_resized_image, self.color_changer_image_rect)

    def get_coords(self, player_color):
        self.coordsList.clear()
        if self.color == player_color:
            pass
        step_size = math.radians(1)  # Adjust step size for precision
        #coordsList = []
        angle = self.start_angle + math.radians(90)
        while angle <= self.stop_angle + math.radians(90):
            x = self.center[0] + radius * math.sin  (angle)
            y = self.center[1] + radius * math.cos(angle)
            self.coordsList.append((int(x), int(y)))  # Use integers for screen coordinates
            angle += step_size
        #return coordsList

    def rotate(self):
        if self.big:
            self.start_angle += rotation_speed
            self.stop_angle += rotation_speed
        elif self.small:
            self.start_angle += small_rotation_speed
            self.stop_angle += small_rotation_speed
        elif self.smaller:
            self.start_angle += rotation_speed
            self.stop_angle += rotation_speed



    def collision(self, other):
        global running
        if self.color != other.color:
            for center in self.coordsList:
                # Check collision with each point on the arc
                if math.sqrt((other.x - center[0]) ** 2 + (other.y - center[1]) ** 2) <= other.radius:
                    return True
                    break

    def move(self):
        self.base_y = self.temp_base_y + 2
        self.temp_base_y = self.base_y
        self.updateRect()
        if self.base_y >= 850:
            self.alive = False

    def updateRect(self):
        if self.big:
            self.rect = pygame.Rect(self.base_x, self.base_y, radius * 2, radius * 2)
        if self.small:
            self.rect = pygame.Rect(self.base_x + 20, self.base_y + 20, smallRadius * 2, smallRadius * 2)
        if self.smaller:
            self.rect = pygame.Rect(self.base_x + 20 + 20, self.base_y + 20 + 20, smallerRadius * 2, smallerRadius * 2)
        self.center = self.rect.center
        if not self.star_die and self.big and self.first_arc:
            self.image_rect.center = self.center
        if self.first_arc and self.color_alive and self.big:
            self.color_changer_image_rect.center = (self.center[0], (self.center[1] - radius) + self.total_obstacle_length() + 100)

    def star_move(self):
        if self.star_die and self.big:
            self.image_rect.centerx += 10  # Move right
            self.image_rect.centery -= 15
        if self.image_rect.centery < self.og_y - 500 and self.big and self.first_arc:
            self.star_remove = True

    def total_obstacle_length(self):
        return radius * 2

def create_Circle_in_Circle(base_y):
    base_x = (screen_x - radius * 2) // 2
    base_y = base_y

    circle = [Arc(RED, base_x, base_y, math.radians(0), math.radians(90), 10, True, False, False, True),
              Arc(GREEN, base_x, base_y,math.radians(90), math.radians(180), 10, True, False, False, False),
              Arc(BLUE, base_x, base_y, math.radians(180), math.radians(270), 10, True, False, False, False),
              Arc(YELLOW,base_x, base_y, math.radians(270), math.radians(360), 10, True, False, False, False)]

    smallCircle = [Arc(RED, base_x, base_y, math.radians(0), math.radians(90), 10, False, True, False, False),
                   Arc(GREEN, base_x, base_y, math.radians(90), math.radians(180), 10, False, True, False, False),
                   Arc(BLUE, base_x, base_y, math.radians(180), math.radians(270), 10, False, True, False, False),
                   Arc(YELLOW, base_x, base_y, math.radians(270), math.radians(360), 10, False, True, False, False)]

    smallerCircle = [Arc(RED, base_x, base_y, math.radians(0), math.radians(90), 10, False, False, True, False),
                     Arc(GREEN, base_x, base_y, math.radians(90), math.radians(180), 10, False, False, True, False),
                     Arc(BLUE, base_x, base_y, math.radians(180), math.radians(270), 10, False, False, True, False),
                     Arc(YELLOW, base_x, base_y, math.radians(270), math.radians(360), 10, False, False, True, False)]

    return [circle, smallCircle, smallerCircle]





