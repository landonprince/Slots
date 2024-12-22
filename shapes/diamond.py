base_x, base_y = 480, 230  
diamond_points = [
    (base_x, base_y - 50),  # Top
    (base_x + 50, base_y),  # Right
    (base_x, base_y + 50),  # Bottom
    (base_x - 50, base_y)   # Left
]
pygame.draw.polygon(screen, "GREEN", diamond_points)  # Filled
pygame.draw.polygon(screen, "BLACK", diamond_points, 7)  # Outline