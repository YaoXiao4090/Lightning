import pygame
import math

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def menu_text(screen, resolution, font_size = 40, title_size = 80):
    font = pygame.font.SysFont("None", font_size)
    title = pygame.font.SysFont("None", title_size, bold = True)
    text_col = pygame.Color(255, 255, 255)
    title_col = pygame.Color(255, 255, 0)
    title_width, title_height = (resolution[0]/2 - title_size * 1.5, 
                                 resolution[1]/2 - title_size * 1.5)
    draw_text(screen, "Lighting",
                title, title_col, title_width, title_height)
    draw_text(screen, "Enter to Start",
                font, text_col, title_width, title_height + title_size)
    draw_text(screen, "Esc to Exit",
                font, text_col, title_width, title_height + title_size + font_size)
    draw_text(screen, "Tab to Fullscreen",
                font, text_col, title_width, title_height + title_size + font_size * 2)
    draw_text(screen, "Space to Pause",
                font, text_col, title_width, title_height + title_size + font_size * 3)

def scrolling_BG(speed, screen, resolution, Fullscreen):
    BG = pygame.image.load("BG_img.jpg").convert()
    BG_width = BG.get_width()
    BG_height = BG.get_height()
    tiles = math.ceil(resolution[0] / BG_width) + 1
    for i in range(0, tiles):
        screen.blit(BG, (i * BG_width + speed, 0))
    if Fullscreen == True:
        for i in range(0, tiles):
            screen.blit(BG, (i * BG_width + speed, BG_height))
        for i in range(0, tiles):
            screen.blit(BG, (i * BG_width + speed, BG_height * 2))
    return BG_width

def pause_menu(screen, resolution, font_size = 160):
    text_font = pygame.font.SysFont("None", font_size, bold = True)
    text_col = pygame.Color(255, 255, 0)
    text_width, text_height = (resolution[0]/2 - font_size * 1.5, 
                                 resolution[1]/2 - font_size/2)
    draw_text(screen, "Paused",
                text_font, text_col, text_width, text_height)
    
def main():
    pygame.init()
    pygame.display.set_caption("Lightning")
    clock = pygame.time.Clock()
    FPS = 60
    resolution = (853, 480)
    screen = pygame.display.set_mode(resolution)
    full_width, full_height = pygame.display.get_desktop_sizes()[0]
    scroll = 0
    Play = False
    Fullscreen = False
    Pause = False
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if Fullscreen == True and event.key == pygame.K_TAB:
                    pygame.display.toggle_fullscreen()
                    resolution = (853, 480)
                    screen = pygame.display.set_mode(resolution)
                    Fullscreen = False
                elif event.key == pygame.K_TAB:
                    resolution = (full_width, full_height)
                    screen = pygame.display.set_mode(resolution)
                    Fullscreen = True
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    run = False
                elif Play == False and event.key == pygame.K_RETURN:
                    Play = True
                elif Pause == False and event.key == pygame.K_SPACE:
                    Pause = True
                elif event.key == pygame.K_SPACE:
                    Pause = False
            if event.type == pygame.QUIT:
                run = False
        if Play == True and Pause == False:
            scroll -= 5
        BG_width = scrolling_BG(scroll, screen, resolution, Fullscreen)
        if abs(scroll) > BG_width:
            scroll = 0
        if Play == False:
            menu_text(screen, resolution, font_size = 40, title_size = 80)
        if Play == True and Pause == True:
            pause_menu(screen, resolution, font_size = 160)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()