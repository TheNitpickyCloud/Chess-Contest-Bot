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
	BoardPiece.BlackKing: 0,
	BoardPiece.WhitePawn: 1,
	BoardPiece.WhiteKnight: 3,
	BoardPiece.WhiteBishop: 3,
	BoardPiece.WhiteRook: 5,
	BoardPiece.WhiteQueen: 9,
	BoardPiece.WhiteKing: 0
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

		# get old map
		for file in files:
			for rank in ranks:
				pos[file+rank] = board_state.piece_at(file, rank)

		optimalMove = getOptimalMove(self.color, self.color, board_state, 1, 2)
		# optimalMove = random.choice(pawnMoves)

		self.points += optimalMove[2]

		pos[optimalMove[0]] = BoardPiece.EmptySquare
		
		pos[optimalMove[1]] = optimalMove[3]

		newBoardState = BoardState(pos)

		return newBoardState, optimalMove

def get_all_moves(color: int, board_state: BoardState) -> list:
	pos = {}
	possibleList = []
	enemyPosDict = {} # enemy pos, points
	pawnList = []
	knightList = []
	bishopList = []

	# get map
	for file in files:
		for rank in ranks:
			pos[file+rank] = board_state.piece_at(file, rank)

			if color == 0:
				if str(pos[file+rank]).find('Empty') != -1: # empty square
					possibleList.append(file+rank)

				else:
					if str(pos[file+rank]).find('White') == -1: # black square
						enemyPosDict[file+rank] = pointsDict[pos[file+rank]]

					elif str(pos[file+rank]).find('Pawn') != -1: # white pawn
						pawnList.append(file+rank)

					elif str(pos[file+rank]).find('Knight') != -1: # white knight
						knightList.append(file+rank)

					elif str(pos[file+rank]).find('Bishop') != -1: # white bishop
						bishopList.append(file+rank)

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

					elif str(pos[file+rank]).find('Bishop') != -1: # black bishop
						bishopList.append(file+rank)

	pawns = Pawns(color, possibleList, pawnList, enemyPosDict)
	knights = Knights(color, possibleList, knightList, enemyPosDict)
	bishops = Bishops(color, possibleList, bishopList, enemyPosDict)

	pawnMoves = pawns.getMoves()
	knightMoves = knights.getMoves()
	bishopMoves = bishops.getMoves()

	all_moves = []
	all_moves.extend(pawnMoves)
	all_moves.extend(knightMoves)
	all_moves.extend(bishopMoves)

	return all_moves

def get_board_score(color: int, board_state: BoardState) -> int:
	blackScore = 0
	whiteScore = 0

	for file in files:
		for rank in ranks:
			piece = board_state.piece_at(file, rank)

			if str(piece).find("Resignation") != -1: # resigned
				return 0

			if str(piece).find('Empty') == -1: # not empty square
				if str(piece).find('Black') == -1: # white square
					whiteScore += pointsDict[piece]

				else: # black square
					blackScore += pointsDict[piece]

	if color == 0:
		return whiteScore - blackScore
	else:
		return blackScore - whiteScore

def getOptimalMove(color: int, initColor: int, currBoardState: BoardState, depth: int, finalDepth: int):
	# simulate optimal play for x depth, then choose best move

	theScore = None
	otherPlayer = None
	moveList = []

	if color != initColor:
		theScore = float('inf')
	else:
		theScore = -float('inf')

	if color == 0:
		otherPlayer = 1
	else:
		otherPlayer = 0

	# get moves
	moves = get_all_moves(color, currBoardState)

	# base cases
	if len(moves) == 0:
		return ['a1', 'a1', 0, BoardPiece.Resignation]

	if depth == finalDepth:
		if color != initColor: # enemy move, return min score
			for move in moves:
				pos = {}
				for file in files:
					for rank in ranks:
						pos[file+rank] = currBoardState.piece_at(file, rank)

				pos[move[0]] = BoardPiece.EmptySquare
		
				pos[move[1]] = move[3]

				newBoardState = BoardState(pos)

				newScore = get_board_score(initColor, newBoardState)

				if newScore < theScore:
					theScore = newScore
					moveList.clear()
					moveList.append(move)

				elif newScore == theScore:
					moveList.append(move)

		else: # player move, return max score
			for move in moves:
				pos = {}
				for file in files:
					for rank in ranks:
						pos[file+rank] = currBoardState.piece_at(file, rank)

				pos[move[0]] = BoardPiece.EmptySquare
		
				pos[move[1]] = move[3]

				newBoardState = BoardState(pos)

				newScore = get_board_score(initColor, newBoardState)

				if newScore > theScore:
					theScore = newScore
					moveList.clear()
					moveList.append(move)

				elif newScore == theScore:
					moveList.append(move)

		# print(len(moveList))
		return random.choice(moveList)

	for move in moves:
		pos = {}
		for file in files:
			for rank in ranks:
				pos[file+rank] = currBoardState.piece_at(file, rank)

		pos[move[0]] = BoardPiece.EmptySquare
		pos[move[1]] = move[3]

		newBoardState = BoardState(pos)

		possMove = getOptimalMove(otherPlayer, initColor, newBoardState, depth+1, finalDepth)

		pos[possMove[0]] = BoardPiece.EmptySquare
		pos[possMove[1]] = possMove[3]

		score = get_board_score(initColor, BoardState(pos))

		if color != initColor:
			if score < theScore: # minimize the score
				moveList.clear()
				moveList.append(move)
				theScore = score
			
			elif score == theScore:
				moveList.append(move)

		else:
			if score > theScore: # maximize the score
				moveList.clear()
				moveList.append(move)
				theScore = score
			
			elif score == theScore:
				moveList.append(move)

	return random.choice(moveList)

def nextChar(char: chr, inc: int):
	return chr(ord(char)+inc)

class Pawns:
	def __init__(self, color: int, possibleList: list, pawnList: list, enemyPosDict: dict):
		self.color = color
		self.pawnList = pawnList
		self.enemyPosDict = enemyPosDict
		self.possibleList = possibleList

	def getNormalMoves(self) -> list:
		# return a list of possible moves in the format (start, end, points, piece)
		moves = []

		for pawn in self.pawnList:
			if self.color == 0:
				if pawn[0] + nextChar(pawn[1], 1) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], 1), 0])

				if pawn[1] == '2' and pawn[0] + nextChar(pawn[1], 1) in self.possibleList and pawn[0] + nextChar(pawn[1], 2) in self.possibleList:
					moves.append([pawn, pawn[0] + nextChar(pawn[1], 2), 0])

			else:
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
				if elem[1][1] == '8':
					elem.append(BoardPiece.WhiteQueen)
				else:
					elem.append(BoardPiece.WhitePawn)

		else:
			for elem in moves:
				if elem[1][1] == '1':
					elem.append(BoardPiece.BlackQueen)
				else:
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

		# print(self.color, len(moves))
		return moves

class Bishops:
	def __init__(self, color: int, possibleList: list, bishopList: list, enemyPosDict: dict):
		self.color = color
		self.bishopList = bishopList
		self.enemyPosDict = enemyPosDict
		self.possibleList = possibleList

	def getAllMoves(self) -> list:
		# return a list of possible moves in the format (start, end, points)
		moves = []

		for bishop in self.bishopList:
			# normal and attacking moves
			for i in range(1, 9): # top right
				if nextChar(bishop[0], i) + nextChar(bishop[1], i) in self.enemyPosDict:
					moves.append([bishop, nextChar(bishop[0], i) + nextChar(bishop[1], i), self.enemyPosDict[nextChar(bishop[0], i) + nextChar(bishop[1], i)]])
					break
				
				elif nextChar(bishop[0], i) + nextChar(bishop[1], i) in self.possibleList:
					moves.append([bishop, nextChar(bishop[0], i) + nextChar(bishop[1], i), 0])

				else:
					break

			for i in range(1, 9): # top left
				if nextChar(bishop[0], -i) + nextChar(bishop[1], i) in self.enemyPosDict:
					moves.append([bishop, nextChar(bishop[0], -i) + nextChar(bishop[1], i), self.enemyPosDict[nextChar(bishop[0], -i) + nextChar(bishop[1], i)]])
					break
				
				elif nextChar(bishop[0], -i) + nextChar(bishop[1], i) in self.possibleList:
					moves.append([bishop, nextChar(bishop[0], -i) + nextChar(bishop[1], i), 0])

				else:
					break

			for i in range(1, 9): # bottom right
				if nextChar(bishop[0], i) + nextChar(bishop[1], -i) in self.enemyPosDict:
					moves.append([bishop, nextChar(bishop[0], i) + nextChar(bishop[1], -i), self.enemyPosDict[nextChar(bishop[0], i) + nextChar(bishop[1], -i)]])
					break
				
				elif nextChar(bishop[0], i) + nextChar(bishop[1], -i) in self.possibleList:
					moves.append([bishop, nextChar(bishop[0], i) + nextChar(bishop[1], -i), 0])

				else:
					break

			for i in range(1, 9): # bottom left
				if nextChar(bishop[0], -i) + nextChar(bishop[1], -i) in self.enemyPosDict:
					moves.append([bishop, nextChar(bishop[0], -i) + nextChar(bishop[1], -i), self.enemyPosDict[nextChar(bishop[0], -i) + nextChar(bishop[1], -i)]])
					break
				
				elif nextChar(bishop[0], -i) + nextChar(bishop[1], -i) in self.possibleList:
					moves.append([bishop, nextChar(bishop[0], -i) + nextChar(bishop[1], -i), 0])

				else:
					break

		return moves

	def getMoves(self) -> list:
		# return a list of 4 elements, the start pos, end pos, points and the piece
		moves = []
		moves.extend(self.getAllMoves())
		moves = [elem for elem in moves if elem != []]
		
		if self.color == 0:
			for elem in moves:
				elem.append(BoardPiece.WhiteBishop)

		else:
			for elem in moves:
				elem.append(BoardPiece.BlackBishop)

		# print(self.color, len(moves))
		return moves