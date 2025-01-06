from sys import exit
import pygame
import random
import shapes
import graph


pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Reroll")
clock = pygame.time.Clock() 


# BACKGROUND ------------------------------------------------------------------


# Initialize background rects
outer_bg_x, outer_bg_y = 750, 550
inner_bg_x, inner_bg_y = 720, 520

outer_bg = pygame.Rect((screen.get_width() - outer_bg_x) // 2, 
                       (screen.get_height() - outer_bg_y) // 2, 
                        outer_bg_x, outer_bg_y)
inner_bg = pygame.Rect((screen.get_width() - inner_bg_x) // 2, 
                       (screen.get_height() - inner_bg_y) // 2, 
                        inner_bg_x, inner_bg_y)
side_bg = pygame.Rect((screen.get_width() - inner_bg_x) // 2 + 510, 
                      (screen.get_height() - inner_bg_y) // 2, 
                       inner_bg_x - 510, inner_bg_y)

scoreboard_bg = pygame.Rect(574, 55, 170, 411)


def draw_background():
    """
    Fills the screen, draws the inner, outer, and side backgrounds, 
    draws the vertical grid lines, and draws the scoreboard background.
    """
    screen.fill((125, 160, 185)) 
    
    # Outer background
    pygame.draw.rect(screen, (110, 80, 50), outer_bg, 20, 15)
    pygame.draw.rect(screen, "black", outer_bg, 5, 15)

    # Inner background
    pygame.draw.rect(screen, (145, 130, 115), inner_bg, 0, 10) 
    
    # Side background
    pygame.draw.rect(screen, (150, 125, 95), side_bg, 0, 10)
    pygame.draw.rect(screen, "black", inner_bg, 5, 10)
    
    # Vertical grid lines
    pygame.draw.line(screen, "black", (163, 40), (163, 558), 5)
    pygame.draw.line(screen, "black", (288, 40), (288, 558), 5)
    pygame.draw.line(screen, "black", (416, 40), (416, 558), 5)
    pygame.draw.line(screen, "black", (544, 40), (544, 558), 5)

    # Inner background and side background boundary 
    pygame.draw.line(screen, (110, 80, 50), (552, 40), (552, 560), 11)
    pygame.draw.line(screen, "black", (560, 40), (560, 558), 5)
    
    # Scoreboard background
    pygame.draw.rect(screen, (214, 207, 180), scoreboard_bg, 0, 15)
    pygame.draw.rect(screen, "black", scoreboard_bg, 5, 15)


# BUTTONS ---------------------------------------------------------------------


# Initialize button rects and text
reroll_button = pygame.Rect(574, 475, 170, 70)
reroll_button_color = (155, 191, 155)
reroll_font = pygame.font.Font(None, 65)
reroll_text = reroll_font.render("Reroll", False, "black") 

x_button = pygame.Rect(745, 15, 40, 40)
x_button_color = (155, 191, 155)
x_font = pygame.font.Font(None, 45)
x_text = x_font.render("x", False, "black")


def draw_buttons():
    """
    Draws the "Reroll" and "x" buttons.
    """
    # "Reroll" button
    pygame.draw.rect(screen, reroll_button_color, reroll_button, 0, 30)
    pygame.draw.rect(screen, "black", reroll_button, 5, 30)
    screen.blit(reroll_text, (595, 490))
    
    # "X" button
    pygame.draw.rect(screen, x_button_color, x_button, 0, 50)
    pygame.draw.rect(screen, "black", x_button, 5, 50)
    screen.blit(x_text, (757, 19))


# SHAPES ----------------------------------------------------------------------


def generate_shapes():
    """
    Generates 16 shapes of random type and color, where each
    is randomly assigned a position in the 4x4 grid.
    
    Returns:
        list: A list containing 16 Shape subclass objects (either
        Square, Circle, Triangle, or Diamond objects).
    """
    points_copy = shapes.points[:] 
    shape_list = []
    
    # Generate random shapes until each position in the 4x4 grid is filled
    while points_copy:
        index = random.randint(0, len(points_copy) - 1)
        x, y = points_copy.pop(index)
        
        shape_type, shape_color = shapes.get_random_shape()
        
        # Make a specific Shape subclass object based on shape type
        if shape_type == "square":
            shape = shapes.Square(shape_color, x, y)
        elif shape_type == "circle":
            shape = shapes.Circle(shape_color, x, y)
        elif shape_type == "triangle":
            shape = shapes.Triangle(shape_color, x, y)
        elif shape_type == "diamond":
            shape = shapes.Diamond(shape_color, x, y)
        else:
            raise ValueError(f"Invalid shape type: {shape_type}")
            
        shape_list.append(shape)
        
    return shape_list


def draw_shapes(shape_list):
    """
    Draws the 16 shapes from shape_list polymorphically.
    
    Parameters:
        shape_list (list): A list containing 16 Shape subclass objects.
    """
    for shape in shape_list:
        shape.draw_shape(screen)
        

def get_matching_shapes(pos, type, shape_list):
    """
    From shape_list, create a list of all adjacent shapes in the same
    row or column that have the same shape type.
    
    Parameters:
        pos (int): The row y position or column x position.
        type (str): "row" or "col".
        shape_list (list): A list containing 16 Shape subclass objects.
        
    Returns:
        list: A list containing Shape subclass objects that are
        adjacent and have the same shape type.
    """
    # Get all 4 shapes in a row or column based on type parameter
    if type == "row":
        row_col_shapes = [shape for shape in shape_list if shape.y == pos]
        row_col_shapes = sorted(row_col_shapes, key=lambda shape: shape.x)
    else:
        row_col_shapes = [shape for shape in shape_list if shape.x == pos]
        row_col_shapes = sorted(row_col_shapes, key=lambda shape: shape.y)
    
    matching_shapes = []
    cur_matching_shapes = [row_col_shapes[0]]
    
    # Iterate through the 4 shapes and append matching shapes
    for i in range(len(row_col_shapes) - 1):
        if (row_col_shapes[i].type == row_col_shapes[i + 1].type):
            cur_matching_shapes.append(row_col_shapes[i + 1])
        else:
            if len(cur_matching_shapes) > len(matching_shapes):
                matching_shapes = cur_matching_shapes
            cur_matching_shapes = [row_col_shapes[i + 1]]
    
    # Check the last pair of adjacent shapes
    if len(cur_matching_shapes) > len(matching_shapes):
        matching_shapes = cur_matching_shapes
        
    if len(matching_shapes) == 1:
        return []
    
    return matching_shapes


# LINES -----------------------------------------------------------------------


def generate_lines(shape_list):
    """
    Generates a list of dictionaries (one for each line) containing the
    matching shapes and the start/end position for that line.
    
    Parameters:
        shape_list (list): A list containing 16 Shape subclass objects.
        
    Returns:
        list: A list of dictionaries, where each dictionary contains:
            - "shapes": The matching shapes forming the line.
            - "coords": A tuple with the start and end coords of the line.
    """
    lines = []
    
    # Add horizontal line information to lines list 
    row_positions = [73, 193, 313, 433]
    for row_pos in row_positions:
        
        matching_shapes = get_matching_shapes(row_pos, "row", shape_list)
        
        if matching_shapes:
            # Append dictionary containing line info to lines list
            lines.append({
                "shapes": matching_shapes,
                "coords": (
                    matching_shapes[0].x + 95 // 2, 
                    matching_shapes[0].y + 95 // 2,
                    matching_shapes[-1].x + 95 // 2, 
                    matching_shapes[-1].y + 95 // 2
                )
            })
            
    # Add vertical line information to lines list
    col_positions = [55, 178, 305, 434]
    for col_pos in col_positions:
        
        matching_shapes = get_matching_shapes(col_pos, "col", shape_list)
        
        if matching_shapes:
            # Append dictionary containing line info to lines list
            lines.append({
                "shapes": matching_shapes,
                "coords": (
                    matching_shapes[0].x + 95 // 2, 
                    matching_shapes[0].y + 95 // 2,
                    matching_shapes[-1].x + 95 // 2, 
                    matching_shapes[-1].y + 95 // 2
                )
            })
            
    return lines


def draw_lines(lines):
    """
    Draws all lines connecting matching shapes.
    
    Parameters:
        lines (list): A list of dictionaries containing line info.
    """
    for line_info in lines:
        x1, y1, x2, y2 = line_info["coords"]
        pygame.draw.line(screen, "black", (x1, y1), (x2, y2), 5)
    

# LOG -------------------------------------------------------------------------


# initialize fonts, color to name mapping, and color to points mapping
log_font = pygame.font.Font(None, 23)
score_font = pygame.font.Font(None, 40)

color_names = {
    (185, 117, 60): "Bronze",
    (180, 180, 180): "Silver",
    (212, 168, 55): "Gold",
    (80, 160, 85): "Emerald"
}
color_points = {
    (185, 117, 60): 1,  
    (180, 180, 180): 3,  
    (212, 168, 55): 5,  
    (80, 160, 85): 10
}


def generate_log(component_shapes):
    """
    Generate log data for each connected component and their shapes.
    
    Parameters:
        component_shapes (dict): A dictionary containing connected 
        components and their associated shapes.
        
    Returns:
        dict: A dictionary of log data containing:
            - "log_entries": A list of strings for each log entry.
            - "totals": A list of total points for each component.
            - "grand_total": The final score for all components.
    """
    log_data = {
        "log_entries": [],
        "totals": [],
        "grand_total": 0
    }

    for component_number, shapes in component_shapes.items():
        component_total = 0
        shape_count = len(shapes)

        # Generate log entries for each shape in the component
        for shape in shapes:
            points = color_points.get(shape.color, 0)
            color_name = color_names.get(shape.color, "unknown")
            component_total += points

            # Add individual shape log entry
            log_data["log_entries"].append(
                f"{component_number + 1}. {color_name} +{points}")

        # Calculate the total for the component
        final_total = component_total * shape_count
        log_data["totals"].append(final_total)

        # Add total log entry for the component
        log_data["log_entries"].append(
            f"Line {component_number + 1}: {component_total} x " \
                f"{shape_count} = {final_total}"
        )

    # Calculate the grand total
    log_data["grand_total"] = sum(log_data["totals"])
    return log_data


def draw_log(log_data):
    """
    Draw the generated log data onto the screen.
    
    Parameters:
        log_data (dict): A dictionary containing log data for rendering. Keys:
            - 'log_entries': A list of strings for each log entry.
            - 'totals': A list of final totals for each component.
            - 'grand_total': The total score for all components combined.
    """
    x_offset, y_offset = 587, 67  # Initial position for the log

    # Render each log entry
    for entry in log_data["log_entries"]:
        if "Line" in entry:
            y_offset += 3
            pygame.draw.line(screen, "black", (x_offset, y_offset), (729, y_offset), 2)
            y_offset += 5  # Add spacing below the line
            
        # Render the log entry
        text_surface = log_font.render(entry, True, (0, 0, 0))
        screen.blit(text_surface, (x_offset, y_offset))
        y_offset += 14  # Move down for the next log entry

        # Add a divider line after component totals
        if "Line" in entry:
            y_offset += 3
            pygame.draw.line(screen, "black", (x_offset, y_offset), (729, y_offset), 2)
            y_offset += 5  # Add spacing below the line

    # Render the grand total
    final_total_surface = score_font.render(
        f"Score: {log_data['grand_total']}",
        True,
        (0, 0, 0),
    )
    screen.blit(final_total_surface, (x_offset, y_offset))



# initialize all lines and the shapes in each component
all_shapes = generate_shapes() # initialize all random shapes
all_lines = generate_lines(all_shapes)
component_shapes = graph.get_component_shapes(all_lines)
log_data = generate_log(component_shapes)

    



    

while True:
    # generate game structure and state
    draw_background() 
    draw_buttons()
    draw_shapes(all_shapes)
    draw_lines(all_lines)
    draw_log(log_data)
    
    mouse_pos = pygame.mouse.get_pos() # get mouse position every frame
    
    # if the mouse position collides with the "spin" button, change its color
    if reroll_button.collidepoint(mouse_pos):
        reroll_button_color = (125, 161, 125)
    else:
        reroll_button_color = (155, 191, 155)
    # if the mouse position collides with the "x" button, change its color
    if x_button.collidepoint(mouse_pos):
        x_button_color = (125, 161, 125)
    else:
        x_button_color = (155, 191, 155)
    
    # iterate through user input every frame
    for event in pygame.event.get():
        # if the user closes the game window, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicks the "spin" button, regenerate random shapes
            if event.button == 1 and reroll_button.collidepoint(mouse_pos):
                all_shapes = generate_shapes()
                all_lines = generate_lines(all_shapes)
                component_shapes = graph.get_component_shapes(all_lines)
                log_data = generate_log(component_shapes)
            # if the user clicks the "x" button, quit the game
            if event.button == 1 and x_button.collidepoint(mouse_pos):
                pygame.quit()
                exit()
    
    # update the display every frame
    pygame.display.update()
    clock.tick(60)




