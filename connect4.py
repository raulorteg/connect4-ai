# connect 4 game
"""
Created on Sun Nov 1 2020
@author: Raul Ortega Ochoa
"""

import numpy as np 
import pygame
import time
import copy

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

	start_button = pygame.Rect(250, 175, 100, 50)
	pygame.draw.rect(screen, GRAY, start_button)
	text = STAT_FONT.render("Start", 1, (0,0,0))
	screen.blit(text, (260, 185))

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

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if start_button.collidepoint(event.pos):
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

            elif board[row][col] == -1:
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

def is_final(board):
	# check for horizontal
	for i in range(NUM_ROWS):
		for j in range(NUM_COLS-3):
			in_row = board[i][j] + board[i][j+1]+ board[i][j+2] + board[i][j+3]
			if in_row == 4: # ai wins
				pattern = [board[i][j], board[i][j+1],
				board[i][j+2], board[i][j+3]]
				final = True
				score = 1
				return final, score, pattern

			elif in_row == -4: # human wins
				pattern = [board[i][j], board[i][j+1],
				board[i][j+2], board[i][j+3]]
				final = True
				score = -1
				return final, score, pattern

	# check for vertical
	for j in range(NUM_COLS):
		for i in range(NUM_ROWS-3):
			in_col = board[i][j] + board[i+1][j]+ board[i+2][j] + board[i+3][j]
			if in_col == 4: # ai wins
				pattern = [board[i][j], board[i+1][j],
				board[i+2][j], board[i+3][j]]
				final = True
				score = 1
				return final, score, pattern

			elif in_col == -4: # human wins
				pattern = [board[i][j], board[i+1][j],
				board[i+2][j], board[i+3][j]]
				final = True
				score = -1
				return final, score, pattern

	# TODO: check for diagonal

	for i in range(NUM_ROWS):
		for j in range(NUM_COLS):
			if board[i][j] == 0: # game not completed
				pattern = []
				score = 0
				final = False
				return final, score, pattern

	# its a tie then
	pattern = []
	score = 0
	final = True
	return final, score, pattern

def available_moves(board):
	''' given board return coordinates of next possible moves '''
	moves = []
	for col in range(NUM_COLS):
		temp = [slc[col] for slc in board]
		temp.reverse()
		valid = False
		for idx, cell in enumerate(temp):
				if cell == 0:
					valid = True
					moves.append((NUM_ROWS - idx -1 , col))
					break
	return moves


def minimax(board, USER, DEPTH):
	''' given board state return next best movement by exploring
	DEPTH steps ahead '''
	board2 = copy.deepcopy(board)
	DEPTH -= 1
	if DEPTH == -1:
		final, score, _ = is_final(board2)
		return score
		
	else:
		scores = []
		next_moves = available_moves(board)
		for move in next_moves:
			board3 = copy.deepcopy(board2)
			if USER:
				x, y = move
				board3[x][y] = -1
				final, score, _ = is_final(board3)
				if final:
					scores.append(score)
				else:
					score = minimax(board3, not USER, DEPTH)
					scores.append(score)
			else:
				x, y = move
				board3[x][y] = 1
				final, score, _ = is_final(board3)
				if final:
					scores.append(score)
				else:
					score = minimax(board=board3, USER=not USER, DEPTH=DEPTH)
					scores.append(score)


		if USER:
			return min(scores)
		else:
			return max(scores)

def game_loop(board):
	pygame.display.set_caption("Connect 4")
	RUN = True
	USER = True # true if user's turn
	while RUN:
		clock.tick(30)
		draw_board(board)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False
				pygame.quit()
				quit()

			elif (event.type == pygame.MOUSEBUTTONDOWN) and (USER):
				pos = pygame.mouse.get_pos()

				row = pos[1] // (WIDTH + MARGIN)
				col = pos[0] // (HEIGHT + MARGIN)

				temp = [slc[col] for slc in board]
				temp.reverse()
				valid = False
				for idx, cell in enumerate(temp):
					if cell == 0:
						valid = True
						temp[idx] = -1 # paint yellow
						break

				if valid:
					temp.reverse()
					for i in range(NUM_ROWS):
						board[i][col] = temp[i]

					USER = False

				final, score, pattern = is_final(board)
				if final:
					RUN = False
					break


			elif not USER:
				print("AI's turn")
				scores = []
				next_moves = available_moves(board)
				print("#"*20)
				print(next_moves)
				print("#"*20)
				for move in next_moves:
					board2 = copy.deepcopy(board)
					x, y = move

					# debugging, theres an issue with dimensions
					#print(x,y)
					#print()
					#foo = []
					#for i in range(NUM_ROWS):
					#	print(foo)
					#	foo = []
					#	for j in range(NUM_COLS):
					#		foo.append((i,j))
					#print(foo)
					#print()

					#board2[x][y] = 1
					#for foo in board2:
					#	print(foo)

					#print()
					score = minimax(board=board2, USER=USER, DEPTH = 4)
					scores.append(score)
				print(scores)

				scores = np.array(scores)
				idx = np.argmax(scores)
				x, y = next_moves[idx]
				board[x][y] = 1
				USER = True

			final, score, pattern = is_final(board)
			if final:
				RUN = False
				break

	# finished game
	# TODO: Display winner, show winning pattern, show end screen

				

if __name__ == "__main__":
	intro_menu()
	game_loop(board)