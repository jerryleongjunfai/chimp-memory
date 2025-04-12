import pygame
import ui_manager as ui
from grid import Grid
import game_logic as game
from screen import WelcomeScreen
from game_logic import GameState
import os

pygame.init()
pygame.font.init()
pygame.mixer.init() # Initialize the mixer for sound
pygame.display.set_caption("Chimpanzee Memory Game")
screen = pygame.display.set_mode((ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))
clock = pygame.time.Clock()

def load_sound(filename):
    """Helper function to load sound files."""
    sound_path = os.path.join('sound', filename)  # Assuming sounds are in a 'sounds' folder
    try:
        sound = pygame.mixer.Sound(sound_path)
        return sound
    except pygame.error:
        print(f"Could not load sound file: {sound_path}")
        return None

def run_screen(screen_obj):
    running = True
    chimp_img = ui.load_image("chimp.jpg", (400, 200))
    
    while running:
        screen.fill(ui.background_color)
        # Calculate center positions
        center_x = ui.SCREEN_WIDTH // 2
        
        # Display chimp image at the top
        img_rect = chimp_img.get_rect(center=(center_x, 120))
        screen.blit(chimp_img, img_rect)
        
        # Draw title and instructions with better padding and centering
        ui.draw_text("Are you smarter than a chimpanzee?", ui.title_font, ui.BLACK, screen, center_x, 240, True)
        ui.draw_text("Memorize the number tiles and select them in order.", ui.regular_font, ui.BLACK, screen, center_x, 300, True)
        ui.draw_text("You have 3 lives", ui.regular_font, ui.BLACK, screen, center_x, 350, True)
        
        # Draw start button
        button_width, button_height = 300, 60
        button_x = center_x - button_width // 2
        button_y = 450
        mouse = pygame.mouse.get_pos()
        
        # Highlight button on hover
        if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
            pygame.draw.rect(screen, ui.button_hover_color, (button_x, button_y, button_width, button_height), border_radius=10)
        else:
            pygame.draw.rect(screen, ui.button_color, (button_x, button_y, button_width, button_height), border_radius=10)
        
        ui.draw_text("START GAME", ui.button_font, ui.WHITE, screen, center_x, button_y + button_height // 2, True)
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
        
        # Polymorphism: screen_obj can be any object with a draw() method
        screen_obj.draw(screen)

# Game loop that handles gameplay state and drawing
def main_game():
    # Load sound effects
    sounds = {
        'correct': load_sound('correct.wav'),
        'wrong': load_sound('wrong.wav'),
        'level_complete': load_sound('level_complete.wav'),
        'game_over': load_sound('game_over.wav')
    }
    
    game_instance = game.Game()
    # Pass sound effects to the game instance
    game_instance.load_sounds(sounds)
    game_instance.start_new_level()
    run = True
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_instance._game_state == GameState.HIDE_TILES:
                    game_instance.handle_click(pygame.mouse.get_pos())
                elif game_instance._game_state == GameState.LEVEL_COMPLETE:
                    game_instance.start_new_level()
                elif game_instance._game_state == GameState.GAME_OVER:
                    # Reset game
                    game_instance = game.Game()
                    game_instance.start_new_level()
        
        screen.fill(ui.WHITE)
        
        # Only update game logic if the state is not paused
        if game_instance._game_state in [GameState.SHOW_TILES, GameState.HIDE_TILES]:
            game_instance.update_game()
        
        game_instance.draw_game_state(screen)
        pygame.display.update()
    
    pygame.quit()
    exit()

# Start the program by showing the welcome screen, then launch the main game
if __name__ == "__main__":
    welcome = WelcomeScreen()  # WelcomeScreen implements draw(screen)
    run_screen(welcome)  # Pass welcome as screen_obj into run_screen() — POLYMORPHISM
    main_game()