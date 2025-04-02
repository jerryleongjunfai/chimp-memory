import grid as grid

class Player:
    def tileSelection(self, tile):
        userSelection = []
        for i in range (1, len(grid.correctOrder)):
            print("Select tile number", i)