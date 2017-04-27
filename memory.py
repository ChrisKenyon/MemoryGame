import pygame
from pygame.locals import *
import random
import sys
import time

GRID_SIZE = 2
NUMBER_CARDS = GRID_SIZE**2
CARD_BORDER_WIDTH = 2
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000
CARD_HEIGHT = SCREEN_HEIGHT / GRID_SIZE - CARD_BORDER_WIDTH
CARD_WIDTH = SCREEN_WIDTH / GRID_SIZE - CARD_BORDER_WIDTH
CARD_TEXT_SIZE = CARD_WIDTH / 5
MSG_TEXT_SIZE = SCREEN_WIDTH / 20
DISPLAY_TIME = 1.5


class Posn:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Card:
    def __init__(self, posn, value):
        self.posn = posn
        self.value = value

        self.solved = False
        self.flipped = False
    def draw_card(self,screen):
        draw_x = self.posn.x * (CARD_WIDTH+CARD_BORDER_WIDTH)
        draw_y = self.posn.y * (CARD_HEIGHT+CARD_BORDER_WIDTH)
        if self.solved:
            pygame.draw.rect(screen, (50,40,161), (draw_x,draw_y,CARD_HEIGHT,CARD_WIDTH))
        elif not self.flipped:
            pygame.draw.rect(screen, (161,40,50), (draw_x,draw_y,CARD_HEIGHT,CARD_WIDTH))
        elif self.flipped:
            pygame.draw.rect(screen, (40,161,50), (draw_x,draw_y,CARD_HEIGHT,CARD_WIDTH))
            label = card_font.render(str(self.value), 1, (255,255,0))
            center_x = draw_x + CARD_WIDTH/2 - CARD_TEXT_SIZE/2
            center_y = draw_y + CARD_HEIGHT/2 - CARD_TEXT_SIZE/2
            screen.blit(label, (center_x, center_y))

class Grid:
    def __init__(self, size, screen):
        self.size = size
        self._grid = []
        self.screen = screen

        self.card_is_flipped = False
        self.flipped_card = None
    def populate_grid(self, values):
        """ Takes a list of values that should be equal
        to size * size. Creates cards for each value
        and populates the list of lists          """
        for column in range(self.size):
            self._grid.append([])
            for row in range(self.size):
                position = Posn(column, row)
                new_card = Card(position, values.pop(0))
                self._grid[column].append(new_card)
    def draw_all_cards(self):
        """ This is the rendering function for the grid """
        for column in self._grid:
            for card in column:
                card.draw_card(self.screen)
    def check_all_solved(self):
        for column in self._grid:
            for card in column:
                if not card.solved:
                    return False
        return True
    def update_card(self,x,y):
        """ This takes an x and y coordinate corresponding
        to the card selected on the grid and updates it
        appropriately according to the rules of Memory """
        card = self._grid[x][y]
        if card.solved or card.flipped:
            # do nothing if this card is solved or flipped already
            return
        elif self.card_is_flipped:
            if card.value == self.flipped_card.value:
                # If we have a match, call both cards solved
                card.solved = True
                self.flipped_card.solved = True
            else:
                # Otherwise we don't have a match, so we should
                # display the incorrect valued card for a short time
                card.flipped = True
                card.draw_card(self.screen)
                pygame.display.update()
                time.sleep(DISPLAY_TIME)
                # and then hide it again
                card.flipped = False
                # along with the previously flipped card
                self.flipped_card.flipped = False
            # and remember that we dont have a flipped card anymore
            self.card_is_flipped = False
            self.flipped_card = None
        elif not self.card_is_flipped:
            # if we didn't have a flipped card, then flip this one
            card.flipped = True
            # and remember that we have a currently flipped card
            self.flipped_card = card
            self.card_is_flipped = True
    def draw_score(self, duration):
        message = "Completed in {} seconds.".format(duration)
        label = msg_font.render(message, 1, (255,255,255))
        center_x = SCREEN_WIDTH/10
        center_y = SCREEN_HEIGHT/2 - MSG_TEXT_SIZE/2
        self.screen.blit(label, (center_x, center_y))
        pygame.display.update()

def get_random_values(grid_size):
    num_elements = grid_size**2
    max_value = grid_size*10 # adjust later for difficulty
    values = []
    for i in range(num_elements/2):
        new_val = random.randint(1,max_value)
        values.append(new_val)
        # append twice to account for match
        values.append(new_val)
    random.shuffle(values)
    return values

def handle_click(game_board):
    click_x, click_y = pygame.mouse.get_pos()
    card_x = click_x/CARD_WIDTH
    card_y = click_y/CARD_HEIGHT
    game_board.update_card(card_x,card_y)

def run_pygame_loop(game_board):
    start_time = time.time()
    game_over = False
    # Developed with the help of usingpython.com/pygame-intro/
    while not game_over:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                handle_click(game_board)
                game_over = game_board.check_all_solved()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        game_board.draw_all_cards()
        pygame.display.update()

    # return how long it took
    duration = time.time() - start_time
    duration = round(duration, 2)
    return duration


def run_memory_game(grid_size):
    screen = pygame.display.set_mode((1000,1000))
    values = get_random_values(grid_size)
    game_board = Grid(grid_size, screen)
    game_board.populate_grid(values)
    duration = run_pygame_loop(game_board)
    game_board.draw_score(duration)
    time.sleep(10)

if __name__=="__main__":
    if NUMBER_CARDS % 2 != 0:
        raise Exception("Game board size must be divisible by 2 to make matches!")
    pygame.init()
    pygame.display.set_caption("Memory")
    card_font = pygame.font.SysFont("monospace", CARD_TEXT_SIZE)
    msg_font = pygame.font.SysFont("monospace", MSG_TEXT_SIZE)
    run_memory_game(GRID_SIZE)
