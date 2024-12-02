import pygame

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


def main():
    pygame.init()
    pygame.display.set_caption("Lightning")
    resolution = (853, 480)
    full_width, full_height = pygame.display.get_desktop_sizes()[0]
    BG_color = pygame.Color(255, 0, 255)
    Play = False
    Fullscreen = False
    Pause = False
    screen = pygame.display.set_mode(resolution)
    run = True
    while run:
        screen.fill(BG_color)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if Fullscreen == True and event.key == pygame.K_TAB:
                    pygame.display.toggle_fullscreen()
                    resolution = (853, 480)
                    screen = pygame.display.set_mode(resolution)
                    screen.fill(BG_color)
                    Fullscreen = False
                elif event.key == pygame.K_TAB:
                    resolution = (full_width, full_height)
                    screen = pygame.display.set_mode(resolution)
                    screen.fill(BG_color)
                    Fullscreen = True
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        menu_text(screen, resolution, font_size = 40, title_size = 80)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()