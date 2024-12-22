base_x, base_y = 480, 230  
diamond_points = [
    (base_x, base_y - 50),  
    (base_x + 50, base_y), 
    (base_x, base_y + 50), 
    (base_x - 50, base_y)   
]
pygame.draw.polygon(screen, "GREEN", diamond_points)  # Filled
pygame.draw.polygon(screen, "BLACK", diamond_points, 7)  # Outline