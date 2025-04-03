import pygame
import uimanager as ui

pygame.init()
pygame.font.init()
pygame.display.set_caption("Chimpanzee Memory Game")
screen = pygame.display.set_mode((ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))

def welcome_screen():
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

        button_width, button_height = 300, 60
        button_x = center_x - button_width // 2
        button_y = 450

        mouse = pygame.mouse.get_pos()
        if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
            pygame.draw.rect(screen, ui.button_hover_color, (button_x, button_y, button_width, button_height), border_radius=10)
        else:
            pygame.draw.rect(screen, ui.button_color, (button_x, button_y, button_width, button_height), border_radius=10)
            
        ui.draw_text("START GAME", ui.button_font, ui.WHITE, screen, center_x, button_y + button_height//2, True)
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
        screen.fill(ui.BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

print("trying it again")
welcome_screen()
main_game()