from ContestUtils import PlayerColour
from ContestUtils import BoardState, BoardPiece
from EngineAPI import Engine
import time

class PlayGame:
    def init_board(self):
      posMap = {}
      files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
      ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

      posMap['a1'] = BoardPiece.WhiteRook
      posMap['b1'] = BoardPiece.WhiteKnight
      posMap['c1'] = BoardPiece.WhiteBishop
      posMap['d1'] = BoardPiece.WhiteQueen
      posMap['e1'] = BoardPiece.WhiteKing
      posMap['f1'] = BoardPiece.WhiteBishop
      posMap['g1'] = BoardPiece.WhiteKnight
      posMap['h1'] = BoardPiece.WhiteRook

      posMap['a8'] = BoardPiece.BlackRook
      posMap['b8'] = BoardPiece.BlackKnight
      posMap['c8'] = BoardPiece.BlackBishop
      posMap['d8'] = BoardPiece.BlackQueen
      posMap['e8'] = BoardPiece.BlackKing
      posMap['f8'] = BoardPiece.BlackBishop
      posMap['g8'] = BoardPiece.BlackKnight
      posMap['h8'] = BoardPiece.BlackRook

      for file in files:
        posMap[file+'2'] = BoardPiece.WhitePawn
        posMap[file+'7'] = BoardPiece.BlackPawn

      return posMap

    def __init__(self):
      self.finalMoves = []
      player1 = Engine(PlayerColour.White, 5.0) # white
      player2 = Engine(PlayerColour.Black, 5.0) # black
      boardState = BoardState(self.init_board())

      for i in range(0, 10):
        startTime = time.time()

        if i%2 == 0:
          boardState, move, extra = player1.get_move(boardState)

          if extra != None:
            print(extra)

          if move == None:
            print("black wins!")
            break

          # if extra == -float('inf'):
          #   print(i, "black wins!")
          #   break
          # if extra == float('inf'):
          #   print(i, "black wins!")
          #   break
          
          self.finalMoves.append(move)
        else:
          boardState, move, extra = player2.get_move(boardState)

          if extra != None:
            print(extra)

          if move == None:
            print("white wins!")
            break

          # if extra == -float('inf'):
          #   print(i, "black wins!")
          #   break
          # if extra == float('inf'):
          #   print(i, "black wins!")
          #   break 
          
          self.finalMoves.append(move)

        endTime = time.time()

        print("Time taken for this move:", endTime-startTime)

      else:
        print("draw!")
