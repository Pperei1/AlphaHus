import NN
import numpy as np
import cPickle as pickle
# a copy of the HusBoard class provided in java
class Board:
	board_width = 16
	max_turn = 5000
	max_turn_length = 200

	def __init__(self):
		self.board = np.array([np.zeros(2*self.board_width),np.zeros(2*self.board_width)])
		self.placeInitialSeeds()
		self.turn_number = 0
		self.winner = -1
		self.turn_player = 0
		self.first_player = 0

	def placeInitialSeeds(self):
		i = 0
		while(i < (3.0/2)*self.board_width):
			self.board[0][i] = 2
			self.board[1][i] = 2
			i = i+1

	def gameOver(self):
		return winner == -1

	def getLegalMoves(self):
		moves = []
		for i in range(0,2*self.board_width):
			if self.board[self.turn_player][i] > 1:
				moves.append(i)
		return moves

	def move(self,m):
		if(self.board[self.turn_player][m] > 1):
			endpit = self.runMove(m)
			if endpit == -1:
				return False
			if self.turn_player == 1:
				self.turn_number = self.turn_number + 1
			self.turn_player = (self.turn_player+1)%2
			self.updateWinner(self.turn_player)
			return True
		else:
			print "illegal move"

	def sowSeeds(self,pit,num_seeds,direction):
		while(num_seeds > 0):
			pit = self.getNextPit(pit,direction)
			self.board[self.turn_player][pit] = self.board[self.turn_player][pit]+1
			num_seeds = num_seeds -1
		return pit

	def runMove(self,start_pit):
		num_seeds_in_hand = self.board[self.turn_player][start_pit]
		self.board[self.turn_player][start_pit] = 0

		num_iterations = 0
		endturn = True
		while(endturn):
			end_pit = self.sowSeeds(start_pit, num_seeds_in_hand, 1)
			if(self.board[self.turn_player][end_pit]>1):
				if(self.canCapture(self.turn_player,end_pit)):
					num_seeds_in_hand = self.capture(self.turn_player,end_pit)
				else:
					num_seeds_in_hand = self.board[self.turn_player][end_pit]
					self.board[self.turn_player][end_pit] = 0
				start_pit = end_pit
			else:
				endturn = False
		return end_pit

	def getNextPit(self,pit,direction):
		if direction == 1:
			return (pit+1) % (self.board_width*2)
		elif direction == -1:
			return (pit-1) % (self.board_width*2)
		else:
			print "error direction"

	def canCapture(self,player_id,pit):
		if(self.turn_number <= 0):
			return False
		if((pit < self.board_width) | (pit >= 2* self.board_width)):
			return False
		opponent_player_id = (player_id+1)%2
		opponent_pit = pit - self.board_width
		test = True
		test = test & (self.board[opponent_player_id][2*self.board_width-1-opponent_pit] > 0)
		return test

	def capture(self,player_id,pit):
		opponent_player_id = (player_id+1)%2
		opponent_pit = pit - self.board_width
		captured_seeds = self.board[opponent_player_id][opponent_pit]
		captured_seeds = captured_seeds+self.board[opponent_player_id][2*self.board_width-1-opponent_pit]
		self.board[opponent_player_id][opponent_pit] = 0
		self.board[opponent_player_id][2*self.board_width-1-opponent_pit] = 0
		return captured_seeds

	def hasValidMoves(self,player_id):
		pit = 0
		for i in range(0,2*self.board_width):
			if self.board[player_id][pit] > 1:
				return True
			pit = self.getNextPit(pit,1)
		return False

	def updateWinner(self,next_to_play):
		if self.winner != -1:
			return
		if self.hasValidMoves(next_to_play) ==  False:
			self.winner = (next_to_play+1)%2
			return
	def printBoard(self):
		print np.append(self.board[0],self.board[1])

class student:
	def __init__(self,file,player_id):
		with open(file, 'rb') as input:
			self.model = pickle.load(input)
		self.player_id = player_id

	def move(self,b):
		if b.turn_player == 0:
			x = np.append(b.board[0],b.board[1])
		else:
			x = np.append(b.board[1],b.board[0])
		prob = self.model.getOutput(x)
		poss = b.getLegalMoves()
		moves = np.random.choice(np.array(range(0,32)),32,replace = False,p=prob)
		for i in range(0,32):
			for j in range(0,len(poss)):
				if moves[i] == poss[j]:
					return moves[i]

	def findMax(self,vec):
		max = vec[0]
		best = 0
		for j in range(1,vec.size):
			if vec[j]>max:
				max = vec[j]
				best = j
		return best