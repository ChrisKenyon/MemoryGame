import pygame
from pygame.locals import *
import random
import sys
import time

GRID_SIZE = 4
NUMBER_CARDS = GRID_SIZE**2
CARD_BORDER_WIDTH = 2
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000
CARD_HEIGHT = SCREEN_HEIGHT / GRID_SIZE - CARD_BORDER_WIDTH
CARD_WIDTH = SCREEN_WIDTH / GRID_SIZE - CARD_BORDER_WIDTH
CARD_TEXT_SIZE = CARD_WIDTH / 5
MSG_TEXT_SIZE = SCREEN_WIDTH / 20
DISPLAY_TIME = 1.5

SOLVED_COLOR = (50,40,161)
HIDDEN_COLOR = (161,40,50)
FLIPPED_COLOR = (40,161,50)

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

        # WRITE CODE HERE

        # what should you draw if self.solved? (use pygame.draw.rect)

        # what should you draw if not self.flipped? (use pygame.draw.rect)

        # what should you draw if self.flipped? (use pygame.draw.rect and screen.blit for the number)

class Grid:
    def __init__(self, size, screen):
        self.size = size
        self.grid = []
        self.screen = screen

        self.card_is_flipped = False
        self.flipped_card = None
    def populate_grid(self, values):
        """ Takes a list of values that should be equal
        to size * size. Creates cards for each value
        and populates the list of lists          """

        # WRITE CODE HERE
        # create a new card object for each spot in the grid
        # use a for loop inside a for loop
        # to create each card, you will need to make a Posn
        # object too, based on the indexes from you for loops

    def draw_all_cards(self):
        """ This is the rendering function for the grid """

        # WRITE CODE HERE
        # what function should you call on every Card to draw them?
        # (use a for loop in a for loop on self.grid)

    def check_all_solved(self):
        solved = False
        # WRITE CODE HERE
        # See if any card isn't True for self.solved
        return solved

    def update_card(self,x,y):
        """ This takes an x and y coordinate corresponding
        to the card selected on the grid and updates it
        appropriately according to the rules of Memory """
        card = self.grid[x][y]
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

        # WRITE CODE HERE
        # Make a message that says the game is over and how long you took to finish

        pygame.display.update()

def get_random_values(grid_size):
    """ This function returns a list of random integers, where
        each number has a matching pair number. This represents
        the values you will flip, which must have a matching pair
        For example, with a grid size of 4, you may return something like:
            [5, 15, 30, 23,  28, 5, 60, 15,  44, 44, 56, 23,  30, 28, 60, 56
        where you are filling a 4x4 grid with values that all have
        another value the same (i.e. there are 2 5's, 2 15's, ...) """


    # WRITE CODE HERE


    # you probably want to use this at the end
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

    # WRITE CODE HERE
    # 1. create your list of values
    # 2. create you Grid game board using the grid_size and screen
    # 3. populate the grid with the values
    # 4. run the game, which will return a duration that you should use
    # 5. draw the score using that duration

    time.sleep(10)

if __name__=="__main__":
    if NUMBER_CARDS % 2 != 0:
        raise Exception("Game board size must be divisible by 2 to make matches!")
    # Initialize pygame stuff
    pygame.init()
    pygame.display.set_caption("Memory")
    card_font = pygame.font.SysFont("monospace", CARD_TEXT_SIZE)
    msg_font = pygame.font.SysFont("monospace", MSG_TEXT_SIZE)
    run_memory_game(GRID_SIZE)
