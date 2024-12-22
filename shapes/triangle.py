base_x, base_y = 351, 106 
triangle_points = [
    (base_x, base_y - 45), 
    (base_x + 50, base_y + 45),  
    (base_x - 50, base_y + 45)  
]
pygame.draw.polygon(screen, "GREEN", triangle_points)  # Filled
pygame.draw.polygon(screen, "BLACK", triangle_points, 5)  # Outline