from chessboard import display
import time
import chess
import pygame
from PlayGame import PlayGame
from ContestUtils import BoardPiece

game = PlayGame()
move_list = game.finalMoves

pieceDict = {
	BoardPiece.BlackPawn: 'p',
	BoardPiece.BlackKnight: 'n',
	BoardPiece.BlackBishop: 'b',
	BoardPiece.BlackRook: 'r',
	BoardPiece.BlackQueen: 'q',
	BoardPiece.BlackKing: 'k',
	BoardPiece.WhitePawn: 'p',
	BoardPiece.WhiteKnight: 'n',
	BoardPiece.WhiteBishop: 'b',
	BoardPiece.WhiteRook: 'r',
	BoardPiece.WhiteQueen: 'q',
	BoardPiece.WhiteKing: 'k'
}

board = chess.Board()

game_board = display.start(board.fen())

i = 0
while True:
	display.check_for_quit()

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			if i >= len(move_list):
				break
			
			if move_list[i] != None:
				move1 = chess.Move.from_uci(move_list[i][0] + move_list[i][1] + pieceDict[move_list[i][3]])
				move2 = chess.Move.from_uci(move_list[i][0] + move_list[i][1])
				
				if move1 in board.legal_moves or move2 in board.legal_moves:
					board.push(move1)
					display.update(board.fen(), game_board)
				else:
					print("invalid move:", move_list[i][0] + move_list[i][1], move_list[i][3])
					print(*move_list, sep='\n')
					break
			
			else:
				print("No more moves possible!")
				break

			# if move in board.legal_moves:
			# 	board.push(move)
			# 	display.update(board.fen(), game_board)
			# else:
			# 	print("invalid move:", move_list[i][0] + move_list[i][1])
			# 	print(move_list)
			# 	break

			i += 1

	else:
		continue

	break

display.terminate()
