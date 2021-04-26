#!/usr/bin/python3.8


# Imports:
import tensorflow as tf
from tensorflow import keras

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense

import numpy as np
from numpy import loadtxt
from numpy import savetxt

import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import math

import os


###########################################################################################################
###########################################################################################################
## The Straw Hats: The Seer - EE493 Senior Design                                                      ####
## Neural Network - 5 Antenna Array - Final Model                                                      ####
## Author: Tate Harsch-Hudspeth                                                                        ####
## Last Edit Made: 04/20/2021                                                                          ####
## University: Sonoma State University, Department of Engineering Science                              #### 
###########################################################################################################
###########################################################################################################

# Use this code to save the model architecture and prepare the model for predictions.
# Use "Neural_Net_5AA_Test.py" to dial in the best model for the target problem.
# This model attempts to solve our multi-output regression problem:
# Inputs: [Pr1,Phi_1,Pr2,Phi_2,Pr3,Phi_3,Pr4,Phi_4]
# Outputs: [x,y] or [r,theta]


# Set choice to 1 for training data, set choice to 2 for validation data:
#choice = 1
choice = 2

if (choice == 1):

	##### Process the Data #####
	
	# Load Training Dataset:
	#dataset = loadtxt('data_xy.csv', delimiter=',')
	dataset = loadtxt('data_rtheta.csv', delimiter=',')
	#print (dataset)

	X = dataset[:,0:8]
	y = dataset[:,8:]
	size=len(X)

	#print (X)
	#print (y)
	
	# Normalize the Data:
	no_scale_inputs = X
	X = preprocessing.scale(X)
	
	
	##### The Straw Hats Model #####

	# Define the Keras model:
	#model = Sequential()
	#model.add(Dense(32, input_dim=3, activation='relu'))
	#model.add(Dense(32, activation='relu'))
	#model.add(Dense(2, activation='linear'))
	# Compile the Keras model.
	#model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

	# Fit the Keras Model:
	model.fit(X, y, epochs=500, batch_size=32)
	_, accuracy = model.evaluate(X, y)
	print ('Accuracy: %.2f' % (accuracy*100))

	# Save model and architecture to single file:
	#model.save("model.h5")
	#print ("Saved model to disk.")


elif (choice == 2):

	##### Process the Data #####
	
	# Load Validation Dataset:
	validation_data = loadtxt('data_rtheta_validation.csv', delimiter=',')

	X_validate = validation_data[:,0:8]
	y_validate = validation_data[:,8:]

	#print (X_validate)
	#print (y_validate)
	
	# Normalize the Data:
	no_scale_validation_inputs = X_validate
	X_validate = preprocessing.scale(X_validate)
	
	
	##### The Straw Hats Model #####

	# Use the following block of code after you have saved your model and architecture.
	# Comment out the rest of "The Straw Hats Model".
	# Load model:
	model = load_model('model.h5')
	# Summarize model:
	model.summary()
	
	# Tells model to predict the outputs of X_validate:
	y_new = model.predict(X_validate)

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


	##### The Straw Hats Prediction Methods #####
	
	# Display the inputs and predicted outputs:
	for i in range(len(X_validate)):
		#print ("X=%s, Predicted=%s" % (no_scale_validation_inputs[i], y_new[i]))
		#print ("Y_test =", y_validate[i])
		
		# Find the average difference between the correct and the predicted values for (x,y) or (r,theta):
		
		# For (x,y):
	#	x_difference = y_validate[i][0] - y_new[i][0]
	#	if (x_difference < 0):
	#		x_difference = -1 * x_difference
	#	x_sum = x_sum + x_difference
	#	x_diff.append(x_difference)
	#	y_difference = y_validate[i][1] - y_new[i][1]
	#	if (y_difference < 0):
	#		y_difference = -1 * y_difference
	#	y_sum = y_sum + y_difference
	#	y_diff.append(y_difference)
	#x_avg = x_sum / len(y_new)
	#y_avg = y_sum / len(y_new)

		# For (r,theta):
		r_difference = y_validate[i][0] - y_new[i][0]
		if (r_difference < 0):
			r_difference = -1 * r_difference
		r_sum = r_sum + r_difference
		r_diff.append(r_difference)
		theta_difference = y_validate[i][1] - y_new[i][1]
		if (theta_difference < 0):
			theta_difference = -1 * theta_difference
		theta_sum = theta_sum + theta_difference
		theta_diff.append(theta_difference)
	r_avg = r_sum / len(y_new)
	theta_avg = theta_sum / len(y_new)

	# Find the standard deviation of the difference between the correct and the predicted values:

	# For (x,y):
	#for i in range(len(y_new)):
	#	pre_std_x = (x_diff[i] - x_avg)**2
	#	std_x_sum = std_x_sum + pre_std_x
	#	pre_std_y = (y_diff[i] - y_avg)**2
	#	std_y_sum = std_y_sum + pre_std_y
	#std_x = math.sqrt(std_x_sum / len(ynew))
	#std_y = math.sqrt(std_y_sum / len(y_new))
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
	std_r = math.sqrt(std_r_sum / len(y_new))
	std_theta = math.sqrt(std_theta_sum / len(y_new))
	#print ("Average Difference (r) = ",r_avg)
	#print ("Average Difference (theta) = ",theta_avg)
	#print ("SD (r) = ",std_r)
	#print ("SD (theta) = ",std_theta)


	# Save y_new, y_validate, and X_validate as CSV files to pass to the GUI:
	#savetxt('Inputs.csv', no_scale_validation_inputs, delimiter=',')
	#savetxt('y_pred_3Pr.csv', y_new, delimiter=',')
	#savetxt('y_correct_3Pr.csv', y_validate, delimiter=',')
	

	# Uncomment the following code, commenting out the above fit, in order to plot the learning rate:
	# Use with validation data.
	#history = model.fit(X, y, validation_data=(X_validate,y_validate), epochs=500, batch_size=32)
	#plt.plot(history.history['loss'], label='MSE (training data)')
	#plt.plot(history.history['val_loss'], label='MSE (validation data)')
	#plt.title('MSE for The Straw Hats System Keras Model')
	#plt.ylabel('Loss')
	#plt.xlabel('N. epoch')
	#plt.legend(loc="upper left")
	#plt.show()


# Call the GUI to run the results of the validation data:
os.system("sudo python3 GUI.py")


# End #####################################################################################################
###########################################################################################################
