from chessboard import display
import time
import chess
import pygame
from PlayGame import PlayGame


game = PlayGame()
move_list = game.finalMoves

board = chess.Board()

game_board = display.start(board.fen())

i = 0
while True:
	display.check_for_quit()

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			if i >= len(move_list):
				break

			move = chess.Move.from_uci(move_list[i][0] + move_list[i][1])
			
			if move in board.legal_moves:
				board.push(move)
				display.update(board.fen(), game_board)
			else:
				print("invalid move:", move_list[i][0] + move_list[i][1])
				print(move_list)
				break

			i += 1

	else:
		continue

	break

display.terminate()
