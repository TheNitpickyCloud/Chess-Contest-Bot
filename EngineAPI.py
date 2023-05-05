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
	BoardPiece.BlackPawn: 10,
	BoardPiece.BlackKnight: 30,
	BoardPiece.BlackBishop: 30,
	BoardPiece.BlackRook: 50,
	BoardPiece.BlackQueen: 270,
	BoardPiece.BlackKing: 0,
	BoardPiece.WhitePawn: 10,
	BoardPiece.WhiteKnight: 30,
	BoardPiece.WhiteBishop: 30,
	BoardPiece.WhiteRook: 50,
	BoardPiece.WhiteQueen: 270,
	BoardPiece.WhiteKing: 0
}

class Engine:
	def __init__(self, colour, time_per_move: float):
		if colour == PlayerColour.White:
			self.color = 0
		else:
			self.color = 1

		self.time_per_move = time_per_move
	
	def get_move(self, board_state: BoardState):
		pos = {}

		# get old map
		for file in files:
			for rank in ranks:
				pos[file+rank] = board_state.piece_at(file, rank)

		optimalMove, score, extra = getOptimalMove(self.color, self.color, board_state, 1, 2, -float('inf'), float('inf'))
		# optimalMove = random.choice(pawnMoves)

		if optimalMove == None:
			return None, None, None

		pos[optimalMove[0]] = BoardPiece.EmptySquare
		
		pos[optimalMove[1]] = optimalMove[3]

		newBoardState = BoardState(pos)

		return newBoardState, optimalMove, extra

def get_all_moves(color: int, board_state: BoardState) -> list:
	pos = {}
	possibleList = []
	enemyPosDict = {} # enemy pos, points
	pawnList = []
	knightList = []
	bishopList = []
	rookList = []
	queenList = []
	kingList = []

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

					elif str(pos[file+rank]).find('Rook') != -1: # white rook
						rookList.append(file+rank)

					elif str(pos[file+rank]).find('Queen') != -1: # white queen
						queenList.append(file+rank)

					elif str(pos[file+rank]).find('King') != -1: # white king
						kingList.append(file+rank)

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

					elif str(pos[file+rank]).find('Rook') != -1: # black rook
						rookList.append(file+rank)

					elif str(pos[file+rank]).find('Queen') != -1: # black queen
						queenList.append(file+rank)

					elif str(pos[file+rank]).find('King') != -1: # black king
						kingList.append(file+rank)

	pawns = Pawns(color, possibleList, pawnList, enemyPosDict)
	knights = Knights(color, possibleList, knightList, enemyPosDict)
	bishops = Bishops(color, possibleList, bishopList, enemyPosDict)
	rooks = Rooks(color, possibleList, rookList, enemyPosDict)
	queens = Queens(color, possibleList, queenList, enemyPosDict)
	kings = Kings(color, possibleList, kingList, enemyPosDict)

	pawnMoves = pawns.getMoves()
	knightMoves = knights.getMoves()
	bishopMoves = bishops.getMoves()
	rookMoves = rooks.getMoves()
	queenMoves = queens.getMoves()
	kingMoves = kings.getMoves()

	all_moves = []
	all_moves.extend(pawnMoves)
	all_moves.extend(knightMoves)
	all_moves.extend(bishopMoves)
	all_moves.extend(rookMoves)
	all_moves.extend(queenMoves)
	all_moves.extend(kingMoves)

	return all_moves

def get_legal_moves(color: int,  board_state: BoardState) -> list:
	moves = get_all_moves(color, board_state)
	newMoves = []
	
	for move in moves:
		pos = {}
		kingLoc = None
		done = True

		for file in files:
			for rank in ranks:
				pos[file+rank] = board_state.piece_at(file, rank)

		# make move
		pos[move[0]] = BoardPiece.EmptySquare
		pos[move[1]] = move[3]

		# get king position

		for file in files:
			for rank in ranks:
				if color == 0:
					if str(pos[file+rank]).find('WhiteKing') != -1: # white king
						kingLoc = file+rank
						break

				else:
					if str(pos[file+rank]).find('BlackKing') != -1: # black king
						kingLoc = file+rank
						break

		# new board state after making move
		newBoardState = BoardState(pos)

		opp_moves = get_all_moves(not color, newBoardState)

		for opp_move in opp_moves:
			if opp_move[1] == kingLoc:
				# illegal move
				done = False
				break

		if done:
			newMoves.append(move)

	return newMoves

def get_board_score(color: int, board_state: BoardState):
	blackScore = 0
	whiteScore = 0

	for file in files:
		for rank in ranks:
			piece = board_state.piece_at(file, rank)

			if str(piece).find('Empty') == -1: # not empty square
				if str(piece).find('Black') == -1: # white square
					whiteScore += pointsDict[piece]

				else: # black square
					blackScore += pointsDict[piece]

	if color == 0:
		return whiteScore - blackScore
	else:
		return blackScore - whiteScore

def isCheckmate(color: int, board_state: BoardState, movesLength: int):
	# get if current color to move is under check
	kingLoc = None

	# get map
	for file in files:
		for rank in ranks:
			piece = board_state.piece_at(file, rank)

			if color == 0:
				if str(piece).find('WhiteKing') != -1: # white king
					kingLoc = file+rank

			else:
				if str(piece).find('BlackKing') != -1: # black king
					kingLoc = file+rank

	opp_moves = get_legal_moves(not color, board_state)

	attacked = False

	for move in opp_moves:
		if move[1] == kingLoc:
			attacked = True
			break

	if attacked == True and movesLength == 0:
		return True
	
	return False

def getOptimalMove(color: int, initColor: int, currBoardState: BoardState, depth: int, finalDepth: int, alpha, beta):
	# simulate optimal play for x depth, then choose best move

	# get moves
	moves = get_legal_moves(color, currBoardState)

	# sort moves
	if color != initColor:
		moves.sort(key=lambda x: x[2], reverse=True)
	else:
		moves.sort(key=lambda x: x[2], reverse=False)

	# base case
	if isCheckmate(color, currBoardState, len(moves)):
		if color != initColor:
			return None, -float('inf'), None
		else:
			return None, float('inf'), None

	if depth > finalDepth:
		return None, get_board_score(initColor, currBoardState), None

	theScore = None
	newAlpha = alpha
	newBeta = beta
	moveList = []

	if color != initColor:
		theScore = float('inf')
	else:
		theScore = -float('inf')

	for move in moves:
		pos = {}
		for file in files:
			for rank in ranks:
				pos[file+rank] = currBoardState.piece_at(file, rank)

		# make move
		pos[move[0]] = BoardPiece.EmptySquare
		pos[move[1]] = move[3]

		# new board state after making move
		newBoardState = BoardState(pos)

		# get score of optimal move
		aMove, score, extra = getOptimalMove(not color, initColor, newBoardState, depth+1, finalDepth, newAlpha, newBeta)

		if color != initColor:
			if score < theScore: # minimize the score
				moveList.clear()
				moveList.append(move)
				theScore = score
			
			elif score == theScore:
				moveList.append(move)

			newBeta = min(newBeta, theScore)
			if newBeta <= newAlpha:
				break

		else:
			if score > theScore: # maximize the score
				moveList.clear()
				moveList.append(move)
				theScore = score
			
			elif score == theScore:
				moveList.append(move)

			newAlpha = max(newAlpha, theScore)
			if newBeta <= newAlpha:
				break

	if len(moveList) > 0:
			# move = random.choice(moveList)
			# if move[3] == BoardPiece.BlackKing or move[3] == BoardPiece.WhiteKing:
			# 	return move, theScore, move[1]

			return random.choice(moveList), theScore, None
			# return move, theScore, None
			# return moveList[0], theScore, None
			# return random.choice(moveList), theScore

	else:
		return None, theScore, None

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

class Rooks:
	def __init__(self, color: int, possibleList: list, rookList: list, enemyPosDict: dict):
		self.color = color
		self.rookList = rookList
		self.enemyPosDict = enemyPosDict
		self.possibleList = possibleList

	def getAllMoves(self) -> list:
		# return a list of possible moves in the format (start, end, points)
		moves = []

		for rook in self.rookList:
			# normal and attacking moves
			for i in range(1, 9): # top
				if rook[0] + nextChar(rook[1], i) in self.enemyPosDict:
					moves.append([rook, rook[0] + nextChar(rook[1], i), self.enemyPosDict[rook[0] + nextChar(rook[1], i)]])
					break
				
				elif rook[0] + nextChar(rook[1], i) in self.possibleList:
					moves.append([rook, rook[0] + nextChar(rook[1], i), 0])

				else:
					break

			for i in range(1, 9): # bottom
				if rook[0] + nextChar(rook[1], -i) in self.enemyPosDict:
					moves.append([rook, rook[0] + nextChar(rook[1], -i), self.enemyPosDict[rook[0] + nextChar(rook[1], -i)]])
					break
				
				elif rook[0] + nextChar(rook[1], -i) in self.possibleList:
					moves.append([rook, rook[0] + nextChar(rook[1], -i), 0])

				else:
					break

			for i in range(1, 9): # right
				if nextChar(rook[0], i) + rook[1] in self.enemyPosDict:
					moves.append([rook, nextChar(rook[0], i) + rook[1], self.enemyPosDict[nextChar(rook[0], i) + rook[1]]])
					break
				
				elif nextChar(rook[0], i) + rook[1] in self.possibleList:
					moves.append([rook, nextChar(rook[0], i) + rook[1], 0])

				else:
					break

			for i in range(1, 9): # left
				if nextChar(rook[0], -i) + rook[1] in self.enemyPosDict:
					moves.append([rook, nextChar(rook[0], -i) + rook[1], self.enemyPosDict[nextChar(rook[0], -i) + rook[1]]])
					break
				
				elif nextChar(rook[0], -i) + rook[1] in self.possibleList:
					moves.append([rook, nextChar(rook[0], -i) + rook[1], 0])

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
				elem.append(BoardPiece.WhiteRook)

		else:
			for elem in moves:
				elem.append(BoardPiece.BlackRook)

		# print(self.color, len(moves))
		return moves

class Queens:
	def __init__(self, color: int, possibleList: list, queenList: list, enemyPosDict: dict):
		self.color = color
		self.queenList = queenList
		self.enemyPosDict = enemyPosDict
		self.possibleList = possibleList

	def getAllMoves(self) -> list:
		# return a list of possible moves in the format (start, end, points)
		moves = []

		for queen in self.queenList:
			# normal and attacking moves
			for i in range(1, 9): # top
				if queen[0] + nextChar(queen[1], i) in self.enemyPosDict:
					moves.append([queen, queen[0] + nextChar(queen[1], i), self.enemyPosDict[queen[0] + nextChar(queen[1], i)]])
					break
				
				elif queen[0] + nextChar(queen[1], i) in self.possibleList:
					moves.append([queen, queen[0] + nextChar(queen[1], i), 0])

				else:
					break

			for i in range(1, 9): # bottom
				if queen[0] + nextChar(queen[1], -i) in self.enemyPosDict:
					moves.append([queen, queen[0] + nextChar(queen[1], -i), self.enemyPosDict[queen[0] + nextChar(queen[1], -i)]])
					break
				
				elif queen[0] + nextChar(queen[1], -i) in self.possibleList:
					moves.append([queen, queen[0] + nextChar(queen[1], -i), 0])

				else:
					break

			for i in range(1, 9): # right
				if nextChar(queen[0], i) + queen[1] in self.enemyPosDict:
					moves.append([queen, nextChar(queen[0], i) + queen[1], self.enemyPosDict[nextChar(queen[0], i) + queen[1]]])
					break
				
				elif nextChar(queen[0], i) + queen[1] in self.possibleList:
					moves.append([queen, nextChar(queen[0], i) + queen[1], 0])

				else:
					break

			for i in range(1, 9): # left
				if nextChar(queen[0], -i) + queen[1] in self.enemyPosDict:
					moves.append([queen, nextChar(queen[0], -i) + queen[1], self.enemyPosDict[nextChar(queen[0], -i) + queen[1]]])
					break
				
				elif nextChar(queen[0], -i) + queen[1] in self.possibleList:
					moves.append([queen, nextChar(queen[0], -i) + queen[1], 0])

				else:
					break

			# normal and attacking moves
			for i in range(1, 9): # top right
				if nextChar(queen[0], i) + nextChar(queen[1], i) in self.enemyPosDict:
					moves.append([queen, nextChar(queen[0], i) + nextChar(queen[1], i), self.enemyPosDict[nextChar(queen[0], i) + nextChar(queen[1], i)]])
					break
				
				elif nextChar(queen[0], i) + nextChar(queen[1], i) in self.possibleList:
					moves.append([queen, nextChar(queen[0], i) + nextChar(queen[1], i), 0])

				else:
					break

			for i in range(1, 9): # top left
				if nextChar(queen[0], -i) + nextChar(queen[1], i) in self.enemyPosDict:
					moves.append([queen, nextChar(queen[0], -i) + nextChar(queen[1], i), self.enemyPosDict[nextChar(queen[0], -i) + nextChar(queen[1], i)]])
					break
				
				elif nextChar(queen[0], -i) + nextChar(queen[1], i) in self.possibleList:
					moves.append([queen, nextChar(queen[0], -i) + nextChar(queen[1], i), 0])

				else:
					break

			for i in range(1, 9): # bottom right
				if nextChar(queen[0], i) + nextChar(queen[1], -i) in self.enemyPosDict:
					moves.append([queen, nextChar(queen[0], i) + nextChar(queen[1], -i), self.enemyPosDict[nextChar(queen[0], i) + nextChar(queen[1], -i)]])
					break
				
				elif nextChar(queen[0], i) + nextChar(queen[1], -i) in self.possibleList:
					moves.append([queen, nextChar(queen[0], i) + nextChar(queen[1], -i), 0])

				else:
					break

			for i in range(1, 9): # bottom left
				if nextChar(queen[0], -i) + nextChar(queen[1], -i) in self.enemyPosDict:
					moves.append([queen, nextChar(queen[0], -i) + nextChar(queen[1], -i), self.enemyPosDict[nextChar(queen[0], -i) + nextChar(queen[1], -i)]])
					break
				
				elif nextChar(queen[0], -i) + nextChar(queen[1], -i) in self.possibleList:
					moves.append([queen, nextChar(queen[0], -i) + nextChar(queen[1], -i), 0])

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
				elem.append(BoardPiece.WhiteQueen)

		else:
			for elem in moves:
				elem.append(BoardPiece.BlackQueen)

		# print(self.color, len(moves))
		return moves

class Kings:
	def __init__(self, color: int, possibleList: list, kingsList: list, enemyPosDict: dict):
		self.color = color
		self.kingsList = kingsList
		self.enemyPosDict = enemyPosDict
		self.possibleList = possibleList

	def getAllMoves(self) -> list:
		# return a list of possible moves in the format (start, end, points)
		moves = []

		for kings in self.kingsList:
			# normal and attacking moves
			for i in range(1, 2): # top
				if kings[0] + nextChar(kings[1], i) in self.enemyPosDict:
					moves.append([kings, kings[0] + nextChar(kings[1], i), self.enemyPosDict[kings[0] + nextChar(kings[1], i)]])
					break
				
				elif kings[0] + nextChar(kings[1], i) in self.possibleList:
					moves.append([kings, kings[0] + nextChar(kings[1], i), -1])

				else:
					break

			for i in range(1, 2): # bottom
				if kings[0] + nextChar(kings[1], -i) in self.enemyPosDict:
					moves.append([kings, kings[0] + nextChar(kings[1], -i), self.enemyPosDict[kings[0] + nextChar(kings[1], -i)]])
					break
				
				elif kings[0] + nextChar(kings[1], -i) in self.possibleList:
					moves.append([kings, kings[0] + nextChar(kings[1], -i), -1])

				else:
					break

			for i in range(1, 2): # right
				if nextChar(kings[0], i) + kings[1] in self.enemyPosDict:
					moves.append([kings, nextChar(kings[0], i) + kings[1], self.enemyPosDict[nextChar(kings[0], i) + kings[1]]])
					break
				
				elif nextChar(kings[0], i) + kings[1] in self.possibleList:
					moves.append([kings, nextChar(kings[0], i) + kings[1], -1])

				else:
					break

			for i in range(1, 2): # left
				if nextChar(kings[0], -i) + kings[1] in self.enemyPosDict:
					moves.append([kings, nextChar(kings[0], -i) + kings[1], self.enemyPosDict[nextChar(kings[0], -i) + kings[1]]])
					break
				
				elif nextChar(kings[0], -i) + kings[1] in self.possibleList:
					moves.append([kings, nextChar(kings[0], -i) + kings[1], -1])

				else:
					break

			# normal and attacking moves
			for i in range(1, 2): # top right
				if nextChar(kings[0], i) + nextChar(kings[1], i) in self.enemyPosDict:
					moves.append([kings, nextChar(kings[0], i) + nextChar(kings[1], i), self.enemyPosDict[nextChar(kings[0], i) + nextChar(kings[1], i)]])
					break
				
				elif nextChar(kings[0], i) + nextChar(kings[1], i) in self.possibleList:
					moves.append([kings, nextChar(kings[0], i) + nextChar(kings[1], i), -1])

				else:
					break

			for i in range(1, 2): # top left
				if nextChar(kings[0], -i) + nextChar(kings[1], i) in self.enemyPosDict:
					moves.append([kings, nextChar(kings[0], -i) + nextChar(kings[1], i), self.enemyPosDict[nextChar(kings[0], -i) + nextChar(kings[1], i)]])
					break
				
				elif nextChar(kings[0], -i) + nextChar(kings[1], i) in self.possibleList:
					moves.append([kings, nextChar(kings[0], -i) + nextChar(kings[1], i), -1])

				else:
					break

			for i in range(1, 2): # bottom right
				if nextChar(kings[0], i) + nextChar(kings[1], -i) in self.enemyPosDict:
					moves.append([kings, nextChar(kings[0], i) + nextChar(kings[1], -i), self.enemyPosDict[nextChar(kings[0], i) + nextChar(kings[1], -i)]])
					break
				
				elif nextChar(kings[0], i) + nextChar(kings[1], -i) in self.possibleList:
					moves.append([kings, nextChar(kings[0], i) + nextChar(kings[1], -i), -1])

				else:
					break

			for i in range(1, 2): # bottom left
				if nextChar(kings[0], -i) + nextChar(kings[1], -i) in self.enemyPosDict:
					moves.append([kings, nextChar(kings[0], -i) + nextChar(kings[1], -i), self.enemyPosDict[nextChar(kings[0], -i) + nextChar(kings[1], -i)]])
					break
				
				elif nextChar(kings[0], -i) + nextChar(kings[1], -i) in self.possibleList:
					moves.append([kings, nextChar(kings[0], -i) + nextChar(kings[1], -i), -1])

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
				elem.append(BoardPiece.WhiteKing)

		else:
			for elem in moves:
				elem.append(BoardPiece.BlackKing)

		# print(self.color, len(moves))
		return moves
