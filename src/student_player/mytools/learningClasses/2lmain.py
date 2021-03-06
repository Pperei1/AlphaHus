import csv
import numpy as np
import NN
import random
import cPickle as pickle
import math

with open('../../../trainData.csv', 'rb') as f:
	reader = csv.reader(f)
	data = list(reader)
	
corpus = np.array(data)
corpus = np.transpose(corpus)
trainX = corpus[0:64]
trainY = corpus[64]
trainX = np.transpose(trainX)
trainY = np.transpose(trainY)
'''
with open('../../../datatest.csv', 'rb') as f:
	reader = csv.reader(f)
	data = list(reader)
	
corpus = np.array(data)
corpus = np.transpose(corpus)
testX = corpus[0:64]
testY = corpus[64]
testX = np.transpose(testX)
testY = np.transpose(testY)
'''
print "finished loading"
trainX = trainX.astype(float)
trainY = trainY.astype(int)
numberOfFeatures = 64
numberOfClasses = 32
numberOfExamples = trainX.size/trainX[0].size
print numberOfExamples
validX = trainX[800000:900001]
validY = trainY[800000:900001]
trainX = trainX[0:700001]
trainY = trainY[0:700001]
print "starting training"
loading = True
if loading == False:
	model = NN.neuralNetwork([numberOfFeatures,numberOfFeatures,48,numberOfClasses])
else:
	print "---- loading model ----"
	with open('2l.pkl', 'rb') as input:
		model = pickle.load(input)
		
    	
alpha = 0.0002
momentum = 0.5
epochs = 0
acc = 0
diff = 0.005
while(epochs<100):
	print "----- training ----"
	for i in range(0,20000):
		r = random.randint(0,700000)
		model.trainNetwork(trainX[r],trainY[r],alpha,momentum)
	if epochs%3 == 0:
		print "----- testing ----"
		newAcc = model.accuraccy(validX,validY,validX.size/validX[0].size)
		print "at epoch "+str(epochs)+": "+str(newAcc)
	epochs = epochs + 1
	if epochs%13 == 0:
		alpha = alpha/2
		momentum = momentum+0.05
		with open('2l.pkl', 'wb') as output:
			pickle.dump(model, output, -1)

with open('2l.pkl', 'wb') as output:
    pickle.dump(model, output, -1)

'''
testX = trainX.astype(float)
testY = trainY.astype(float)

with open('coeff.csv', 'rb') as f:
	reader = csv.reader(f)
	data = list(reader)
weights = np.array(data)
weights = weights.astype(float)

with open('intercept.csv', 'rb') as f:
	reader = csv.reader(f)
	data = list(reader)
intercept = np.array(data)
intercept = intercept.astype(float)

model = node.neuralNetwork()
model.coef_= weights

np.savetxt('coeff2.csv',model.coef_,delimiter=',')
np.savetxt('intercept.csv',model.intercept_,delimiter=',')

print model.coef_[0].size
print model.score(testX,testY)
'''