import random as rand
import numpy as np
import math
#the node class for the neural network, contains Weights and a bias. The weights are randomly initialized
class node:
	def __init__(self,nInNode):
		self.w = np.zeros(nInNode)
		for i in range(0,nInNode):
			self.w[i] = -1.0+2*rand.random()
		self.update = np.zeros(nInNode)
		self.output = 0
		self.bias = -1+2*rand.random()
		self.biasupdate = 0
		self.propagation = 0
## the layer class, contains a list of nodes
class Layer:
	## calculates the output of each node in the layer once the input has been chosen
	def forward(self):
		if self.isSoft == False:
			for i in range(0,len(self.node)):
				self.node[i].output = self.sigmoid(self.node[i].bias+np.dot(self.input,self.node[i].w))
		else:
			for i in range(0,len(self.node)):
				self.node[i].output = math.exp(self.node[i].bias+np.dot(self.input,self.node[i].w))
			sum = np.sum(self.outputVector())
			for i in range(0,len(self.node)):
				self.node[i].output = self.node[i].output/sum
	## the sigmoid function
	def sigmoid(self,a):
		return 1.0/(1.0+math.exp(-a))
	## returns the output of the layer to be passed on the next layer or outputed by the network
	def outputVector(self):
		vector = np.array([])
		for i in range(0,len(self.node)):
			vector = np.append(vector,self.node[i].output)
		return vector
	## initializes the layer by giving the number of nodes and whether to used the sigmoid activation function or the softmax one
	def __init__(self,nNode,nInNode,isSoft):
		self.net = 0.0
		self.node = []
		self.isSoft = isSoft
		for i in range(0,nNode):
			self.node.append(node(nInNode))
		self.input = np.zeros(nInNode)

class neuralNetwork:
	## the neural network class
	## this method performs the forward propagation of an input through the network
	def forward(self):
		for i in range(0,len(self.layer[0].node)):
			self.layer[0].node[i].Output = self.layer[0].input[i]

		self.layer[1].input = self.layer[0].input
		for i in range(1,len(self.layer)):
			self.layer[i].forward()
			if(i != len(self.layer)-1):
				self.layer[i+1].input = self.layer[i].outputVector()
	##this method updates the weights in the network by first calculating the error signal for each node and then performing backpropagation
	def updatews(self,x,y,alpha,m):
		self.calcPropagations(x,y)
		self.backPropagation(alpha,m)
	## this method calculates the signal error at each node in the network
	def calcPropagations(self,x,y):
		for i in range(0,len(self.layer[self.numberofLayers-1].node)):
			currentNode = self.layer[self.numberofLayers-1].node[i]
			## the loss function used is cross entropy hence the signal error is y-o where y is the expected output and o the output of the node at the outpus layer
			currentNode.propagation = ((y == i) - currentNode.output)
		for i in range(2,self.numberofLayers):
			for j in range(0,len(self.layer[self.numberofLayers-i].node)):
				sum = 0
				for k in range(0,len(self.layer[self.numberofLayers-i+1].node)):
					sum = sum + self.layer[self.numberofLayers-i+1].node[k].w[j]*self.layer[self.numberofLayers-i+1].node[k].propagation
				self.layer[self.numberofLayers-i].node[j].propagation = self.layer[self.numberofLayers-i].node[j].output*(1-self.layer[self.numberofLayers-i].node[j].output)*sum
	## performs backpropagation to update the weights
	def backPropagation(self,alpha,momentum):
		for i in range(1,self.numberofLayers):
			for j in range(0,len(self.layer[self.numberofLayers-i].node)):
				currentNode = self.layer[self.numberofLayers-i].node[j]
				currentNode.biasupdate = learningRate * currentNode.propagation + momentum*currentNode.biasupdate
				currentNode.bias = currentNode.bias + currentNode.biasupdate
				currentNode.update = alpha * currentNode.propagation*self.layer[self.numberofLayers-i].input+momentum*currentNode.update
				currentNode.w = currentNode.w + currentNode.update
	#takes as input a feature matrix validX and the class vector y and outpus the percentage of examples that were correctly classified
	def accuraccy(self,validX,validY,numberOfEx):
		acc = 0.0
		for i in range(0,numberOfEx):
			output = self.getOutput(validX[i])
			best = self.findMax(output)
			if best == validY[i]:
				acc = acc + 1.0
		return acc/numberOfEx

	def findMax(self,vec):
		max = vec[0]
		best = 0
		for j in range(1,vec.size):
			if vec[j]>max:
				max = vec[j]
				best = j
		return best
	# calculates the cross entropy
	def lossFunction(self,validX,validY,numberOfEx):
		sum = 0
		for i in range(0,numberOfEx):
			self.layer[0].input = validX[i]
			self.forward()
			sum = sum + math.log(self.layer[self.numberofLayers-1].node[validY[i]].output)
		return -sum

	def __init__(self,nOfF):
		self.numberofLayers = len(nOfF)
		self.layer = [Layer(nOfF[0],nOfF[0],False)]
		for i in range(1,len(nOfF)-1):
			self.layer.append(Layer(nOfF[i],nOfF[i-1],False))
		self.layer.append(Layer(nOfF[len(nOfF)-1],nOfF[len(nOfF)-2],True))

	## takes as input a feature vector x and the expected class y and trains the network on that example
	def trainNetwork(self,x,y,alpha,m):
		self.layer[0].input = x
		self.forward()
		self.updatews(x,y,alpha,m)
	## outputs the prediction based on the feature vector x
	def getOutput(self,x):
		self.layer[0].input = x
		self.forward()
		return self.layer[self.numberofLayers-1].outputVector()
	## returns the weights of the network
	def getw(self):
		W = []
		for i in range(0,self.numberofLayers):
			for j in range(0,len(self.layer[i].node)):
				W.append(self.layer[i].node[j].w)
		return W
	## returns the bias of each node in the network
	def getbias(self):
		T = []
		for i in range(0,self.numberofLayers):
			for j in range(0,len(self.layer[i].node)):
				T.append(self.layer[i].node[j].bias)
		return T