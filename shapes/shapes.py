colors = ("red", "green", "blue", "yellow", "purple")
shapes = ("square", "triangle", "circle", "diamond", "star")

class Shape:
    def __init__(self, color):
        self.color = color
    
    def draw(self):
        raise NotImplementedError("Subclasses must implement draw method")
    
class Square(Shape):
    def __init__(self, color):
        super().__init__(color)

    def draw(self): # potentially add position as additional argument
        pygame.draw.rect(screen, "GREEN", (177, 60, 95, 95))  # Filled
        pygame.draw.rect(screen, "black", (177, 60, 95, 95), 5)  # Outline
        
class Circle(Shape):
    def __init__(self, color):
        super().__init__(color)
        
    def draw(self):
        pygame.draw.circle(screen, "GREEN", (100, 105), 48)  
        pygame.draw.circle(screen, "black", (100, 105), 48, 5) 


        