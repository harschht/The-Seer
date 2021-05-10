#!/usr/bin/python3.8


# Imports:
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import math


###########################################################################################################
###########################################################################################################
## The Straw Hats: The Seer - EE493 Senior Design                                                      ####
## Graphical User Interface (GUI)                                                                      ####
## Author: Victor Madrid & Evan Peelen                                                                 ####
## Documentation by Tate Harsch-Hudspeth                                                               ####
## Last Edit Made: 04/20/2021                                                                          ####
## University: Sonoma State University, Department of Engineering Science                              #### 
###########################################################################################################
###########################################################################################################


# Extracts the validation inputs from the CSV passed along by the neural network
prx = np.loadtxt("Inputs.csv", delimiter=",")
count_row = prx.shape[0]  # Gives number of rows
count_col = prx.shape[1]  # Gives number of columns

power = [] # Inputs
# Appends the inputs to an array with a new format
for i in range(count_row):
	for j in range(count_col):
		power.append(prx[i][j])


# Extracts the correct values, measured by the team, from the CSV passed along by the neural network
y_cor = np.loadtxt("y_correct_3Pr.csv", delimiter=",")
count_row = y_cor.shape[0]  # Gives number of rows

cor_dis = [] # These are the correct r values
cor_theta = [] # These are the correct theta values
for i in range(count_row):
	cor_dis.append(y_cor[i][0])
	cor_theta.append(y_cor[i][1])

# Extracts the predicted values from the CSV passed along by the neural network
y_pred = np.loadtxt("y_pred_3Pr_test3.csv", delimiter=",")
count_row = y_pred.shape[0]  # Gives number of rows

pred_dis = [] # These are the predicted r values
pred_theta = [] # These are the predicted theta values
for i in range(count_row):
	pred_dis.append(y_pred[i][0])
	pred_theta.append(y_pred[i][1])


# Finds the difference between the correct r and the predicted r
dis_acc = 0
for i in range(len(pred_dis)):
	x = cor_dis[i] - pred_dis[i]
	if x < 0:
		x = x * -1
	dis_acc = dis_acc + x
dis_acc = dis_acc / (len(pred_dis))

# Finds the difference between the correct theta and the predicted theta
theta_acc = 0
for i in range(len(pred_theta)):
	x = cor_theta[i] - pred_theta[i]
	if x < 0:
		x = x * -1
	theta_acc = theta_acc + x
theta_acc = theta_acc / (len(pred_theta))


# Calculates the percent of validation data that fail to meet our required accuracy metrics
counter = 0
for i in range(len(y_pred)):
	r_counter = 0
	theta_counter = 0
	r_difference = y_cor[i][0] - y_pred[i][0]
	theta_difference = y_cor[i][1] - y_pred[i][1]
	if (r_difference < 0):
		r_difference = -1*(r_difference)
	if (r_difference > 1.0):
        	r_counter = 1
        	counter += 1
	if (theta_difference < 0):
        	theta_difference = -1*(theta_difference)
	if (theta_difference > 45.0):
		theta_counter = 1
        	counter += 1
    	if (r_counter == 1 and theta_counter == 1):
        	counter -= 1
sys_acc = (10 - counter)*10


# This section defines the look and feel of the GUI using Tkinter
def show():
	listBox.insert(END, "\t\t\t  THE SEER \t\t \n")
	listBox.insert(END,"\t")
	listBox.insert(END,"\n")
	listBox.insert(END, "\tInputs \t ")
	listBox.insert(END, "\t\t      Predicted Outputs \t \n")
	listBox.insert(END,"\t")
	listBox.insert(END,"\n")
	listBox.insert(END, " Power [dBW]\t\t\t\t ")
	listBox.insert(END, "    Distance \t ")
	listBox.insert(END, "\t Angle \t \n")
	counter = 0
	listBox.insert(END, " ")
	for i in range(0,int((len(pred_dis)))):
		for j in range(0,3):
			listBox.insert(END,('%s' % float('%.2g' % (power[(j + counter)]))))
			listBox.insert(END,"  " )
		counter = counter + 3
		listBox.insert(END, " \t\t\t\t     ")
		listBox.insert(END,('%s' % float('%.2g' % (pred_dis[i]))))
		listBox.insert(END, "m ")
		listBox.insert(END, "  \t\t  ")
 		listBox.insert(END,('%s' % float('%.2g' % (pred_theta[i]))))
		listBox.insert(END, "°")
		listBox.insert(END, " \n ")
		listBox.insert(END, " \n ")
	listBox.insert(END, "Avg. Distance Diff. \t ")
	listBox.insert(END, " Avg. Theta Diff. \t ")
	listBox.insert(END, "System Accuracy\n")
	listBox.insert(END, " ")
	listBox.insert(END,('%s' % float('%.2g' % (dis_acc))))
	listBox.insert(END, "m")
	listBox.insert(END, "\t\t\t")
	listBox.insert(END,('%s' % float('%.2g' % (theta_acc))))
	listBox.insert(END, "°")
	listBox.insert(END, "\t \t   ")
	listBox.insert(END, sys_acc)
 	listBox.insert(END, "%")


# This section defines the polar plot using matplotlib
def graph():
	for i in range(len(pred_dis)):
		theta = (0,((math.pi / 180) * pred_theta[i]))
		r = ((0,pred_dis[i]))
		# Create polar plot here
		plt.rcParams['axes.facecolor'] = 'black'
		plt.polar(theta, r, color='green')
		plt.title(("Predicted Output " + str(i+1)), va='bottom')
		plt.show()

# This section brings the previous sections together to form a functioning GUI
scores = Tk()
label = Label(scores,bg= 'black', fg='green', text="5G DOA\t\t\t\t\t                ", font=(30)).grid(row = 0, columnspan = 3)
listBox= Text(scores, height = 28, width = 60, bg= 'black', fg='green')
listBox.grid(row = 1,column= 0, columnspan = 2)
scores.title("Team Straw Hats")
show()
showGraph = Button(scores, text="Show Graph", width=15, command=graph).grid(row=4, column=0)
closeButton = Button(scores, text = "Close",width = 15, command=exit).grid(row = 4, column = 1)
scores.mainloop()
