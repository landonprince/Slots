import pygame
import random

# a random color & shape is chosen from these tuples when creating a shape
bronze = (185, 117, 60)
silver = (180, 180, 180)
gold = (212, 168, 55)
diamond = (80, 160, 85)

colors = (bronze, silver, gold, diamond)
weights = [50, 30, 15, 5]
shapes = ("square", "triangle", "circle", "diamond")

# each point represents a position to place a shape (top-left)
points = [
    (55, 73),  (178, 73),  (305, 73),  (434, 73),
    (55, 193), (178, 193), (305, 193), (434, 193),
    (55, 313), (178, 313), (305, 313), (434, 313),
    (55, 433), (178, 433), (305, 433), (434, 433)
]

# return a random shape type & color
def get_random_shape():
    shape_type = random.choice(shapes)
    color = random.choices(colors, weights=weights, k=1)[0]
    return shape_type, color

# superclass to square, circle, triangle, & diamond subclasses
class Shape:
    # set the color & position of the shape
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    # abstract method to be implemented by subclasses
    def draw_shape(self):
        raise NotImplementedError("Subclasses must implement draw_shape method")

    # abstract method to be implemented by subclasses
    def print_shape(self):
        raise NotImplementedError("Subclasses must implement print_shape method")

# subclass for square shape 
class Square(Shape):
    # set the color, position, size, & type of the square
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 95
        self.type = "square"
    
    # draw the square at its designated position
    def draw_shape(self, screen):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, "black", rect, 5)
        
    # print the attributes of the square 
    def print_shape(self):
        print(f"\n{self.type}, {self.color}, X: {self.x}, Y: {self.y}\n")

# subclass for the circle shape
class Circle(Shape):
    # set the color, position, size, & type of the circle
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 48
        self.type = "circle"
    
    # draw the circle at its designated position
    def draw_shape(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (self.x + self.size, self.y + self.size), self.size)
        pygame.draw.circle(screen, "black", 
                           (self.x + self.size, self.y + self.size), self.size, 5)
    
    # print the attributes of the circle 
    def print_shape(self):
        print(f"\n{self.type}, {self.color}, X: {self.x}, Y: {self.y}\n")

# subclass for the triangle shape
class Triangle(Shape):
    # set the color, position, size, & type of the triangle
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 95
        self.type = "triangle"

    # draw the triangle at its designated position 
    def draw_shape(self, screen):
        center_x = self.x + self.size // 2   
        center_y = self.y + self.size // 2  
        
        triangle_points = [
            (center_x, center_y - 45),
            (center_x + 45, center_y + 45),
            (center_x - 45, center_y + 45)  
        ]
        
        pygame.draw.polygon(screen, self.color, triangle_points)
        pygame.draw.polygon(screen, "black", triangle_points, 5)
    
    # print the attributes of the triangle
    def print_shape(self):
        print(f"\n{self.type}, {self.color}, X: {self.x}, Y: {self.y}\n")

# subclass for the diamond shape
class Diamond(Shape):
    # set the color, position, size, & type of the diamond
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 95
        self.type = "diamond"

    # draw the diamond at its designated position
    def draw_shape(self, screen):
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        diamond_points = [
            (center_x, center_y - 50),  
            (center_x + 50, center_y),         
            (center_x, center_y + 50), 
            (center_x - 50, center_y)          
        ]

        pygame.draw.polygon(screen, self.color, diamond_points)
        pygame.draw.polygon(screen, "black", diamond_points, 7)
        
    # print the attributes of the diamond
    def print_shape(self):
        print(f"\n{self.type}, {self.color}, X: {self.x}, Y: {self.y}\n")  