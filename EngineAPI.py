"""
Write your code in this file to participate in the Chess Bot challenge!

Username: ghosty
"""
from ContestUtils import PlayerColour
from ContestUtils import BoardState, BoardPiece
import random

files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

class Engine:
	def __init__(self, colour, time_per_move: float):
		if colour == PlayerColour.White:
			self.color = 0
		else:
			self.color = 1

		self.time_per_move = time_per_move
	
	def get_move(self, board_state: BoardState):
		pos = {}
		possibleList = []
		enemyPosList = []
		pawnList = []

		# get old map
		for file in files:
			for rank in ranks:
				pos[file+rank] = board_state.piece_at(file, rank)

				if self.color == 0:
					if str(pos[file+rank]).find('Empty') != -1: # empty square
						possibleList.append(file+rank)

					else:
						if str(pos[file+rank]).find('White') == -1: # black square
							enemyPosList.append(file+rank)

						elif str(pos[file+rank]).find('Pawn') != -1: # white pawn
							pawnList.append(file+rank)

				else:
					if str(pos[file+rank]).find('Empty') != -1: # empty square
						possibleList.append(file+rank)

					else:
						if str(pos[file+rank]).find('Black') == -1: # white square
							enemyPosList.append(file+rank)

						elif str(pos[file+rank]).find('Pawn') != -1: # black pawn
							pawnList.append(file+rank)


		# return the new BoardState and the (oldPos, newPos) combo. Remove the latter in production

		pawns = Pawns(self.color, possibleList, pawnList, enemyPosList)

		optimalPawnMove = pawns.chooseOptimalMove()

		pos[optimalPawnMove[0]] = BoardPiece.EmptySquare
		
		if(self.color == 0):
			pos[optimalPawnMove[1]] = BoardPiece.WhitePawn
		else:
			pos[optimalPawnMove[1]] = BoardPiece.BlackPawn

		newBoardState = BoardState(pos)

		return newBoardState, optimalPawnMove
	
def nextChar(char: chr, inc: int):
	return chr(ord(char)+inc)

class Pawns:
	def __init__(self, color: int, possibleList: list, pawnList: list, enemyPosList: list):
		self.color = color
		self.pawnList = pawnList
		self.enemyPosList = enemyPosList
		self.possibleList = possibleList

	def getNormalMoves(self) -> list:
		# return a list of possible moves
		moves = []

		for pawn in self.pawnList:
			if self.color == 0:
				if pawn[1] == '8':
					# get new piece (queen, duh)
					continue

				if pawn[0] + nextChar(pawn[1], 1) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], 1)])

				if pawn[1] == '2' and pawn[0] + nextChar(pawn[1], 2) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], 2)])

			else:
				if pawn[1] == '1':
					# get new piece (queen, duh)
					continue

				if pawn[0] + nextChar(pawn[1], -1) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], -1)])

				if pawn[1] == '7' and pawn[0] + nextChar(pawn[1], -2) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], -2)])

		return moves

	def getAttackingMoves(self) -> list:
		moves = []

		for pawn in self.pawnList:
			if self.color == 0:
				if nextChar(pawn[0], 1) + nextChar(pawn[1], 1) in self.enemyPosList:
					moves.append([pawn, nextChar(pawn[0], 1) + nextChar(pawn[1], 1)])

				if nextChar(pawn[0], -1) + nextChar(pawn[1], 1) in self.enemyPosList:
					moves.append([pawn, nextChar(pawn[0], -1) + nextChar(pawn[1], 1)])

			else:
				if nextChar(pawn[0], 1) + nextChar(pawn[1], -1) in self.enemyPosList:
					moves.append([pawn, nextChar(pawn[0], 1) + nextChar(pawn[1], -1)])

				if nextChar(pawn[0], -1) + nextChar(pawn[1], -1) in self.enemyPosList:
					moves.append([pawn, nextChar(pawn[0], -1) + nextChar(pawn[1], -1)])

		return moves

	def chooseOptimalMove(self) -> list:
		# return a list of 2 elements, the start and end pos
		moves = []
		moves.extend(self.getNormalMoves())
		moves.extend(self.getAttackingMoves())
		moves = [elem for elem in moves if elem != []]
		# simulate optimal play for x depth, then choose best move
		# currently, choose random move

		return random.choice(moves)

