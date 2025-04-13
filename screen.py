import ui_manager as ui
import pygame

# screens.py
class Screen:
    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

class WelcomeScreen(Screen):
    def __init__(self):
        self.chimp_img = ui.load_image("chimp.jpg", (400, 200))

    def draw(self, surface):
        surface.fill(ui.background_color)
        center_x = ui.SCREEN_WIDTH // 2
        img_rect = self.chimp_img.get_rect(center=(center_x, 120))
        surface.blit(self.chimp_img, img_rect)
        ui.draw_text("Are you smarter than a chimpanzee?", ui.title_font, ui.BLACK, surface, center_x, 240, True)
        # Other UI drawing...
        self.button_rect = pygame.draw.rect(surface, ui.button_color, (center_x - 150, 450, 300, 60), border_radius=10)
        ui.draw_text("START GAME", ui.button_font, ui.WHITE, surface, center_x, 480, True)