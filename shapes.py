import pygame
import random

colors = ("red", "green", "blue", "yellow")
shapes = ("square", "triangle", "circle", "diamond")

points = [
    (55, 73), (178, 73), (305, 73), (434, 73),
    (55, 193), (178, 193), (305, 193), (434, 193),
    (55, 313), (178, 313), (305, 313), (434, 313),
    (55, 433), (178, 433), (305, 433), (434, 433)
]

class Shape:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
    
    def draw(self):
        raise NotImplementedError("Subclasses must implement draw method")
    
class Square(Shape):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 95
    
    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, "black", rect, 5)
        
class Circle(Shape):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 48
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (self.x + self.size, self.y + self.size), self.size)
        pygame.draw.circle(screen, "black", 
                           (self.x + self.size, self.y + self.size), self.size, 5)
        
class Triangle(Shape):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 95

    def draw(self, screen):
        center_x = self.x + self.size // 2   
        center_y = self.y + self.size // 2  
        
        triangle_points = [
            (center_x, center_y - 45),
            (center_x + 45, center_y + 45),
            (center_x - 45, center_y + 45)  
        ]
        
        pygame.draw.polygon(screen, self.color, triangle_points)
        pygame.draw.polygon(screen, "black", triangle_points, 5)
        
class Diamond(Shape):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.size = 95

    def draw(self, screen):
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        diamond_points = [
            (center_x, center_y - 45),  
            (center_x + 45, center_y),         
            (center_x, center_y + 45), 
            (center_x - 45, center_y)          
        ]

        pygame.draw.polygon(screen, self.color, diamond_points)
        pygame.draw.polygon(screen, "black", diamond_points, 7)
        
def get_random_shape():
    shape_type = random.choice(shapes)
    color = random.choice(colors)
    return shape_type, color