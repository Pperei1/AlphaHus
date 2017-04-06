import csv
import numpy as np
import ANN
import random
import cPickle as pickle
import math

def accuraccy(model,validX,validY,numberOfEx):
		acc = 0.0
		for i in range(0,numberOfEx):
			count = 0
			output = model.getOutput(validX[i])
			best = model.findMax(output)
			while(count < 3):
				if best == validY[i]:
					acc = acc + 1.0
					count = 3
				output[best] = 0
				count = count+1
		return acc/numberOfEx


with open('./valueData.csv', 'rb') as f:
	reader = csv.reader(f)
	data = list(reader)
	
X = np.array(data)

with open('./valuePred.csv', 'rb') as f:
	reader = csv.reader(f)
	data = list(reader)
	
Y = np.array(data)

trainX = X[0:40000]
trainY = Y[0:40000]
validX = X[40001:50000]
validY = Y[40001:50000]
print "finished loading"
trainX = trainX.astype(float)
trainY = trainY.astype(float)
trainY = trainY.astype(int)
validX = trainX.astype(float)
validY = trainY.astype(float)
validY = trainY.astype(int)
numberOfFeatures = 64
numberOfClasses = 1

numberOfExamples = len(trainX)
print "starting training"
loading = False
if loading == False:
	model = ANN.neuralNetwork([numberOfFeatures,numberOfFeatures/2,numberOfFeatures/4,numberOfClasses])
else:
	print "---- loading model ----"
	with open('value2.pkl', 'rb') as input:
		model = pickle.load(input)
	
  	
alpha = 0.003
momentum = 0.50
epochs = 0
acc = 0
diff = 0.005
bestscore = 0.5
print accuraccy(model,validX,validY,len(validX))

while(epochs<200):
	print "----- training ----"
	for i in range(0,128):
		r = random.randint(0,39999)
		model.trainNetwork(trainX[r],trainY[r],alpha,momentum)
	if epochs%3 == 0:
		print "----- testing ----"
		newAcc = model.accuraccy(validX,validY,validX.size/validX[0].size)
		print "at epoch "+str(epochs)+": "+str(newAcc)
		if newAcc - acc < 0.001:
			alpha = alpha/2
		acc = newAcc
		if acc > bestscore:
			with open('value2.pkl', 'wb') as output:
				pickle.dump(model, output, -1)
				bestscore = acc
	epochs = epochs + 1

