#!/usr/bin/python3.8


# Imports:
import tensorflow as tf
from tensorflow import keras

from keras.models import Sequential
from keras.layers import Dense

import numpy as np
from numpy import loadtxt
from numpy import savetxt

import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import math


###########################################################################################################
###########################################################################################################
## The Straw Hats: The Seer - EE493 Senior Design                                                      ####
## Neural Network - 3 Antenna Array, Power Only - Model Analysis Tool                                  ####
## Author: Tate Harsch-Hudspeth                                                                        ####
## Last Edit Made: 04/14/2021                                                                          ####
## University: Sonoma State University, Department of Engineering Science                              #### 
###########################################################################################################
###########################################################################################################

# Use this code to anlyze the effectiveness of the Keras model, once a model has reached
# an acceptable level of accuracy, use "Neural_Net_3P.py" to save the model architecture
# and to prepare the model for predictions.
# This model attempts to solve our multi-output regression problem:
# Inputs: [Pr1,Pr2,Pr3]
# Outputs: [x,y] or [r,theta]


##### Process the Data #####

# Load Dataset:
dataset = loadtxt('data_rtheta.csv', delimiter=',')
#print (dataset)

X = dataset[:,0:3]
y = dataset[:,3:]
size=len(X)

#print (X)
#print (y)

# Test Split:
# Split the data into input (X) training and testing data, and output (y) training and testing data.
# Training data being 95% of the data (if split=0.05), and testing data being the remaining 5% of the data.
split=0.05
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split)

# Normalize the Data:
X_train = preprocessing.scale(X_train)
no_scale_inputs = X_test
X_test = preprocessing.scale(X_test)


##### The Straw Hats Model #####

# Define the Keras model:
model = Sequential()
model.add(Dense(32, input_dim=3, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(2, activation='linear'))
# Compile the Keras model.
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Fit the Keras Model:
model.fit(X_train, y_train, epochs=500, batch_size=32)
_, accuracy = model.evaluate(X_train, y_train)
print ('Accuracy: %.2f' % (accuracy*100))


##### The Straw Hats Prediction Methods #####

# Uncomment the following code, commenting out the above fit, in order to plot the learning rate:
# Use with test split.
#history = model.fit(X_train, y_train, validation_data=(X_test,y_test), epochs=1150, batch_size=32)
#plt.plot(history.history['loss'], label='MSE (training data)')
#plt.plot(history.history['val_loss'], label='MSE (validation data)')
#plt.title('MSE for Straw Hat Keras Model: JTC Simulation')
#plt.ylabel('Loss')
#plt.xlabel('N. epoch')
#plt.legend(loc="upper left")
#plt.show()


# Tells model to predict the outputs of X_test:
y_new = model.predict(X_test)

# For (x,y):
#x_sum = 0
#y_sum = 0
#x_diff = []
#y_diff = []
#std_x_sum = 0
#std_y_sum = 0

# For (r,theta):
r_sum = 0
theta_sum = 0
r_diff = []
theta_diff = []
std_r_sum = 0
std_theta_sum = 0


# Display the inputs and predicted outputs:
for i in range(len(X_test)):
	print ("X=%s, Predicted=%s" % (no_scale_inputs[i], y_new[i]))
	print ("Y_test =", y_test[i])
	
	# Find the average difference between the correct and the predicted values for (x,y) or (r,theta):
	
	# For (x,y):
#	x_difference = y_test[i][0] - y_new[i][0]
#	if (x_difference < 0):
#		x_difference = -1 * x_difference
#	x_sum = x_sum + x_difference
#	x_diff.append(x_difference)
#	y_difference = y_test[i][1] - y_new[i][1]
#	if (y_difference < 0):
#		y_difference = -1 * y_difference
#	y_sum = y_sum + y_difference
#	y_diff.append(y_difference)
#x_avg = x_sum / (split * size)
#y_avg = y_sum / (split * size)

	# For (r,theta):
	r_difference = y_test[i][0] - y_new[i][0]
	if (r_difference < 0):
		r_difference = -1 * r_difference
	r_sum = r_sum + r_difference
	r_diff.append(r_difference)
	theta_difference = y_test[i][1] - y_new[i][1]
	if (theta_difference < 0):
		theta_difference = -1 * theta_difference
	theta_sum = theta_sum + theta_difference
	theta_diff.append(theta_difference)
r_avg = r_sum / (split * size)
theta_avg = theta_sum / (split * size)

# Find the standard deviation of the difference between the correct and the predicted values:

# For (x,y):
#for i in range(len(y_new)):
#	pre_std_x = (x_diff[i] - x_avg)**2
#	std_x_sum = std_x_sum + pre_std_x
#	pre_std_y = (y_diff[i] - y_avg)**2
#	std_y_sum = std_y_sum + pre_std_y
#std_x = math.sqrt(std_x_sum / (split * size))
#std_y = math.sqrt(std_y_sum / (split * size))
#print ("Average Difference (x) = ",x_avg)
#print ("Average Difference (y) = ",y_avg)
#print ("SD (x) = ",std_x)
#print ("SD (y) = ",std_y)

# For (r,theta):
for i in range(len(y_new)):
	pre_std_r = (r_diff[i] - r_avg)**2
	std_r_sum = std_r_sum + pre_std_r
	pre_std_theta = (theta_diff[i] - theta_avg)**2
	std_theta_sum = std_theta_sum + pre_std_theta
std_r = math.sqrt(std_r_sum / (split * size))
std_theta = math.sqrt(std_theta_sum / (split * size))
print ("Average Difference (r) = ",r_avg)
print ("Average Difference (theta) = ",theta_avg)
print ("SD (r) = ",std_r)
print ("SD (theta) = ",std_theta)


# Save y_new, y_test, and X_test as CSV files for more in-depth analysis in Excel:
#savetxt('y_pred_3Pr_Test.csv', y_new, delimiter=',')
#savetxt('y_correct_3Pr_Test.csv', y_test, delimiter=',')
#savetxt('Inputs.csv', no_scale_inputs, delimiter=',')


# End #####################################################################################################
###########################################################################################################
