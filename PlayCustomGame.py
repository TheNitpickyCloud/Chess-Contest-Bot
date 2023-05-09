from ContestUtils import PlayerColour
from ContestUtils import BoardState, BoardPiece
from EngineAPI import Engine
import time

files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

class PlayGame:
    def from_fen(self, fen):
      PieceCharName = {
          'P': BoardPiece.WhitePawn,
          'N': BoardPiece.WhiteKnight,
          'B': BoardPiece.WhiteBishop,
          'R': BoardPiece.WhiteRook,
          'Q': BoardPiece.WhiteQueen,
          'K': BoardPiece.WhiteKing,
          'p': BoardPiece.BlackPawn,
          'n': BoardPiece.BlackKnight,
          'b': BoardPiece.BlackBishop,
          'r': BoardPiece.BlackRook,
          'q': BoardPiece.BlackQueen,
          'k': BoardPiece.BlackKing,
      }

      board = fen.split(" ")[0]
      board_ranks = board.split("/")
      result = {}

      for rank_index, rank in enumerate(board_ranks):
          file_index = 0
          for char in rank:
              if char.isdigit():
                  file_index += int(char)
              else:
                  result[files[file_index] + ranks[7 - rank_index]] = PieceCharName[char]
                  file_index += 1

      return BoardState(result)
    
    def getInput(self):
      fen_string = input("The input fen string: ")
      curr_player = int(input("The current player to simulate (0 for white, 1 for black): "))

      return fen_string, curr_player

    def __init__(self):
      
      fen_string, curr_player = self.getInput() 

      player1 = Engine(PlayerColour.White, 5.0) # white
      player2 = Engine(PlayerColour.Black, 5.0) # black
      boardState = self.from_fen(fen_string)

      startTime = time.time()

      if curr_player == 0:
        boardState, move, extra = player1.get_move(boardState)

        if move == None:
          print("black wins!")
        
        print(move[0], move[1])
        if extra != None:
          print(extra)
        
      else:
        boardState, move, extra = player2.get_move(boardState)

        if move == None:
          print("white wins!")
        
        print(move[0], move[1])
        if extra != None:
          print(extra)

      endTime = time.time()

      print("Time taken for this move:", endTime-startTime)

playGame = PlayGame()
