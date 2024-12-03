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

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        explode(self.x, self.y - 50)
        objects.remove(self)
        enemies.remove(self)


def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def menu_text(screen, resolution, font_size=40, title_size=80):
    font = pygame.font.SysFont("None", font_size)
    title = pygame.font.SysFont("None", title_size, bold=True)
    text_col = pygame.Color(255, 255, 255)
    title_col = pygame.Color(255, 255, 0)
    title_width, title_height = (
        resolution[0] / 2 - title_size * 1.5,
        resolution[1] / 2 - title_size,
    )
    draw_text(screen, "Lighting", title, title_col, title_width, title_height)
    draw_text(
        screen, "Enter to Start", font, text_col, title_width, title_height + title_size
    )
    draw_text(
        screen,
        "Esc to Exit",
        font,
        text_col,
        title_width,
        title_height + title_size + font_size,
    )


def get_image(sheet, part_W, part_H, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (part_W, part_H, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image


def check_input(key, value):
    if key == pygame.K_a:
        player_input["left"] = value
    if key == pygame.K_d:
        player_input["right"] = value
    if key == pygame.K_w:
        player_input["up"] = value
    if key == pygame.K_s:
        player_input["down"] = value
    if key == pygame.K_ESCAPE:
        player_input["Exit"] = value


def scrolling_BG(speed, screen, resolution):
    BG = pygame.image.load("BG_img.jpg").convert()
    BG_width = BG.get_width()
    BG_height = BG.get_height()
    tiles = math.ceil(resolution[0] / BG_width) + 1
    for i in range(0, tiles):
        screen.blit(BG, (i * BG_width + speed, 0))
    for i in range(0, tiles):
        screen.blit(BG, (i * BG_width + speed, BG_height))
    for i in range(0, tiles):
        screen.blit(BG, (i * BG_width + speed, BG_height * 2))
    return BG_width


def enemy_spawner():
    while True:
        for i in range(60):
            yield
        randomy = random.randint(0, full_height - 18)
        enemy = Enemy(full_width - 43, randomy, 43, 18, enemy_ship, 2)


bullet_img = get_image(SSI, bullet_part[0], bullet_part[1], 21, 5, 2, blue)
health_img = get_image(health_pic, 0, 5, 511, 515, 0.1, white)


def shoot():
    player_center = player.get_center()
    bullet = Object(player_center[0], player_center[1], 21, 5, bullet_img, 4)
    bullet.velocity = [5, 0]
    bullets.append(bullet)


def enemy_shoot():
    for e in enemies:
        enemy_center = e.get_center()
        enemy_bullet = Object(enemy_center[0], enemy_center[1], 21, 5, bullet_img, 3)
        enemy_bullet.velocity = [-5, 0]
        enemy_bullets.append(enemy_bullet)


def check_collision(obj1, obj2):
    x1, y1 = obj1.get_center()
    x2, y2 = obj2.get_center()
    w1, h1 = obj1.collider[0] / 2, obj1.collider[1] / 2
    w2, h2 = obj2.collider[0] / 2, obj2.collider[1] / 2
    if x1 + w1 > x2 - w2 and x1 - w1 < x2 + w2:
        return y1 + h1 > y2 - h2 and y1 - h1 < y2 + h2
    return False


def display_ui():
    img = health_img
    for i in range(player.max_health):
        if i < player.health:
            screen.blit(img, (i * 40 - player.max_health * 3, 20))
    font = pygame.font.SysFont("None", 40)
    loss_font = pygame.font.SysFont("None", 160)
    score_display = draw_text(
        screen, f"Score: {score}", font, white, full_width / 2 - 40, 20
    )

    if game_over:
        game_over_screen = draw_text(
            screen,
            "You Loss",
            loss_font,
            pink,
            full_width / 2 - 200,
            full_height / 2 - 80,
        )


def update_screen():
    clock.tick(FPS)
    pygame.display.update()


player_ship = get_image(SSI, player_ship_part[0], player_ship_part[1], 41, 19, 2, blue)
enemy_ship = get_image(EMI, enemy_part[0], enemy_part[1], 43, 18, 2, pink)


def explode(x, y):
    explosion = Object(x, y, 87, 87, pygame.image.load("enemy_explode.png"), 0)
    explosions.append(explosion)

