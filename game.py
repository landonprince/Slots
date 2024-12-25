import pygame
from sys import exit
import random
import shapes

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Slots")
clock = pygame.time.Clock() 

def generate_shapes():
    points_copy = shapes.points[:]
    shape_list = []
    while points_copy:
        index = random.randint(0, len(points_copy) - 1)
        x, y = points_copy.pop(index)
        
        shape_type, color = shapes.get_random_shape()
        
        if shape_type == "square":
            shape = shapes.Square(color, x, y)
        elif shape_type == "circle":
            shape = shapes.Circle(color, x, y)
        elif shape_type == "triangle":
            shape = shapes.Triangle(color, x, y)
        elif shape_type == "diamond":
            shape = shapes.Diamond(color, x, y)
        else:
            raise ValueError(f"Invalid shape type: {shape_type}")
            
        shape_list.append(shape)
        
    return shape_list

outer_bg_x, outer_bg_y = 750, 550
inner_bg_x, inner_bg_y = 720, 520

outer_bg = pygame.Rect((screen.get_width() - outer_bg_x) // 2, 
                        (screen.get_height() - outer_bg_y) // 2, outer_bg_x, outer_bg_y)
inner_bg = pygame.Rect((screen.get_width() - inner_bg_x) // 2, 
                        (screen.get_height() - inner_bg_y) // 2, inner_bg_x, inner_bg_y)
side_bg = pygame.Rect(((screen.get_width() - inner_bg_x) // 2) + 510, 
                        (screen.get_height() - inner_bg_y) // 2, inner_bg_x - 510, inner_bg_y)

def draw_background():
    screen.fill("brown4")
    
    pygame.draw.rect(screen, (100, 70, 40), outer_bg, 20, 15)
    pygame.draw.rect(screen, "black", outer_bg, 5, 15)

    pygame.draw.rect(screen, "bisque4", inner_bg, 0, 10)
    pygame.draw.rect(screen, "burlywood4", side_bg, 0, 10)
    pygame.draw.rect(screen, "black", inner_bg, 5, 10)
    
    pygame.draw.line(screen, "black", (162, 40), (162, 558), 5)
    pygame.draw.line(screen, "black", (288, 40), (288, 558), 5)
    pygame.draw.line(screen, "black", (416, 40), (416, 558), 5)
    pygame.draw.line(screen, "black", (544, 40), (544, 558), 5)

    pygame.draw.line(screen, (100, 70, 40), (552, 40), (552, 560), 11)
    pygame.draw.line(screen, "black", (560, 40), (560, 558), 5)
    
spin_button = pygame.Rect(574, 458, 170, 85)
spin_button_color = (214, 207, 180)
spin_font = pygame.font.Font(None, 75)
spin_text = spin_font.render("SPIN", False, "black") 

x_button = pygame.Rect(705, 54, 40, 40)
x_button_color = (220, 20, 60)
x_font = pygame.font.Font(None, 45)
x_text = x_font.render("x", False, "black")

def draw_buttons():
    pygame.draw.rect(screen, spin_button_color, spin_button, 0, 30)
    pygame.draw.rect(screen, "black", spin_button, 5, 30)
    screen.blit(spin_text, (598, 479))
    
    pygame.draw.rect(screen, x_button_color, x_button, 0, 50)
    pygame.draw.rect(screen, "black", x_button, 5, 50)
    screen.blit(x_text, (717, 58))
    
def fill_board(shape_list):
    for shape in shape_list:
        shape.draw_shape(screen)
        
def print_shapes(shape_list):
    for shape in shape_list:
        shape.print_shape()
        
def check_row(y_pos, shape_list):
    row_shapes = [shape for shape in shape_list if shape.y == y_pos]
    row_shapes = sorted(row_shapes, key=lambda shape: shape.x)
    
    max_adjacent_shapes = []
    cur_adjacent_shapes = [row_shapes[0]]
    
    for i in range(len(row_shapes) - 1):
        if (row_shapes[i].type == row_shapes[i + 1].type) or \
           (row_shapes[i].color == row_shapes[i + 1].color):
            cur_adjacent_shapes.append(row_shapes[i + 1])
        else:
            if len(cur_adjacent_shapes) > len(max_adjacent_shapes):
                max_adjacent_shapes = cur_adjacent_shapes
            cur_adjacent_shapes = [row_shapes[i + 1]]
    
    if len(cur_adjacent_shapes) > len(max_adjacent_shapes):
        max_adjacent_shapes = cur_adjacent_shapes
        
    return max_adjacent_shapes
    
    
        
        
        
all_shapes = generate_shapes()

first_row_adjacent_shapes = check_row(73, all_shapes)
print_shapes(first_row_adjacent_shapes)

while True:
    draw_background()
    fill_board(all_shapes)
    draw_buttons()
    
    mouse_pos = pygame.mouse.get_pos()
    
    if spin_button.collidepoint(mouse_pos):
        spin_button_color = (184, 177, 150)
    else:
        spin_button_color = (214, 207, 180)
    if x_button.collidepoint(mouse_pos):
        x_button_color = (190, 20, 30)
    else:
        x_button_color = (220, 20, 60)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and spin_button.collidepoint(mouse_pos):
                all_shapes = generate_shapes()
            if event.button == 1 and x_button.collidepoint(mouse_pos):
                pygame.quit()
                exit()
                
    
    pygame.display.update()
    clock.tick(60)




