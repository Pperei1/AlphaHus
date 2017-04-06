import board
import numpy as np
import random
import cPickle as pickle

def playGame(player1,player2):
	game = board.Board()
	if game.turn_player == 0:
		move = player1.move(game)
		Y = np.array([move])
		X = np.append(game.board[0],game.board[1])
	else:
		move = player2.move(game)
	game.move(move)
	while(game.winner == -1):
		if game.turn_player == 0:
			move = player1.move(game)
			Y = np.append(Y,move)
			X = np.vstack((X,np.append(game.board[0],game.board[1])))
		else:
			move = player2.move(game)
		game.move(move)
	return [X,Y,game.winner]

alpha = 0.0001
epochs = 0
numberOfModels = 140
player1 = board.student('model140.pkl',0)
model = player1.model
while(epochs<30000):
	print "----playingGame----"
	r = random.randint(1,numberOfModels)
	fileload = 'model'+str(r)+'.pkl'
	player2 = board.student(fileload,1)
	ex = playGame(player1,player2)
	X = ex[0]
	Y = ex[1]
	winner = ex[2]
	print winner
	print numberOfModels
	print epochs
	if winner == 1:
		al = -alpha
	else:
		al = alpha
	print "----- training ----"
	for i in range(0,len(X)):
		model.trainNetwork(X[i],Y[i],al,0.0)
	if epochs%500 == 0:
		numberOfModels = numberOfModels + 1
		file = 'model'+str(numberOfModels)+'.pkl'
		with open(file, 'wb') as output:
			pickle.dump(model, output, -1)
	epochs = epochs + 1
