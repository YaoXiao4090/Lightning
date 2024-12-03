import pygame
import math
import random

pygame.init()
resolution = (853, 480)
blue = (0, 0, 255)
pink = (255, 91, 175)
white = (255, 255, 255)
full_width, full_height = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Lightning")
clock = pygame.time.Clock()
player_input = {
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "shoot": False,
    "Exit": False,
    "Play": False,
}
score = 0
game_over = False
objects = []
bullets = []
enemy_bullets = []
enemies = []
explosions = []
FPS = 60
SSI = pygame.image.load("Arcade - Raiden Fighters - Raiden MK-II.png"
                        ).convert_alpha()
EMI = pygame.image.load("Arcade - Sengeki Striker - Enemy 01.png"
                        ).convert_alpha()
health_pic = pygame.image.load("health.png").convert_alpha()
player_ship_part = [1974, 5]
bullet_part = [1900, 447]
enemy_part = [163, 212]
Bound_x = (0, full_width)
Bound_y = (0, full_height)
dt = 0