import board
import numpy as np
import random
import cPickle as pickle
import ANN
## this method was used to test two players playing moves using neural networks 
def playGame(player1,player2,X,Y):
	game = board.Board()
	r = random.randint(1,60)
	while((game.winner == -1) & (game.turn_number<r)):
		if game.turn_player == 0:
			move = player1.move(game)
		else:
			move = player2.move(game)
		game.move(move)
	print game.turn_number
	if(game.winner == -1):
		moves = game.getLegalMoves()
		r = random.randint(0,len(moves)-1)
		game.move(moves[r])
	X = np.vstack((X,np.append(game.board[0],game.board[1])))
	while(game.winner == -1):
		if game.turn_player == 0:
			move = player1.move(game)
		else:
			move = player2.move(game)
		game.move(move)
	if game.winner == 0:
		Y = np.append(Y,1)
	else:
		Y = np.append(Y,0)
	return [X,Y]

# the player loaded up saved neural networks, obtained during the REINFORCE learning and recorded who won in order to train a value neural network
player1 = board.student('model138.pkl',0)
player2 = board.student('model138.pkl',1)
game = board.Board()
X = np.append(game.board[0],game.board[1])
Y = np.array([1.0])
for i in range(0,50000):
	[X,Y] = playGame(player1,player2,X,Y)
	print i


np.savetxt("valueData.csv", X, delimiter=",")
np.savetxt("valuePred.csv", Y, delimiter=",")