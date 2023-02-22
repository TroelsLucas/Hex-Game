import pygame
import math
#
WHITE = (255,255,255)
BLACK =(0,0,0)
RED = (255,0,0)

FPS = 60

#Surface/Screen size (this shoudl be scaleable)
WIDTH, HEIGHT= 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HEX")

#add width to the hexagon so there can be a "neutral"   
class Hexagon:
    def __init__(self,player,pos,radius,color,surface):
        self.player = player
        self.pos = pos
        self.radius = radius
        self.color = color
        self.fill = None
        self.posArr = None
        # board pos needs to be coded
        self.boardPos = None
        self.surface = surface

    def __str__(self):
        return (f'HEXOBJ=player: {self.player}, pos:{self.pos}, color:{self.color}, posArr{self.posArr}')
    #the underscore infront indicates that these are private attributes they are not necessary
    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player
        
    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_fill(self):
        return self.fill

    def set_fill(self, fill):
        self.fill = fill

    def get_screen(self):
        return self.surface

    def set_screen(self, surface):
        self.surface = surface

    def get_posArr(self):
        return self.posArr

    #is this even necessary
    def set_posArr(self, posArr):
        self.posArr = posArr

    def draw(self):
        posArr = list()
        pygame.draw.polygon(self.surface, self.color, [
        (self.pos[0] + self.radius * math.sin(2 * math.pi * i / 6), self.pos[1] + self.radius * math.cos(2 * math.pi * i / 6))
        for i in range(6)
        ], 0)
        for i in range(6):
            posArr.append((self.pos[0] + self.radius * math.sin(2 * math.pi * i / 6), self.pos[1] + self.radius * math.cos(2 * math.pi * i / 6)))

        self.set_posArr(posArr)

class Board:
    def __init__(self,hexagon,coords, dimensions,surface):
        self.hexagon = hexagon
        self.coords = coords
        self.dimensions = dimensions
        self.surface = surface
        self.grid = None
        self.selected_hexagon = None

    def __str__(self):
        return (f'BOARDOBJ=hexagon:{self.hexagon}, coords:{self.coords}, grid{self.grid}, selected_hexagon:{self.selected_hexagon}')

    def generate_hexagon_grid(self):
        hex_width = self.hexagon.get_radius() * 1.75
        hex_height = (3 ** 0.5) / 2 * hex_width

        hex_grid = []

        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                hex_x = hex_width * j + hex_width / 2 * (i % 2) + self.coords[0]
                hex_y = hex_height * i + self.coords[1]
                hex_position = (hex_x, hex_y)

                hexagon = Hexagon(0, hex_position, self.hexagon.get_radius(), self.hexagon.get_color(), self.surface)
                # Set the hexagon board pos
                # hexagon.set_boardPos
                hexagon.draw()
                row.append(hexagon)

            hex_grid.append(row)

        self.grid = hex_grid
        return hex_grid

    def get_grid(self):
        return self.grid

    def set_grid(self, hex_grid):
        self.grid = hex_grid

        for row in hex_grid:
            for hexagon in row:
                hexagon.draw()

    def get_hexagon_at_cursor(self, pixel):
        """
        Returns the hexagon at the specified pixel coordinate, or None if no hexagon exists at that coordinate.
        """
        hex_width = self.hexagon.get_radius() * 1.75
        hex_height = (3 ** 0.5) / 2 * hex_width

        # Determine the row and column of the hexagon that contains the specified pixel coordinate
        col = int((pixel[0] - self.coords[0]) / hex_width)
        row = int((pixel[1] - self.coords[1] - (col % 2) * hex_height / 2) / hex_height)

        # Check if the row and column are valid
        if row < 0 or row >= self.dimensions or col < 0 or col >= self.dimensions:
            return None

        # Check if the specified pixel coordinate is within the hexagon
        hex_x = hex_width * col + hex_width / 2 * (row % 2) + self.coords[0]
        hex_y = hex_height * row + self.coords[1]
        distance = math.sqrt((hex_x - pixel[0]) ** 2 + (hex_y - pixel[1]) ** 2)
        if distance > self.hexagon.get_radius():
            return None

        # Return the hexagon object at the specified row and column
        print("HEXAGON POS:"+str(self.grid[row][col]))
        return self.grid[row][col]



class Game:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn

    def __str__(self):
        return(f'GAMEOBJ=board: {self.board}, turn:{self.turn}')
    def run(self):
        # Initialize Pygame and create a window
        pygame.init()
        pygame.display.set_caption("Hex")
        clock = pygame.time.Clock()
        
        # Draw the board
        WIN.fill(WHITE)
        self.board.generate_hexagon_grid()

        # Main game loop
        running = True
        #clicks is away to distinguish between players
        clicks = 0
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicks +=1
                    # Check if the mouse is over a hexagon
                    mouse_pos = pygame.mouse.get_pos()
                    #testing
                    # print("mousepos:"+ str(mouse_pos))
                    grid = self.board.get_grid()
                    # print(grid[0][1].get_pos())
                    # print("grid:"+ str(self.board.get_hexagon_at_cursor(mouse_pos)))
                    hexagon = self.board.get_hexagon_at_cursor(mouse_pos)
                    # print('test hexagon'+str(hexagon))
                    #Testing stop
                    hexagon = self.board.get_hexagon_at_cursor(mouse_pos)
                    if hexagon is not None:
                        self.selected_hexagon = hexagon
                        self.selected_hexagon.set_color((255, 0, 0))
                        self.board.set_grid(self.board.get_grid())


            # Update the display
            pygame.display.update()

        # Clean up
        pygame.quit()
    


#Makes a surface (screen we are printing on)
class Surface:
    def __init__(self,width, height, theme, fps):
        self.width = width
        self.height = height
        self.theme = theme
        self.fps = fps


def main():
    # clock = pygame.time.Clock()
    # is_running = True
    # WIN.fill(WHITE)
    # hex1 = Hexagon(0,(40,40),20,BLACK,WIN)
    # board1 = Board(hex1,(40,40),11,WIN)
    # board1.generate_hexagon_grid()
    # grid = board1.get_grid()
    # grid[0][1].set_color((255,0,0))
    # grid[0][2].set_color((0,255,0))
    # board1.set_grid(grid)
    # pygame.display.update()

    # while is_running:
    #     clock.tick(FPS)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             is_running = False

    hex1 = Hexagon(0,(40,40),40,BLACK,WIN)
    board1 = Board(hex1,(40,40),11,WIN)
    board1.generate_hexagon_grid()
    game1 = Game(board1,None)
    game1.run()
    

if __name__ == '__main__':
    main()


# trapez form




