import pygame

pygame.font.init()

# Constants for screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background_color = (135, 206, 250)  # Light blue
button_color = (70, 130, 180)       # Steel blue
button_hover_color = (30, 100, 150) # Darker blue for hover effect

#Fonts
title_font = pygame.font.Font(None, 48)
regular_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 40)

def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def load_image(name, scale=None):
    try:
        image = pygame.image.load(name)
        if scale:
            return pygame.transform.scale(image, scale)
        return image
    except pygame.error:
        print(f"Unable to load image: {name}")
        # Create a placeholder image with text
        img = pygame.Surface((300, 200))
        img.fill((200, 200, 200))
        text = regular_font.render("Chimp Image", True, BLACK)
        img.blit(text, (100, 90))
        return img