base_x, base_y = 480, 105  
star_points = [
    (base_x, base_y - 50),    # Top point
    (base_x + 15, base_y - 15),  # Top-right inner
    (base_x + 50, base_y - 15),  # Right outer
    (base_x + 25, base_y + 10),  # Bottom-right inner
    (base_x + 40, base_y + 50),  # Bottom-right outer
    (base_x, base_y + 25),       # Bottom center
    (base_x - 40, base_y + 50),  # Bottom-left outer
    (base_x - 25, base_y + 10),  # Bottom-left inner
    (base_x - 50, base_y - 15),  # Left outer
    (base_x - 15, base_y - 15)   # Top-left inner
]

# Draw the star
pygame.draw.polygon(screen, "GREEN", star_points)  # Filled
pygame.draw.polygon(screen, "BLACK", star_points, 5)  # Outline