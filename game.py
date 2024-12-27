import pygame
from sys import exit
import random
import shapes

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Slots")
clock = pygame.time.Clock() 

# return a list of 16 shapes of random type and color
def generate_shapes():
    points_copy = shapes.points[:] # create copy since we will be popping points
    shape_list = []
    
    # place random shapes at random points in the 4x4 grid
    while points_copy:
        index = random.randint(0, len(points_copy) - 1)
        x, y = points_copy.pop(index)
        
        shape_type, color = shapes.get_random_shape()
        
        # make specific shape object based on type and add to shape list
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

all_shapes = generate_shapes() # initialize list of random shapes

# dimensions of the outer background & inner background
outer_bg_x, outer_bg_y = 750, 550
inner_bg_x, inner_bg_y = 720, 520

# initialize rects for the outer, inner, & side backgrounds
outer_bg = pygame.Rect((screen.get_width() - outer_bg_x) // 2, 
                       (screen.get_height() - outer_bg_y) // 2, 
                        outer_bg_x, outer_bg_y)
inner_bg = pygame.Rect((screen.get_width() - inner_bg_x) // 2, 
                       (screen.get_height() - inner_bg_y) // 2, 
                        inner_bg_x, inner_bg_y)
side_bg = pygame.Rect((screen.get_width() - inner_bg_x) // 2 + 510, 
                      (screen.get_height() - inner_bg_y) // 2, 
                       inner_bg_x - 510, inner_bg_y)

# draw the game background
def draw_background():
    screen.fill("brown4") # fill the entire screen (red-brown)
    
    # draw outer background (dark-brown)
    pygame.draw.rect(screen, (100, 70, 40), outer_bg, 20, 15)
    pygame.draw.rect(screen, "black", outer_bg, 5, 15)

    # draw inner background (gray-brown)
    pygame.draw.rect(screen, "bisque4", inner_bg, 0, 10) 
    
    # draw side background (light-brown)
    pygame.draw.rect(screen, "burlywood4", side_bg, 0, 10)
    pygame.draw.rect(screen, "black", inner_bg, 5, 10)
    
    # draw vertical grid lines
    pygame.draw.line(screen, "black", (162, 40), (162, 558), 5)
    pygame.draw.line(screen, "black", (288, 40), (288, 558), 5)
    pygame.draw.line(screen, "black", (416, 40), (416, 558), 5)
    pygame.draw.line(screen, "black", (544, 40), (544, 558), 5)

    # draw inner background/side background boundary 
    pygame.draw.line(screen, (100, 70, 40), (552, 40), (552, 560), 11)
    pygame.draw.line(screen, "black", (560, 40), (560, 558), 5)

# initialize rect, color, & text for "spin" button
spin_button = pygame.Rect(574, 458, 170, 85)
spin_button_color = (214, 207, 180)
spin_font = pygame.font.Font(None, 75)
spin_text = spin_font.render("SPIN", False, "black") 

# initialize rect, color, & text for "x" button
x_button = pygame.Rect(705, 54, 40, 40)
x_button_color = (220, 20, 60)
x_font = pygame.font.Font(None, 45)
x_text = x_font.render("x", False, "black")

# draw the game buttons
def draw_buttons():
    # draw spin button (light-tan)
    pygame.draw.rect(screen, spin_button_color, spin_button, 0, 30)
    pygame.draw.rect(screen, "black", spin_button, 5, 30)
    screen.blit(spin_text, (598, 479))
    
    # draw x button (red)
    pygame.draw.rect(screen, x_button_color, x_button, 0, 50)
    pygame.draw.rect(screen, "black", x_button, 5, 50)
    screen.blit(x_text, (717, 58))

# draw all shapes on the grid polymorphically
def fill_board(shape_list):
    for shape in shape_list:
        shape.draw_shape(screen)
        
# print attributes of all shapes polymorphically
def print_shapes(shape_list):
    for shape in shape_list:
        shape.print_shape()

# return list of adjacent shapes in row/col that have same type or color
def check_row_col(pos, type, shape_list):
    # if we want to check a row, grab all 4 shapes in a specific row 
    if type == "row":
        row_col_shapes = [shape for shape in shape_list if shape.y == pos]
        row_col_shapes = sorted(row_col_shapes, key=lambda shape: shape.x)
    # if we want to check a col, grab all 4 shapes in a specific col
    else:
        row_col_shapes = [shape for shape in shape_list if shape.x == pos]
        row_col_shapes = sorted(row_col_shapes, key=lambda shape: shape.y)
    
    max_matching_shapes = []
    cur_matching_shapes = [row_col_shapes[0]]
    
    # iterate through the 4 shapes in the row or col 
    for i in range(len(row_col_shapes) - 1):
        # if the cur shape matches the next, add it to the cur matches list
        if (row_col_shapes[i].type == row_col_shapes[i + 1].type) or \
           (row_col_shapes[i].color == row_col_shapes[i + 1].color):
            cur_matching_shapes.append(row_col_shapes[i + 1])
        # if they do not match, update max and increment cur matches list
        else:
            if len(cur_matching_shapes) > len(max_matching_shapes):
                max_matching_shapes = cur_matching_shapes
            cur_matching_shapes = [row_col_shapes[i + 1]]
    
    # check the last pair of adjacent shapes
    if len(cur_matching_shapes) > len(max_matching_shapes):
        max_matching_shapes = cur_matching_shapes
        
    # if there are no matching shapes, return empty list
    if len(max_matching_shapes) == 1:
        return []
    
    return max_matching_shapes

def draw_line(matching_shapes):
    length = len(matching_shapes)
    if length != 0:
        pygame.draw.line(
            screen,
            "black",
            (matching_shapes[0].x + 95 // 2, 
             matching_shapes[0].y + 95 // 2),
            (matching_shapes[length - 1].x + 95 // 2, 
             matching_shapes[length - 1].y + 95 // 2),
            5
        )
    
def check_board(shape_list):
    first_row_matches = check_row_col(73, "row", shape_list)
    draw_line(first_row_matches)
    second_row_matches = check_row_col(193, "row", shape_list)
    draw_line(second_row_matches)
    third_row_matches = check_row_col(313, "row", shape_list)
    draw_line(third_row_matches)
    fourth_row_matches = check_row_col(433, "row", shape_list)
    draw_line(fourth_row_matches)
    
    first_col_matches = check_row_col(55, "col", shape_list)
    draw_line(first_col_matches)
    second_col_matches = check_row_col(178, "col", shape_list)
    draw_line(second_col_matches)
    third_col_matches = check_row_col(305, "col", shape_list)
    draw_line(third_col_matches)
    fourth_col_matches = check_row_col(434, "col", shape_list)
    draw_line(fourth_col_matches)

while True:
    # draw the game every frame
    draw_background() 
    draw_buttons()
    fill_board(all_shapes)
    check_board(all_shapes)
    
    mouse_pos = pygame.mouse.get_pos() # get mouse position every frame
    
    # if the mouse position collides with the "spin" button, change its color
    if spin_button.collidepoint(mouse_pos):
        spin_button_color = (184, 177, 150)
    else:
        spin_button_color = (214, 207, 180)
    # if the mouse position collides with the "x" button, change its color
    if x_button.collidepoint(mouse_pos):
        x_button_color = (190, 20, 30)
    else:
        x_button_color = (220, 20, 60)
    
    # iterate through user input every frame
    for event in pygame.event.get():
        # if the user closes the game window, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicks the "spin" button, regenerate random shapes
            if event.button == 1 and spin_button.collidepoint(mouse_pos):
                all_shapes = generate_shapes()
            # if the user clicks the "x" button, quit the game
            if event.button == 1 and x_button.collidepoint(mouse_pos):
                pygame.quit()
                exit()
    
    # update the display every frame
    pygame.display.update()
    clock.tick(60)




