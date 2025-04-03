import pygame
import uimanager as ui
#import main as m
import grid as g
import player as p

class Game(pygame):

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Chimpanzee Memory Game")
        self.screen = pygame.display.set_mode((ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))
        self.level = 4
        self.lives = 3
        self.isGameOver = False
        self.welcome_screen()

    def welcome_screen(self):
        # Logic for the welcome screen
        pass

    def startLevel(self):
        while self.lives > 0 and self.level <= 15:
            grid = g.Grid(self.level)
            grid.generateTiles(self.level)
            grid.showTiles()
            grid.hideTiles()
            playerChoice = p.Player().tileSelection(grid.tiles)
            if playerChoice == grid.tiles:
                print("Correct! Proceeding to the next level.")
                self.level += 1
            else:
                print("Incorrect! You lost a life.")
                self.lives -= 1
            if self.lives == 0:
                self.isGameOver = True
                print("Game Over! You have no lives left.")
                break

    def gameOver(self):
        print("Game Over! You have no lives left.")
        print("Highest level reached:", self.level)
        restart = input("Do you want to restart the game? (yes/no): ")
        if restart.lower() == "yes":
            self.level = 1
            self.lives = 3
            self.isGameOver = False
            self.startLevel()
        else:
            print("Thank you for playing!")
            pygame.quit()
            exit()