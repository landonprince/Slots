base_x, base_y = 480, 105  
star_points = [
    (base_x, base_y - 50),    
    (base_x + 15, base_y - 15),  
    (base_x + 50, base_y - 15),  
    (base_x + 25, base_y + 10), 
    (base_x + 40, base_y + 50), 
    (base_x, base_y + 25),       
    (base_x - 40, base_y + 50), 
    (base_x - 25, base_y + 10),  
    (base_x - 50, base_y - 15), 
    (base_x - 15, base_y - 15)   
]
pygame.draw.polygon(screen, "GREEN", star_points) 
pygame.draw.polygon(screen, "BLACK", star_points, 5)  