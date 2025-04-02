import pygame
import random
import os
pygame.init()

# Constants for screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[0] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width/2)), (y + (height/2)))
    screen.blit(text_surf, text_rect)

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

def welcome_screen():
    running = True
    chimp_img = load_image("chimp.jpg", (400, 200)) 
    while running:
        screen.fill(background_color)

        # Calculate center positions
        center_x = SCREEN_WIDTH // 2

        # Display chimp image at the top
        img_rect = chimp_img.get_rect(center=(center_x, 120))
        screen.blit(chimp_img, img_rect)

        # Draw title and instructions with better padding and centering
        draw_text("Are you smarter than a chimpanzee?", title_font, BLACK, screen, center_x, 240, True)
        draw_text("Memorize the number tiles and select them in order.", regular_font, BLACK, screen, center_x, 300, True)
        draw_text("You have 3 lives", regular_font, BLACK, screen, center_x, 350, True)

        # Create a button instead of text instruction
        button_width, button_height = 300, 60
        button_x = center_x - button_width // 2
        button_y = 450
        
        # Draw button with hover effect
        mouse = pygame.mouse.get_pos()
        if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
            pygame.draw.rect(screen, button_hover_color, (button_x, button_y, button_width, button_height), border_radius=10)
        else:
            pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), border_radius=10)
            
        draw_text("START GAME", button_font, WHITE, screen, center_x, button_y + button_height//2, True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # If ENTER key is pressed, start the game
                    running = False
            # Add mouse click for button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
                    running = False

def main_game():
    run = True 
    while run:
        screen.fill(WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chimpanzee Memory Game")

welcome_screen()
main_game()
# This is a simple Pygame window setup.