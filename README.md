# chess-contest-bot

Todo:
1. Remove looping over chessboard every time, keep track of pieces instead
2. Find optimal sorting for the moves for alpha beta pruning

Heuristics:
1. Pawn promotion reward
2. Reward for taking high level piece with low level piece, punishment for other way around
3. Check pieces which can be taken by other pieces at end of moves, punish accordingly
