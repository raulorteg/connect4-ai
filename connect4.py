# connect 4 game
"""
Created on Sun Nov 1 2020
@author: Raul Ortega Ochoa
"""

import numpy as np 
import pygame
import time
pygame.font.init()

# board dimensions
NUM_ROWS = 6
NUM_COLS = 7

# defining RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255,255,0) 
RED = (255,0,0)
GRAY = (211,211,211)

# Grid settings on Pygame
HEIGHT = 50
WIDTH = HEIGHT
MARGIN = 5

# window settings
WIN_HEIGHT = 335
WIN_WIDTH = 600

# font for text
STAT_FONT = pygame.font.SysFont("comicsans", 50)

board = []
for row in range(NUM_ROWS):
	board.append([])
	for col in range(NUM_COLS):
		board[row].append(0)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])

def intro_menu():
	clock.tick(30)

	pygame.display.set_caption("Press RETURN/ENTER to start")
	screen.fill(WHITE)
	text = STAT_FONT.render("CONNECT 4", 1, (0,0,0))
	screen.blit(text, (200, 100))

	pygame.display.flip()
	start = False
	while not start:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			elif event.type == pygame.KEYDOWN:
				if event.key==pygame.K_RETURN:
					start = True

		



def draw_board(board):

    screen.fill(GRAY) # fill background in grey

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == 1:
                color = RED
                pygame.draw.rect(screen, color, 
                                 [(MARGIN + WIDTH) * col + MARGIN, 
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH, HEIGHT])

            elif board[row][col] == 2:
                color = YELLOW
                pygame.draw.rect(screen, color, 
                                 [(MARGIN + WIDTH) * col + MARGIN, 
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH, HEIGHT])

            else:
                color = WHITE
                pygame.draw.rect(screen, color, 
                                 [(MARGIN + WIDTH) * col + MARGIN, 
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH, HEIGHT])

    pygame.display.flip()

def main(board):
	pygame.display.set_caption("CONNECT4")
	run = True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()

		draw_board(board)

if __name__ == "__main__":
	intro_menu()
	main(board)