import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Slots")
clock = pygame.time.Clock() 

def generate_shapes():
    return
    
def draw_background():
    outer_bg_x, outer_bg_y = 750, 550
    inner_bg_x, inner_bg_y = 720, 520

    outer_bg = pygame.Rect((screen.get_width() - outer_bg_x) // 2,
                       (screen.get_height() - outer_bg_y) // 2, outer_bg_x, outer_bg_y)
    inner_bg = pygame.Rect((screen.get_width() - inner_bg_x) // 2, 
                       (screen.get_height() - inner_bg_y) // 2, inner_bg_x, inner_bg_y)

    screen.fill("brown4")
    
    pygame.draw.rect(screen, (100, 70, 40), outer_bg, 20, 15)
    pygame.draw.rect(screen, "black", outer_bg, 5, 15)

    pygame.draw.rect(screen, "burlywood4", inner_bg, 0, 10)
    pygame.draw.rect(screen, "black", inner_bg, 5, 10)
    
    divider_x = 160
    for _ in range(0, 4):
            pygame.draw.line(screen, "black", (divider_x, 40), (divider_x, 558), 5)
            divider_x += 128
    pygame.draw.line(screen, (100, 70, 40), (552, 40), (552, 560), 11)
    pygame.draw.line(screen, "black", (560, 40), (560, 558), 5)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    draw_background()

    pygame.display.update()
    clock.tick(60)




