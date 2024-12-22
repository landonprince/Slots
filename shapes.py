import random

colors = ("red", "green", "blue", "yellow", "purple")
shapes = ("square", "triangle", "circle", "diamond", "star")

points = [(55, 73), (178, 73), (305, 73), (434, 73),
          (55, 193), (178, 193), (305, 193), (434, 193),
          (55, 313), (178, 310), (305, 313), (434, 313),
          (55, 433), (178, 433), (305, 433), (434, 433)]

class Shape:
    def __init__(self, color):
        self.color = color
    
    def draw(self):
        raise NotImplementedError("Subclasses must implement draw method")
    
class Square(Shape):
    def __init__(self, color):
        super().__init__(color)

    def generate(self):
        random_index = random.randint(0, len(points) - 1)  # Dynamically determine range
        point = points.pop(random_index)  # Safely remove the point
        return (point[0], point[1], 95, 95)
        
        
    
        

# SQUARE
# pygame.draw.rect(screen, "GREEN", (177, 60, 95, 95))  # Filled
# pygame.draw.rect(screen, "black", (177, 60, 95, 95), 5)  # Outline

# CIRCLE
# pygame.draw.circle(screen, "GREEN", (100, 105), 48)  
# pygame.draw.circle(screen, "black", (100, 105), 48, 5) 

# TRIANGLE
# base_x, base_y = 351, 106 
# triangle_points = [
#     (base_x, base_y - 45),  # Top
#     (base_x + 50, base_y + 45),  # Bottom-right
#     (base_x - 50, base_y + 45)   # Bottom-left
# ]
# pygame.draw.polygon(screen, "GREEN", triangle_points)  # Filled
# pygame.draw.polygon(screen, "BLACK", triangle_points, 5)  # Outline

# DIAMOND
# base_x, base_y = 480, 230  
# diamond_points = [
#     (base_x, base_y - 50),  # Top
#     (base_x + 50, base_y),  # Right
#     (base_x, base_y + 50),  # Bottom
#     (base_x - 50, base_y)   # Left
# ]
# pygame.draw.polygon(screen, "GREEN", diamond_points)  # Filled
# pygame.draw.polygon(screen, "BLACK", diamond_points, 7)  # Outline

# STAR
# base_x, base_y = 480, 105  
# star_points = [
#     (base_x, base_y - 50),    # Top point
#     (base_x + 15, base_y - 15),  # Top-right inner
#     (base_x + 50, base_y - 15),  # Right outer
#     (base_x + 25, base_y + 10),  # Bottom-right inner
#     (base_x + 40, base_y + 50),  # Bottom-right outer
#     (base_x, base_y + 25),       # Bottom center
#     (base_x - 40, base_y + 50),  # Bottom-left outer
#     (base_x - 25, base_y + 10),  # Bottom-left inner
#     (base_x - 50, base_y - 15),  # Left outer
#     (base_x - 15, base_y - 15)   # Top-left inner
# ]
# pygame.draw.polygon(screen, "GREEN", star_points)  # Filled
# pygame.draw.polygon(screen, "BLACK", star_points, 5)  # Outline