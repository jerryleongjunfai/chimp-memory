import pygame
import random
import time

class Grid:
    def __init__(self, level):
        self.numberOfTiles = level
        self.tiles = []
        self.generateTiles(level)

    def generateTiles (self, level):
        for num in range(1, level + 1):
            while True:
                xCoord = random.randint(1, 8)
                yCoord = random.randint(1, 5)

                #Check if the tile is already placed at the coordinates
                if not any(tile[0] == xCoord and tile[1] == yCoord for tile in self.tiles):
                    self.tiles.append((xCoord, yCoord, num))
                    break
                else:
                    print(f"Tile at position ({xCoord}, {yCoord}) already exists. Generating a new position.")
        print("Tiles generated successfully.")
        print("Tiles:", self.tiles)
        return self.tiles
            
    def showTiles(self):
        print("Showing the tiles for 3 seconds...")
        for tile in self.tiles:
            print(f"Tile at position ({tile[0]}, {tile[1]}) has number: {tile[2]}")
        time.sleep(3)

    def hideTiles(self):
        print("Tiles are now hidden")

my_grid = Grid(5)
my_grid.showTiles()