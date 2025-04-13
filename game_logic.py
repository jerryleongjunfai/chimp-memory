import pygame
import ui_manager as ui
from grid import Grid

class GameState:
    """Enum-like class to represent different states of the game."""
    SHOW_TILES = "SHOW_TILES"
    HIDE_TILES = "HIDE_TILES"
    LEVEL_COMPLETE = "LEVEL_COMPLETE"
    GAME_OVER = "GAME_OVER"

class Game:
    """Main game class that handles the game logic for the memory tile game."""
    def __init__(self):
        """Initialize the game with default values."""
        self._level = 1
        self._lives = 3
        self._game_state = GameState.SHOW_TILES
        self._is_game_over = False
        self._correct_order = []
        self._user_selections = []
        self._correct_selections = []
        self._wrong_selection = None
        self._expected_next = 1
        self._level_failed = False
        self._game_timer = 60  # seconds
        self._show_timer = 0
        self._start_time = 0
        self.grid = None

    # Initialize sounds
    # Usage of dictionary
        self._sounds = {
            'correct': None,
            'wrong': None,
            'level_complete': None,
            'game_over': None
        }

    # Method to load sounds
    def load_sounds(self, sounds_dict):
        """Load sound effects from provided dictionary."""
        self._sounds = sounds_dict

    # Encapsulated Getters
    def get_level(self):
        """Get the current level number."""
        return self._level

    def get_lives(self):
        """Get the remaining lives."""
        return self._lives

    def lose_life(self):
        """Reduce player's lives by one."""
        self._lives -= 1

    def start_new_level(self):
        """Initialize a new level with appropriate settings."""
        if 0 <= self._level <= 15:
            # Create a grid with number of tiles based on current level
            self.grid = Grid(self._level + 1)
            
            # Sort tiles by their number for tracking correct order
            self._correct_order = sorted(self.grid.tiles, key=lambda x: x[2])
            
            # Reset game state variables
            self._user_selections = []
            self._correct_selections = []
            self._wrong_selection = None
            self._expected_next = 1
            self._game_state = GameState.SHOW_TILES
            
            # Set timers
            self._show_timer = pygame.time.get_ticks()
            self._start_time = pygame.time.get_ticks()
            
            # Display tiles
            self.grid.showTiles()
            self._level_failed = False

    def update_game(self):
        """Update game state based on time elapsed."""
        current_time = pygame.time.get_ticks()

        # After showing tiles for 3 seconds, hide them
        if self._game_state == GameState.SHOW_TILES and current_time - self._show_timer > 3000:
            self._game_state = GameState.HIDE_TILES
            self.grid.hideTiles()

        # Update time remaining
        elapsed_seconds = (current_time - self._start_time) // 1000
        remaining_time = max(0, self._game_timer - elapsed_seconds)

        # Check if time is up
        if remaining_time <= 0 and self._game_state != GameState.GAME_OVER:
            self._lives = 0
            self._game_state = GameState.GAME_OVER
            if self._sounds['game_over']:
                self._sounds['game_over'].play()

    def handle_click(self, pos):
        """Handle mouse click at the given position."""
        # Calculate grid dimensions
        cols, rows = 8, 5
        cell_width = ui.SCREEN_WIDTH // cols
        cell_height = (ui.SCREEN_HEIGHT - 100) // rows

        # Convert screen position to grid coordinates
        col = pos[0] // cell_width + 1
        row = (pos[1] - 50) // cell_height + 1
        clicked_correctly = False

        # Check if the click hit a tile
        for tile in self.grid.tiles:
            x, y, num = tile
            if x == col and y == row:
                if num == self._expected_next:
                    # Correct tile selected
                    self._expected_next += 1
                    self._user_selections.append(tile)
                    self._correct_selections.append(tile)
                    clicked_correctly = True

                    # Play correct sound
                    if self._sounds['correct']:
                        self._sounds['correct'].play()

                    # Check if level is complete
                    if len(self._user_selections) == len(self.grid.tiles):
                        self._level += 1
                        self._game_state = GameState.LEVEL_COMPLETE
                        # Play level complete sound
                        if self._sounds['level_complete']:
                            self._sounds['level_complete'].play()
                else:
                    # Wrong tile selected
                    self._lives -= 1
                    self._wrong_selection = (col, row)

                    # Play wrong sound
                    if self._sounds['wrong']:
                        self._sounds['wrong'].play()

                    if self._lives <= 0:
                        self._game_state = GameState.GAME_OVER
                        # Play game over sound
                        if self._sounds['game_over']:
                            self._sounds['game_over'].play()
                    else:
                        self._level_failed = True
                        self._game_state = GameState.LEVEL_COMPLETE
                break

        # If the click was not on a correct tile and no wrong selection has been made
        if not clicked_correctly and self._wrong_selection is None:
            self._wrong_selection = (col, row)
        
    def draw_game_state(self, screen):
        """Draw the entire game state to the screen."""
        # Draw the game header
        self._draw_header(screen)

        # Draw the grid and tiles
        self._draw_grid(screen)

        # Draw state-specific overlays
        if self._game_state == GameState.LEVEL_COMPLETE:
            if self._level_failed:
                self._draw_center_text(screen, "Wrong tile! You lose a life", extra="Click to continue")
            else:
                self._draw_center_text(screen, "Level Complete! Click to continue")
        elif self._game_state == GameState.GAME_OVER:
            # Define average chimpanzee level
            avg_chimp_level = 9
            # Determine comparison message
            if self._level > avg_chimp_level:
                comparison = f"You performed BETTER than an average chimpanzee! (Avg: {avg_chimp_level})"
            elif self._level < avg_chimp_level:
                comparison = f"You performed WORSE than an average chimpanzee! (Avg: {avg_chimp_level})"
            else:
                comparison = f"You performed EQUAL to an average chimpanzee! (Avg: {avg_chimp_level})"

            self._draw_center_text(screen, "Game Over!", extra=f"Highest level reached: {self._level}",extra2=comparison, bottom="Click to restart")

    def _draw_header(self, screen):
        """Draw the game header with level, timer, and lives."""
        pygame.draw.rect(screen, ui.background_color, (0, 0, ui.SCREEN_WIDTH, 50))
        ui.draw_text(f"Level: {self._level}", ui.regular_font, ui.BLACK, screen, 50, 25, True)

        # Only show timer if game is not over
        if self._game_state != GameState.GAME_OVER:
            elapsed = (pygame.time.get_ticks() - self._start_time) // 1000
            remaining = max(0, self._game_timer - elapsed)
            timer_text = f"{remaining // 60}:{remaining % 60:02d}"
            ui.draw_text(timer_text, ui.regular_font, ui.BLACK, screen, ui.SCREEN_WIDTH // 2, 25, True)

        ui.draw_text(f"Lives: {self._lives}", ui.regular_font, ui.BLACK, screen, ui.SCREEN_WIDTH - 50, 25, True)

    def _draw_grid(self, screen):
        """Draw the game grid with tiles."""
        cols, rows = 8, 5
        cell_width = ui.SCREEN_WIDTH // cols
        cell_height = (ui.SCREEN_HEIGHT - 100) // rows

        # Draw background
        pygame.draw.rect(screen, ui.WHITE, (0, 50, ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT - 50))

        # Draw all tiles
        for tile in self.grid.tiles:
            x, y, num = tile
            x_pos = (x - 1) * cell_width
            y_pos = (y - 1) * cell_height + 50
            pygame.draw.rect(screen, (173, 216, 230), (x_pos, y_pos, cell_width, cell_height))

        # Draw correct selections
        for tile in self._correct_selections:
            x, y, _ = tile
            x_pos = (x - 1) * cell_width
            y_pos = (y - 1) * cell_height + 50
            pygame.draw.rect(screen, (100, 200, 100), (x_pos, y_pos, cell_width, cell_height))

        # Draw wrong selection if any
        if self._wrong_selection:
            x, y = self._wrong_selection
            x_pos = (x - 1) * cell_width
            y_pos = (y - 1) * cell_height + 50
            pygame.draw.rect(screen, (255, 100, 100), (x_pos, y_pos, cell_width, cell_height))

        # Show numbers when in SHOW_TILES state
        if self._game_state == GameState.SHOW_TILES:
            for tile in self.grid.tiles:
                x, y, num = tile
                x_center = (x - 1) * cell_width + cell_width // 2
                y_center = (y - 1) * cell_height + cell_height // 2 + 50
                text = ui.title_font.render(str(num), True, ui.BLACK)
                screen.blit(text, text.get_rect(center=(x_center, y_center)))

        # Hide numbers in HIDE_TILES state, but keep highlighting
        if self._game_state == GameState.HIDE_TILES:
            for tile in self.grid.tiles:
                x, y, _ = tile
                x_pos = (x - 1) * cell_width
                y_pos = (y - 1) * cell_height + 50
                pygame.draw.rect(screen, (173, 216, 230), (x_pos, y_pos, cell_width, cell_height))

            for tile in self._user_selections:
                x, y, _ = tile
                x_pos = (x - 1) * cell_width
                y_pos = (y - 1) * cell_height + 50
                pygame.draw.rect(screen, (100, 200, 100), (x_pos, y_pos, cell_width, cell_height))

    def _draw_center_text(self, screen, message, extra=None, bottom=None, extra2=None):
        """Draw centered text messages on the screen."""
        center_x = ui.SCREEN_WIDTH // 2
        center_y = ui.SCREEN_HEIGHT // 2
        
        # Draw main message
        ui.draw_text(message, ui.title_font, ui.BLACK, screen, center_x, center_y, True)
        
        # Draw extra message if provided
        if extra:
            ui.draw_text(extra, ui.regular_font, ui.BLACK, screen, center_x, center_y + 50, True)

        # Draw second extra message if provided
        if extra2:
            ui.draw_text(extra2, ui.regular_font, ui.BLACK, screen, center_x, center_y + 100, True)
        
        # Draw bottom message if provided
        if bottom:
            ui.draw_text(bottom, ui.regular_font, ui.BLACK, screen, center_x, center_y + 150, True)