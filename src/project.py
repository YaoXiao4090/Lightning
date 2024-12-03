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


class Object:
    def __init__(self, x, y, width, height, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed
        self.velocity = [0, 0]
        self.collider = [width, height]

        objects.append(self)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()


class Player(Object):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image, speed)
        self.health = self.max_health = 3

    def update(self):
        super().update()

        self.x = max(Bound_x[0], min(self.x, Bound_x[1] - self.width))
        self.y = max(Bound_y[0], min(self.y, Bound_y[1] - self.height))


class Enemy(Object):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image, speed)

        self.health = 1
        enemies.append(self)

    def update(self):
        player_center = player.get_center()
        enemy_center = self.get_center()

        self.velocity = [
            player_center[0] - enemy_center[0],
            player_center[1] - enemy_center[1],
        ]
        magnitude = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        self.velocity = [
            self.velocity[0] / magnitude * self.speed,
            self.velocity[1] / magnitude * self.speed,
        ]

        super().update()