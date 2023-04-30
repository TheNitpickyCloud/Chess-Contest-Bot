"""
Write your code in this file to participate in the Chess Bot challenge!

Username: ghosty
"""
from ContestUtils import PlayerColour
from ContestUtils import BoardState, BoardPiece
import random

files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
pointsDict = {
	BoardPiece.BlackPawn: 1,
	BoardPiece.BlackKnight: 3,
	BoardPiece.BlackBishop: 3,
	BoardPiece.BlackRook: 5,
	BoardPiece.BlackQueen: 9,
	BoardPiece.BlackKing: 100000,
	BoardPiece.WhitePawn: 1,
	BoardPiece.WhiteKnight: 3,
	BoardPiece.WhiteBishop: 3,
	BoardPiece.WhiteRook: 5,
	BoardPiece.WhiteQueen: 9,
	BoardPiece.WhiteKing: 100000
}

class Engine:
	def __init__(self, colour, time_per_move: float):
		if colour == PlayerColour.White:
			self.color = 0
		else:
			self.color = 1

		self.time_per_move = time_per_move
		self.points = 0
	
	def get_move(self, board_state: BoardState):
		pos = {}
		possibleList = []
		enemyPosDict = {}
		pawnList = []
		knightList = []

		# get old map
		for file in files:
			for rank in ranks:
				pos[file+rank] = board_state.piece_at(file, rank)

				if self.color == 0:
					if str(pos[file+rank]).find('Empty') != -1: # empty square
						possibleList.append(file+rank)

					else:
						if str(pos[file+rank]).find('White') == -1: # black square
							enemyPosDict[file+rank] = pointsDict[pos[file+rank]]

						elif str(pos[file+rank]).find('Pawn') != -1: # white pawn
							pawnList.append(file+rank)

						elif str(pos[file+rank]).find('Knight') != -1: # white knight
							knightList.append(file+rank)

				else:
					if str(pos[file+rank]).find('Empty') != -1: # empty square
						possibleList.append(file+rank)

					else:
						if str(pos[file+rank]).find('Black') == -1: # white square
							enemyPosDict[file+rank] = pointsDict[pos[file+rank]]

						elif str(pos[file+rank]).find('Pawn') != -1: # black pawn
							pawnList.append(file+rank)

						elif str(pos[file+rank]).find('Knight') != -1: # black knight
							knightList.append(file+rank)


		# return the new BoardState and the (oldPos, newPos) combo. Remove the latter in production

		pawns = Pawns(self.color, possibleList, pawnList, enemyPosDict)
		knights = Knights(self.color, possibleList, knightList, enemyPosDict)

		pawnMoves = pawns.getMoves()
		knightMoves = knights.getMoves()

		all_moves = []
		all_moves.extend(pawnMoves)
		all_moves.extend(knightMoves)


		optimalMove = getOptimalMove(self.color, board_state, all_moves, 1, 2)
		# optimalMove = random.choice(pawnMoves)

		self.points += optimalMove[2]

		pos[optimalMove[0]] = BoardPiece.EmptySquare
		
		pos[optimalMove[1]] = optimalMove[3]

		newBoardState = BoardState(pos)

		return newBoardState, optimalMove
	
class TestEngine:
	def __init__(self, colour, time_per_move: float, depth: int, finalDepth: int):
		if colour == PlayerColour.White:
			self.color = 0
		else:
			self.color = 1

		self.time_per_move = time_per_move
		self.depth = depth
		self.finalDepth = finalDepth
	
	def get_move(self, board_state: BoardState):
		pos = {}
		possibleList = []
		enemyPosDict = {} # enemy pos, points
		pawnList = []
		knightList = []

		# get old map
		for file in files:
			for rank in ranks:
				pos[file+rank] = board_state.piece_at(file, rank)

				if self.color == 0:
					if str(pos[file+rank]).find('Empty') != -1: # empty square
						possibleList.append(file+rank)

					else:
						if str(pos[file+rank]).find('White') == -1: # black square
							enemyPosDict[file+rank] = pointsDict[pos[file+rank]]

						elif str(pos[file+rank]).find('Pawn') != -1: # white pawn
							pawnList.append(file+rank)

						elif str(pos[file+rank]).find('Knight') != -1: # white knight
							knightList.append(file+rank)

				else:
					if str(pos[file+rank]).find('Empty') != -1: # empty square
						possibleList.append(file+rank)

					else:
						if str(pos[file+rank]).find('Black') == -1: # white square
							enemyPosDict[file+rank] = pointsDict[pos[file+rank]]

						elif str(pos[file+rank]).find('Pawn') != -1: # black pawn
							pawnList.append(file+rank)

						elif str(pos[file+rank]).find('Knight') != -1: # white knight
							knightList.append(file+rank)


		pawns = Pawns(self.color, possibleList, pawnList, enemyPosDict)
		knights = Knights(self.color, possibleList, knightList, enemyPosDict)

		pawnMoves = pawns.getMoves()
		knightMoves = knights.getMoves()

		all_moves = []
		all_moves.extend(pawnMoves)
		all_moves.extend(knightMoves)

		optimalMove = getOptimalMove(self.color, board_state, all_moves, self.depth, self.finalDepth)

		pos[optimalMove[0]] = BoardPiece.EmptySquare
		
		pos[optimalMove[1]] = optimalMove[3]

		newBoardState = BoardState(pos)

		return newBoardState, optimalMove, optimalMove[2]


def getOptimalMove(color, currBoardState, moves, depth, finalDepth): # finalDepth will always be even, base case will always be opposing
	# simulate optimal play for x depth, then choose best move
	# currently, choose random move
	# return random.choice(moves)

	moves.sort(key = lambda x: x[2])

	# base case, return the move with the max score
	if depth == finalDepth:
		# print(color, depth, moves[-1])
		return moves[-1]
	
	testPlayer = None
	if color == 0: # am white, next player will be black
		testPlayer = TestEngine(PlayerColour.Black, 5.0, depth+1, finalDepth)
	else: # am black, next player will be white
		testPlayer = TestEngine(PlayerColour.White, 5.0, depth+1, finalDepth)

	maxScore = -float('inf')
	theMove = None

	for move in moves:
		pos = {}
		for file in files:
			for rank in ranks:
				pos[file+rank] = currBoardState.piece_at(file, rank)

		pos[move[0]] = BoardPiece.EmptySquare
		
		pos[move[1]] = move[3]

		newBoardState = BoardState(pos)

		possMove = testPlayer.get_move(newBoardState)

		if move[2] - possMove[2] > maxScore: # maximize the score
			theMove = move
			maxScore = move[2] - possMove[2]

	# print(color, depth, theMove)
	return theMove

def nextChar(char: chr, inc: int):
	return chr(ord(char)+inc)

class Pawns:
	def __init__(self, color: int, possibleList: list, pawnList: list, enemyPosDict: dict):
		self.color = color
		self.pawnList = pawnList
		self.enemyPosDict = enemyPosDict
		self.possibleList = possibleList

	def getNormalMoves(self) -> list:
		# return a list of possible moves in the format (start, end, points)
		moves = []

		for pawn in self.pawnList:
			if self.color == 0:
				if pawn[1] == '8':
					# get new piece (queen, duh)
					continue

				if pawn[0] + nextChar(pawn[1], 1) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], 1), 0])

				if pawn[1] == '2' and pawn[0] + nextChar(pawn[1], 1) in self.possibleList and pawn[0] + nextChar(pawn[1], 2) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], 2), 0])

			else:
				if pawn[1] == '1':
					# get new piece (queen, duh)
					continue

				if pawn[0] + nextChar(pawn[1], -1) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], -1), 0])

				if pawn[1] == '7' and pawn[0] + nextChar(pawn[1], -1) in self.possibleList and pawn[0] + nextChar(pawn[1], -2) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], -2), 0])

		return moves

	def getAttackingMoves(self) -> list:
		moves = []

		for pawn in self.pawnList:
			if self.color == 0:
				if nextChar(pawn[0], 1) + nextChar(pawn[1], 1) in self.enemyPosDict:
					moves.append([pawn, nextChar(pawn[0], 1) + nextChar(pawn[1], 1), self.enemyPosDict[nextChar(pawn[0], 1) + nextChar(pawn[1], 1)]])

				if nextChar(pawn[0], -1) + nextChar(pawn[1], 1) in self.enemyPosDict:
					moves.append([pawn, nextChar(pawn[0], -1) + nextChar(pawn[1], 1), self.enemyPosDict[nextChar(pawn[0], -1) + nextChar(pawn[1], 1)]])

			else:
				if nextChar(pawn[0], 1) + nextChar(pawn[1], -1) in self.enemyPosDict:
					moves.append([pawn, nextChar(pawn[0], 1) + nextChar(pawn[1], -1), self.enemyPosDict[nextChar(pawn[0], 1) + nextChar(pawn[1], -1)]])

				if nextChar(pawn[0], -1) + nextChar(pawn[1], -1) in self.enemyPosDict:
					moves.append([pawn, nextChar(pawn[0], -1) + nextChar(pawn[1], -1), self.enemyPosDict[nextChar(pawn[0], -1) + nextChar(pawn[1], -1)]])

		return moves

	def getMoves(self) -> list:
		# return a list of 4 elements, the start pos, end pos, points and the piece
		moves = []
		moves.extend(self.getNormalMoves())
		moves.extend(self.getAttackingMoves())
		moves = [elem for elem in moves if elem != []]
		
		if self.color == 0:
			for elem in moves:
				elem.append(BoardPiece.WhitePawn)

		else:
			for elem in moves:
				elem.append(BoardPiece.BlackPawn)

		return moves

class Knights:
	def __init__(self, color: int, possibleList: list, knightList: list, enemyPosDict: dict):
		self.color = color
		self.knightList = knightList
		self.enemyPosDict = enemyPosDict
		self.possibleList = possibleList

	def getAllMoves(self) -> list:
		# return a list of possible moves in the format (start, end, points)
		moves = []

		for knight in self.knightList:
			# normal moves
			if nextChar(knight[0], 2) + nextChar(knight[1], 1) in self.possibleList:
				moves.append([knight, nextChar(knight[0], 2) + nextChar(knight[1], 1), 0])

			if nextChar(knight[0], 2) + nextChar(knight[1], -1) in self.possibleList:
				moves.append([knight, nextChar(knight[0], 2) + nextChar(knight[1], -1), 0])

			if nextChar(knight[0], -2) + nextChar(knight[1], 1) in self.possibleList:
				moves.append([knight, nextChar(knight[0], -2) + nextChar(knight[1], 1), 0])

			if nextChar(knight[0], -2) + nextChar(knight[1], -1) in self.possibleList:
				moves.append([knight, nextChar(knight[0], -2) + nextChar(knight[1], -1), 0])

			if nextChar(knight[0], 1) + nextChar(knight[1], 2) in self.possibleList:
				moves.append([knight, nextChar(knight[0], 1) + nextChar(knight[1], 2), 0])

			if nextChar(knight[0], 1) + nextChar(knight[1], -2) in self.possibleList:
				moves.append([knight, nextChar(knight[0], 1) + nextChar(knight[1], -2), 0])

			if nextChar(knight[0], -1) + nextChar(knight[1], 2) in self.possibleList:
				moves.append([knight, nextChar(knight[0], -1) + nextChar(knight[1], 2), 0])

			if nextChar(knight[0], -1) + nextChar(knight[1], -2) in self.possibleList:
				moves.append([knight, nextChar(knight[0], -1) + nextChar(knight[1], -2), 0])

			# attacking moves
			if nextChar(knight[0], 2) + nextChar(knight[1], 1) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], 2) + nextChar(knight[1], 1), self.enemyPosDict[nextChar(knight[0], 2) + nextChar(knight[1], 1)]])

			if nextChar(knight[0], 2) + nextChar(knight[1], -1) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], 2) + nextChar(knight[1], -1), self.enemyPosDict[nextChar(knight[0], 2) + nextChar(knight[1], -1)]])

			if nextChar(knight[0], -2) + nextChar(knight[1], 1) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], -2) + nextChar(knight[1], 1), self.enemyPosDict[nextChar(knight[0], -2) + nextChar(knight[1], 1)]])

			if nextChar(knight[0], -2) + nextChar(knight[1], -1) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], -2) + nextChar(knight[1], -1), self.enemyPosDict[nextChar(knight[0], -2) + nextChar(knight[1], -1)]])

			if nextChar(knight[0], 1) + nextChar(knight[1], 2) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], 1) + nextChar(knight[1], 2), self.enemyPosDict[nextChar(knight[0], 1) + nextChar(knight[1], 2)]])

			if nextChar(knight[0], 1) + nextChar(knight[1], -2) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], 1) + nextChar(knight[1], -2), self.enemyPosDict[nextChar(knight[0], 1) + nextChar(knight[1], -2)]])

			if nextChar(knight[0], -1) + nextChar(knight[1], 2) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], -1) + nextChar(knight[1], 2), self.enemyPosDict[nextChar(knight[0], -1) + nextChar(knight[1], 2)]])

			if nextChar(knight[0], -1) + nextChar(knight[1], -2) in self.enemyPosDict:
				moves.append([knight, nextChar(knight[0], -1) + nextChar(knight[1], -2), self.enemyPosDict[nextChar(knight[0], -1) + nextChar(knight[1], -2)]])

		return moves

	def getMoves(self) -> list:
		# return a list of 4 elements, the start pos, end pos, points and the piece
		moves = []
		moves.extend(self.getAllMoves())
		moves = [elem for elem in moves if elem != []]
		
		if self.color == 0:
			for elem in moves:
				elem.append(BoardPiece.WhiteKnight)

		else:
			for elem in moves:
				elem.append(BoardPiece.BlackKnight)

		return moves
	