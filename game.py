from sys import exit
import pygame
import random
import shapes
import graph

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Reroll")
clock = pygame.time.Clock() 

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
    screen.fill((150, 20, 50)) # fill the entire screen (red-brown)
    
    # draw outer background (dark-brown)
    pygame.draw.rect(screen, (110, 80, 50), outer_bg, 20, 15)
    pygame.draw.rect(screen, "black", outer_bg, 5, 15)

    # draw inner background (gray-brown)
    pygame.draw.rect(screen, (145, 130, 115), inner_bg, 0, 10) 
    
    # draw side background (light-brown)
    pygame.draw.rect(screen, (150, 125, 95), side_bg, 0, 10)
    pygame.draw.rect(screen, "black", inner_bg, 5, 10)
    
    # draw vertical grid lines
    pygame.draw.line(screen, "black", (163, 40), (163, 558), 5)
    pygame.draw.line(screen, "black", (288, 40), (288, 558), 5)
    pygame.draw.line(screen, "black", (416, 40), (416, 558), 5)
    pygame.draw.line(screen, "black", (544, 40), (544, 558), 5)

    # draw inner background/side background boundary 
    pygame.draw.line(screen, (110, 80, 50), (552, 40), (552, 560), 11)
    pygame.draw.line(screen, "black", (560, 40), (560, 558), 5)

# initialize rect, color, & text for "spin" button
spin_button = pygame.Rect(574, 475, 170, 70)
spin_button_color = (214, 207, 180)
spin_font = pygame.font.Font(None, 65)
spin_text = spin_font.render("Reroll", False, "black") 

# initialize rect, color, & text for "x" button
x_button = pygame.Rect(745, 15, 40, 40)
x_button_color = (220, 20, 60)
x_font = pygame.font.Font(None, 45)
x_text = x_font.render("x", False, "black")

# draw the game buttons
def draw_buttons():
    # draw spin button (light-tan)
    pygame.draw.rect(screen, spin_button_color, spin_button, 0, 30)
    pygame.draw.rect(screen, "black", spin_button, 5, 30)
    screen.blit(spin_text, (595, 490))
    
    # draw x button (red)
    pygame.draw.rect(screen, x_button_color, x_button, 0, 50)
    pygame.draw.rect(screen, "black", x_button, 5, 50)
    screen.blit(x_text, (757, 19))

scoreboard = pygame.Rect(574, 55, 170, 411)
scoreboard_color = (214, 207, 180)

def draw_scoreboard():
    pygame.draw.rect(screen, scoreboard_color, scoreboard, 0, 15)
    pygame.draw.rect(screen, "black", scoreboard, 5, 15)

# return a list of 16 shapes of random type & color
def generate_shapes():
    points_copy = shapes.points[:] # create copy since we will be popping points
    shape_list = []
    
    # place random shapes at random points in the 4x4 grid
    while points_copy:
        index = random.randint(0, len(points_copy) - 1)
        x, y = points_copy.pop(index)
        
        shape_type, color = shapes.get_random_shape()
        
        # make specific shape object based on type & add to shape list
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

all_shapes = generate_shapes() # initialize all random shapes

# draw all shapes on the grid polymorphically
def fill_board(shape_list):
    for shape in shape_list:
        shape.draw_shape(screen)
        
# print attributes of all shapes polymorphically
def print_shapes(shape_list):
    for shape in shape_list:
        shape.print_shape()

# return list of adjacent shapes in row/col that have same type or color
def get_matching_shapes(pos, type, shape_list):
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
        if (row_col_shapes[i].type == row_col_shapes[i + 1].type):
            cur_matching_shapes.append(row_col_shapes[i + 1])
        # if they do not match, update max & increment cur matches list
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

# return a list of dictionaries containing information about each line
def generate_lines(shape_list):
    lines = [] # stores a dictionary of information for each line
    
    # add horizontal line information to lines list 
    row_positions = [73, 193, 313, 433]
    for row_pos in row_positions:
        matching_shapes = get_matching_shapes(row_pos, "row", shape_list)
        if matching_shapes:
            # append dictionary containing line info to lines list
            lines.append({
                "shapes": matching_shapes,
                "color": "black", 
                "coords": (
                    # start x,y
                    matching_shapes[0].x + 95 // 2, 
                    matching_shapes[0].y + 95 // 2,
                    # end x,y
                    matching_shapes[-1].x + 95 // 2, 
                    matching_shapes[-1].y + 95 // 2
                )
            })
    
    # add vertical line information to lines list
    col_positions = [55, 178, 305, 434]
    for col_pos in col_positions:
        matching_shapes = get_matching_shapes(col_pos, "col", shape_list)
        if matching_shapes:
            # append dictionary containing line info to lines list
            lines.append({
                "shapes": matching_shapes,
                "color": "black", 
                "coords": (
                    # start x,y
                    matching_shapes[0].x + 95 // 2, 
                    matching_shapes[0].y + 95 // 2,
                    # end x,y
                    matching_shapes[-1].x + 95 // 2, 
                    matching_shapes[-1].y + 95 // 2
                )
            })
            
    return lines

# initialize all lines & the shapes in each component
all_lines = generate_lines(all_shapes)
component_shapes = graph.get_component_shapes(all_lines)

    
log_font = pygame.font.Font(None, 23)
final_score_font = pygame.font.Font(None, 40)

def render_log(component_shapes):
    # Define the points associated with each RGB color tuple
    color_points = {
        (185, 117, 60): 1,  # Bronze
        (180, 180, 180): 3,  # Silver
        (212, 168, 55): 5,   # Gold
        (80, 160, 85): 10  # Diamond
    }

    # Define a reverse mapping from RGB to color names
    color_names = {
        (185, 117, 60): "Bronze",
        (180, 180, 180): "Silver",
        (212, 168, 55): "Gold",
        (80, 160, 85): "Diamond"
    }

    x_offset, y_offset = 587, 67  # Initial position for the log
    all_totals = []  # To store final totals for each line

    for idx, (component_number, shapes) in enumerate(component_shapes.items()):
        component_total = 0
        shape_count = len(shapes)  # Number of shapes in the component

        # Render each shape in the component
        for shape in shapes:
            points = color_points.get(shape.color, 0)
            color_name = color_names.get(shape.color, "unknown")
            component_total += points

            # Render the log for the shape
            text_surface = log_font.render(f"{component_number + 1}. {color_name} +{points}", True, (0, 0, 0))
            screen.blit(text_surface, (x_offset, y_offset))
            y_offset += 14  # Move down for the next log string

        # Calculate the total for the component
        final_total = component_total * shape_count
        all_totals.append(final_total)

        # Draw a horizontal divider line, except for the last component

        y_offset += 3
        pygame.draw.line(screen, "black", (x_offset, y_offset), (729, y_offset), 2)
        y_offset += 5  # Add spacing below the line
            
        # Render the total points for the component
        total_surface = log_font.render(
            f"Line {component_number + 1}: {component_total} x {shape_count} = {final_total}",
            True,
            (0, 0, 0),
        )
        screen.blit(total_surface, (x_offset, y_offset))
        y_offset += 17  # Add spacing below the total points

        # Draw a horizontal divider line, except for the last component
        pygame.draw.line(screen, "black", (x_offset, y_offset), (729, y_offset), 2)
        y_offset += 5  # Add spacing below the line


    # Calculate and display the grand total
    grand_total = sum(all_totals)
    final_total_surface = final_score_font.render(
        f"Score: {grand_total}",
        True,
        (0, 0, 0),
    )
    screen.blit(final_total_surface, (x_offset, y_offset))
    
# draw all lines connecting matching shapes
def draw_lines(lines):
    for line_info in lines:
        x1, y1, x2, y2 = line_info["coords"]
        color = line_info["color"]
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)
    
while True:
    # generate game structure & state
    draw_background() 
    draw_scoreboard()
    draw_buttons()
    fill_board(all_shapes)
    draw_lines(all_lines)
    render_log(component_shapes)
    
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
                all_lines = generate_lines(all_shapes)
                component_shapes = graph.get_component_shapes(all_lines)
            # if the user clicks the "x" button, quit the game
            if event.button == 1 and x_button.collidepoint(mouse_pos):
                pygame.quit()
                exit()
    
    # update the display every frame
    pygame.display.update()
    clock.tick(60)




