import pygame
import uimanager as ui
import grid as g
import player as p
import time

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Chimpanzee Memory Game")
        self.screen = pygame.display.set_mode((ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))
        self._level = 1
        self._lives = 3
        self._gameState = "SHOW_TILES"
        self.isGameOver = False
        self.correctOrder = []
        self.userSelection = []
        self.show_timer = 0
        self.expected_next = 1
        self.level_failed = False
        self.correct_selections = []
        self.wrong_selection = None
        self.game_timer = 60
        self.start_time = 0
    
    def get_level(self):
        return self._level

    def lose_life(self):
        self._lives -= 1

    def start_new_level(self):
        self.grid = g.Grid(self._level + 1)
        self.correctOrder = sorted(self.grid.tiles, key=lambda x: x[2])
        self.user_selections = []
        self.correct_selections = []
        self.wrong_selection = None
        self.expected_next = 1
        self.game_state = "SHOW_TILES"
        self.show_timer = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.grid.showTiles()
        self.level_failed = False

    def update_game(self):
        current_time = pygame.time.get_ticks()
        
        # Handle tile reveal timing
        if self.game_state == "SHOW_TILES" and current_time - self.show_timer > 3000:  # 3 seconds
            self.game_state = "HIDE_TILES"
            self.grid.hideTiles()
        
        # Check if time is up
        elapsed_seconds = (current_time - self.start_time) // 1000
        remaining_time = max(0, self.game_timer - elapsed_seconds)
        
        if remaining_time <= 0 and self.game_state != "GAME_OVER":
            self.lives = 0
            self.game_state = "GAME_OVER"
    
    def handle_click(self, pos):
        if self.game_state != "HIDE_TILES":
            return
            
        cols, rows = 8, 5
        cell_width = ui.SCREEN_WIDTH // cols
        cell_height = (ui.SCREEN_HEIGHT - 100) // rows
        
        # Convert mouse position to grid coordinates
        col = pos[0] // cell_width + 1
        row = (pos[1] - 50) // cell_height + 1

        clicked_correctly = False
        
        # Check if clicked on a valid tile
        for tile in self.grid.tiles:
            x, y, num = tile
            if x == col and y == row:
                # Check if this is the expected next number
                if num == self.expected_next:
                    print(f"Correct! Selected {num}")
                    self.expected_next += 1
                    self.user_selections.append(tile)
                    self.correct_selections.append(tile)
                    clicked_correctly = True
                    
                    # Check if all tiles have been selected in correct order
                    if len(self.user_selections) == len(self.grid.tiles):
                        print("Level complete!")
                        self.level += 1
                        self.game_state = "LEVEL_COMPLETE"
                else:
                    print(f"Wrong! Selected {num}, expected {self.expected_next}")
                    self.lives -= 1
                    self.wrong_selection = (col, row)
                    if self.lives <= 0:
                        self.game_state = "GAME_OVER"
                    else:
                        self.level_failed = True
                        # Reset current level
                        self.game_state = "LEVEL_COMPLETE"
                break
        
        # If clicked outside valid tiles
        if not clicked_correctly:
            if self.wrong_selection is None and self.game_state == "HIDE_TILES":
                self.wrong_selection = (col, row)
        
    def draw_game_state(self, screen):
        # Draw the header with level and lives info
        pygame.draw.rect(screen, ui.background_color, (0, 0, ui.SCREEN_WIDTH, 50))
        ui.draw_text(f"Level: {self._level}", ui.regular_font, ui.BLACK, screen, 50, 25, True)

        if self.game_state != "GAME_OVER":
            elapsed_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining_time = max(0, self.game_timer - elapsed_seconds)
            timer_text = f"{remaining_time // 60}:{remaining_time % 60:02d}"
            ui.draw_text(timer_text, ui.regular_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, 25, True)

        ui.draw_text(f"Lives: {self._lives}", ui.regular_font, ui.BLACK, screen, ui.SCREEN_WIDTH - 50, 25, True)
        
        # Draw grid
        cols, rows = 8, 5
        cell_width = ui.SCREEN_WIDTH // cols
        cell_height = (ui.SCREEN_HEIGHT - 100) // rows

        # Fill the entire grid area with white
        pygame.draw.rect(screen, ui.WHITE, (0, 50, ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT - 50))
   
        for tile in self.grid.tiles:
            xCoord, yCoord, num = tile
            x = (xCoord - 1) * cell_width
            y = (yCoord - 1) * cell_height + 50
            pygame.draw.rect(screen, (173, 216, 230), (x, y, cell_width, cell_height))

        # Draw correct selections in green
        for tile in self.correct_selections:
            xCoord, yCoord, _ = tile
            x = (xCoord - 1) * cell_width
            y = (yCoord - 1) * cell_height + 50
            pygame.draw.rect(screen, (100, 200, 100), (x, y, cell_width, cell_height))

        # Draw wrong selection in red
        if self.wrong_selection:
            xCoord, yCoord = self.wrong_selection
            x = (xCoord - 1) * cell_width
            y = (yCoord - 1) * cell_height + 50
            pygame.draw.rect(screen, (255, 100, 100), (x, y, cell_width, cell_height))


        # Draw numbers on tiles if in show state
        if self.game_state == "SHOW_TILES":
            for tile in self.grid.tiles:
                xCoord, yCoord, num = tile
                # Calculate the position for the number on the tile
                x = (xCoord - 1) * cell_width + cell_width // 2
                y = (yCoord - 1) * cell_height + cell_height // 2 + 50
                # Render the number in the center of the tile
                text = ui.title_font.render(str(num), True, ui.BLACK)
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)
        
        # Draw selected tiles (crossed out or highlighted)
        if self.game_state == "HIDE_TILES":
            # Show a light blue tile for original positions after hiding
            for tile in self.grid.tiles:
                xCoord, yCoord, _ = tile
                x = (xCoord - 1) * cell_width
                y = (yCoord - 1) * cell_height + 50
                pygame.draw.rect(screen, (173, 216, 230), (x, y, cell_width, cell_height))

            for tile in self.user_selections:
                xCoord, yCoord, num = tile
                x = (xCoord - 1) * cell_width
                y = (yCoord - 1) * cell_height + 50
                pygame.draw.rect(screen, (100, 200, 100), (x, y, cell_width, cell_height))
        
        # Show messages for game states
        if self.game_state == "LEVEL_COMPLETE":
            if self.level_failed:
                ui.draw_text("Wrong tile! You lose a life", ui.title_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, ui.SCREEN_HEIGHT // 2, True)
                ui.draw_text("Click to continue", ui.regular_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, ui.SCREEN_HEIGHT // 2 + 50, True)
            else:
                ui.draw_text("Level Complete! Click to continue", ui.title_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, ui.SCREEN_HEIGHT // 2, True)
        
        if self.game_state == "GAME_OVER":
            ui.draw_text("Game Over!", ui.title_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, ui.SCREEN_HEIGHT // 2, True)
            ui.draw_text(f"Highest level reached: {self._level}", ui.regular_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, ui.SCREEN_HEIGHT // 2 + 50, True)
            ui.draw_text("Click to restart", ui.regular_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, ui.SCREEN_HEIGHT // 2 + 150, True)