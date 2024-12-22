base_x, base_y = 351, 106 
triangle_points = [
    (base_x, base_y - 45),  # Top
    (base_x + 50, base_y + 45),  # Bottom-right
    (base_x - 50, base_y + 45)   # Bottom-left
]
# Draw the triangle
pygame.draw.polygon(screen, "GREEN", triangle_points)  # Filled
pygame.draw.polygon(screen, "BLACK", triangle_points, 5)  # Outline