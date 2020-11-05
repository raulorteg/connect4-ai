# connect 4 game
"""
Created on Sun Nov 1 2020
@author: Raul Ortega Ochoa
"""

import numpy as np 
import pygame
import time
import copy
import random

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

# store scores from previous games
score_hist = []

# window settings
WIN_HEIGHT = 335
WIN_WIDTH = 600

# font for text
STAT_FONT = pygame.font.SysFont("comicsans", 50)
STAT_FONT_SMALL = pygame.font.SysFont("comicsans", 30)

# load background
IMG_BG = pygame.image.load("background.jpg")
IMG2_BG = pygame.image.load("background2.jpg")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])

class Background:
	VEL = 1
	WIDTH = IMG_BG.get_width()
	IMG = IMG_BG
	IMG2 = IMG2_BG

	def __init__(self):
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1, 0))
		win.blit(self.IMG2, (self.x2, 0))


def intro_menu():
	clock.tick(30)
	background = Background()
	pygame.display.set_caption("Press RETURN/ENTER to start")
	screen.fill(WHITE)

	pygame.display.flip()
	start = False
	while not start:
		time.sleep(0.05)
		background.move()
		background.draw(screen)

		text = STAT_FONT.render("CONNECT 4", 1, (0,0,0))
		screen.blit(text, (200, 100))

		start_button = pygame.Rect(250, 175, 100, 50)
		pygame.draw.rect(screen, GRAY, start_button)
		text = STAT_FONT.render("Start", 1, (0,0,0))
		screen.blit(text, (260, 185))

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
		pygame.display.flip()
	return start

def draw_board(board):

    screen.fill(GRAY) # fill background in grey

    losses = len([x for x in score_hist if x==1])
    ties = len([x for x in score_hist if x==0])
    wins = len([x for x in score_hist if x==-1])

    score_text = "Human: {}".format(wins)
    text = STAT_FONT_SMALL.render(score_text, 1, (0,0,0))
    screen.blit(text, (400, 10))

    score_text = "AI: {}".format(losses)
    text = STAT_FONT_SMALL.render(score_text, 1, (0,0,0))
    screen.blit(text, (400, 50))

    score_text = "Ties: {}".format(ties)
    text = STAT_FONT_SMALL.render(score_text, 1, (0,0,0))
    screen.blit(text, (400, 90))

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
				pattern = [(i,j), (i,j+1),
				(i,j+2), (i,j+3)]
				final = True
				score = 1
				return final, score, pattern

			elif in_row == -4: # human wins
				pattern = [(i,j), (i,j+1),
				(i,j+2), (i,j+3)]
				final = True
				score = -1
				return final, score, pattern

	# check for vertical
	for j in range(NUM_COLS):
		for i in range(NUM_ROWS-3):
			in_col = board[i][j] + board[i+1][j]+ board[i+2][j] + board[i+3][j]
			if in_col == 4: # ai wins
				pattern = [(i,j), (i+1,j), (i+2,j), (i+3,j)]
				final = True
				score = 1
				return final, score, pattern

			elif in_col == -4: # human wins
				pattern = [(i,j), (i+1,j), (i+2,j), (i+3,j)]
				final = True
				score = -1
				return final, score, pattern

	# inverse diagonal
	for i in [3,4,5]:
		for j in [0,1,2,3]:
			in_diag = board[i][j] + board[i-1][j+1]+ board[i-2][j+2] + board[i-3][j+3]
			if in_diag == 4: # ai wins
				pattern = [(i,j), (i-1,j+1), (i-2,j+2), (i-3,j+3)]
				final = True
				score = 1
				return final, score, pattern

			elif in_diag == -4: # ai wins
				pattern = [(i,j), (i-1,j+1), (i-2,j+2), (i-3,j+3)]
				final = True
				score = -1
				return final, score, pattern

	# direct diagonal
	for i in [0,1,2]:
		for j in [0,1,2,3]:
			in_diag = board[i][j] + board[i+1][j+1]+ board[i+2][j+2] + board[i+3][j+3]
			if in_diag == 4: # ai wins
				pattern = [(i,j), (i+1,j+1), (i+2,j+2), (i+3,j+3)]
				final = True
				score = 1
				return final, score, pattern

			elif in_diag == -4: # ai wins
				pattern = [(i,j), (i+1,j+1), (i+2,j+2), (i+3,j+3)]
				final = True
				score = -1
				return final, score, pattern

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

def minimax(board, user, DEPTH):
	''' given board state return next best movement by exploring
	DEPTH steps ahead '''
	board2 = copy.deepcopy(board)
	DEPTH -= 1

	final, score, _ = is_final(board2)
	if (final) or (DEPTH == -1):
		return score
		
	else:
		scores = []
		next_moves = available_moves(board)
		for move in next_moves:
			board3 = copy.deepcopy(board2)
			if user:
				x, y = move
				board3[x][y] = -1
				final, score, _ = is_final(board3)
				if final:
					scores.append(score)
				else:
					score = minimax(board=board3, user=not user, DEPTH=DEPTH)
					scores.append(score)
			else:
				x, y = move
				board3[x][y] = 1
				final, score, _ = is_final(board3)
				if final:
					scores.append(score)
				else:
					score = minimax(board=board3, user=not user, DEPTH=DEPTH)
					scores.append(score)


		if user:
			return min(scores)
		else:
			return max(scores)

def game_loop():

	board = []
	for row in range(NUM_ROWS):
		board.append([])
		for col in range(NUM_COLS):
			board[row].append(0)

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


			elif not USER:
				final, score, pattern = is_final(board)

				if final:
					RUN = False
					break

				scores = []
				next_moves = available_moves(board)

				for move in next_moves:
					board2 = copy.deepcopy(board)
					x, y = move
					board2[x][y] = 1 # paint red
					score = minimax(board=board2, user=True, DEPTH = 3)
					scores.append(score)

				# choose best option (max) if tie
				# in best option pick random among best
				max_score = max(scores)
				indices = [idx for idx, x in enumerate(scores) if x == max_score]
				idx = random.choice(indices)

				x, y = next_moves[idx]
				board[x][y] = 1
				USER = True

			final, score, pattern = is_final(board)
			if final:
				draw_board(board)
				RUN = False
				break

	# finished game
	EXIT = False
	animation_iter = 0
	while (not EXIT) and (animation_iter < 5):
		clock.tick(60)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				EXIT = True
				pygame.quit()
				quit()

		# simple blinking animation
		if final != 0: # not tie
			for pair in pattern:
				x, y = pair
				board[x][y] = 0

			draw_board(board)
			time.sleep(0.3)

			for pair in pattern:
				x, y = pair
				board[x][y] = score

			draw_board(board)
			time.sleep(0.3)

		animation_iter += 1
	return score

def end_menu(score):
	clock.tick(30)
	background = Background()
	screen.fill(WHITE)
	# screen.blit(IMG_BG, [0, 0])
	pygame.display.set_caption("Press RETURN/ENTER to start")

	if score == -1: # Human
		text = STAT_FONT.render("You won!", 1, (0,0,0))
	elif score == 1: # AI
		text = STAT_FONT.render("GAME OVER", 1, (0,0,0))
	else:
		text = STAT_FONT.render("It's a Tie!", 1, (0,0,0))

	pygame.display.flip()
	start = False
	while not start:
		time.sleep(0.05)
		background.move()
		background.draw(screen)

		screen.blit(text, (200, 100))
		start_button = pygame.Rect(210, 155, 200, 50)
		pygame.draw.rect(screen, GRAY, start_button)
		text_restart = STAT_FONT.render("Play again", 1, (0,0,0))
		screen.blit(text_restart, (220, 165))

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
					
		pygame.display.flip()

	return start

if __name__ == "__main__":
	start = intro_menu()
	while start:
		score = game_loop()
		start = end_menu(score)
		score_hist.append(score)

