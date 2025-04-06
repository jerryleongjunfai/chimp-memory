import random

class Grid:
    def __init__(self, level):
        self.numberOfTiles = level
        self.tiles = []
        self.visible = True
        self.generateTiles(level)

    def generateTiles (self, level):
        self.tiles = []  # Reset tiles for each level
        for num in range(1, level + 1):
            while True:
                xCoord = random.randint(1, 8)
                yCoord = random.randint(1, 5)
                if not any(tile[0] == xCoord and tile[1] == yCoord for tile in self.tiles):
                    self.tiles.append((xCoord, yCoord, num))
                    break
                else:
                    print(f"Tile at position ({xCoord}, {yCoord}) already exists. Generating a new position.")
        print("Tiles generated successfully.")
        print("Tiles:", self.tiles)
        return self.tiles
            
    def showTiles(self):
        self.visible = True
        print("Showing the tiles for 3 seconds...")

    def hideTiles(self):
        self.visible = False
        print("Tiles are now hidden")
