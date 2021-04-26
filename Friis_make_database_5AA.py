#!/usr/bin/python3.8


# Imports:
import random
import math
import numpy as np
#from numpy import loadtxt
from numpy import savetxt


######################################################################################################
######################################################################################################
## The Straw Hats: The Seer - EE493 Senior Design                                                 ####
## Friis Path Loss Simulation - 5 Antenna Array - Simulated Data for Neural Network               ####
## Author: Tate Harsch-Hudspeth                                                                   ####
## Last Edit Made: March 31st, 2021                                                               ####
## University: Sonoma State University, Department of Engineering Science                         #### 
######################################################################################################
######################################################################################################


# Define frequency and assume speed of light:
f = 750000000 # In Hz
c = 300000000 # In m/s
Dr = Dt = 0.447 # In Watts
Pt = 0.01 # In Watts
Z0 = 377 # In Ohms

# Calculate wavelength and angular frequency:
lambda_wav = c / f # In m
omega = 2 * math.pi * f # In Hz

# Initialize arrays to hold values of: (r, theta) or (x,y), Vr (Rx Voltage), Phi (Rx Phase shift):
#x_answer = []
#y_answer = []
r_answer = []
theta_answer = []
Vr = []
data = []

# For Troubleshooting:
#Power_Rx = []
#Voltage_Rx = []
#Phi_Rx = []
#d_answer = []
#angles = []

# Generate random sample that does not repeat:
x_array = random.sample(range(-1400,1400),500)
y_array = random.sample(range(100,1400),500)

# Generate vector and convert to polar coordinates:
for i in range(0,499):
	x = x_array[i]
	y = y_array[i]
	if (x > -100 and x < 100):
		while (x > -100 and x < 100):
			x = random.randrange(-1400,1400)
	x = x / 100
	y = y / 100
#	print ("x = ", x)
#	print ("y = ", y)
	r = math.sqrt((x ** 2) + (y ** 2))
	theta_rad = math.atan2(y,x)
	theta = (theta_rad * 180) / math.pi
	if (theta < 0):
		theta = theta + 360
#	print ("r = ", r)
#	print ("theta = ", theta)
#	x_answer.append(x)
#	y_answer.append(y)
	r_answer.append(r)
	theta_answer.append(theta)

	# Define vectors from fixed point to antenna_1 through antenna_4, spaced lambda_wav / 2 apart
	# x1 --> (x = 0) - lambda_wav, x2 --> (x = 0) - lambda_wav / 2
	# x3 --> (x = 0) + lambda_wav / 2, x4 --> (x = 0) + lambda_wav
	# Due to the linear nature of the array, only posative y values are considered.
	# The linear array ensures no shadowing will occurr between the antennas aside from the extemes at y = 0.
	# These extremes will not be considered (no cell phone would be so close to the base station).
	d = r
	if (x > 1):
		angle_1 = math.atan(y / (x + lambda_wav))
		d1 = y / math.sin(angle_1)
		angle_2 = math.atan(y / (x + (lambda_wav / 2)))
		d2 = y / math.sin(angle_2)
		angle_3 = math.atan(y / (x - (lambda_wav / 2)))
		d3 = y / math.sin(angle_3)
		angle_4 = math.atan(y / (x - lambda_wav))
		d4 = y / math.sin(angle_4)
	if (x < 1):
		angle_1 = math.atan(y / ((-1*x) - lambda_wav))
		d1 = y / math.sin(angle_1)
		angle_2 = math.atan(y / ((-1*x) - (lambda_wav / 2)))
		d2 = y / math.sin(angle_2)
		angle_3 = math.atan(y / ((-1*x) + (lambda_wav / 2)))
		d3 = y / math.sin(angle_3)
		angle_4 = math.atan(y / ((-1*x) + lambda_wav))
		d4 = y / math.sin(angle_4)

	# Calculate phase shift in radians, Phi = omega * l / c. In rads/s
	Phi_0 = omega * d / c
	Phi_1 = omega * d1 / c
	Phi_2 = omega * d2 / c
	Phi_3 = omega * d3 / c
	Phi_4 = omega * d4 / c

	# Calcultate the relative phase difference between the antenna phase shifts and the reference phase.
	# In our final project design we divide the reference signal as a complex number by the complex signals
	# at the receviers prior to FFT processing to obtain the relative phase difference.
	# The division of the complex phasors results in a subtraction of the phase.
	Phi_1 = Phi_0 - Phi_1
	Phi_2 = Phi_0 - Phi_2
	Phi_3 = Phi_0 - Phi_3
	Phi_4 = Phi_0 - Phi_4

	# Friis Equation to solve for distance:
	# d = (lambda_wav / 4 * pi * math.sqrt((Pr / Pt) / Dt * Dr))

	# Use Friis Equation to find the received power at each antenna. In Watts
	# Friis Equation to find received power:
	Pr1 = Pt * Dt * Dr * ((lambda_wav / (4 * math.pi * d1)) ** 2)
	Pr2 = Pt * Dt * Dr * ((lambda_wav / (4 * math.pi * d2)) ** 2)
	Pr3 = Pt * Dt * Dr * ((lambda_wav / (4 * math.pi * d3)) ** 2)
	Pr4 = Pt * Dt * Dr * ((lambda_wav / (4 * math.pi * d4)) ** 2)

	# Calculate voltage amplitude from received power using impedence of free space, Z0 ~ 377 Ohms. In Volts
	Vr1 = math.sqrt(Pr1 * Z0)
	Vr2 = math.sqrt(Pr2 * Z0)
	Vr3 = math.sqrt(Pr3 * Z0)
	Vr4 = math.sqrt(Pr4 * Z0)

	# Save array of [8 inputs,2 outputs] and append each iteration:
	#data_round = [Vr1,Phi_1,Vr2,Phi_2,Vr3,Phi_3,Vr4,Phi_4,x,y]
	data_round = [Vr1,Phi_1,Vr2,Phi_2,Vr3,Phi_3,Vr4,Phi_4,r,theta]
	data.append(data_round)

	# Turn tensor into numpy array:
	data_numpy = np.array(data)

	# Save array of [8 inputs, 2 outputs] into CSV file:
	#savetxt('data_Friis_xy.csv', data_numpy, delimiter=',')
	savetxt('data_Friis_rtheta.csv', data_numpy, delimiter=',')


# End ###############################################################################
#####################################################################################


	# For troubleshooting:

	# Puts values into arrays for troubleshooting:
	#Pr_round = [Pr1,Pr2,Pr3,Pr4]
	#Power_Rx.append(Pr_round)
	#Vr = [Vr1,Vr2,Vr3,Vr4]
	#Voltage_Rx.append(Vr)
	#Phi = [Phi_1,Phi_2,Phi_3,Phi_4]
	#Phi_Rx.append(Phi)
	#d_round = [d1,d2,d3,d4]
	#d_answer.append(d_round)
	#angle_round = [theta_rad, angle_2, angle_3, angle_4]
	#angles.append(angle_round)
	#print ("x_answer = ", x_answer)
	#print ("y_answer = ", y_answer)
	#print ("r_answer = ", r_answer)
	#print ("theta_answer = ", theta_answer)
	#print ("Power_Rx = ", Power_Rx)
	#print ("Voltage_Rx = ", Voltage_Rx)
	#print ("Phi_Rx = ", Phi_Rx)
	#print ("d_answer = ", d_answer)
	#print ("angles = ", angles)
	#print (r_numpy)
	#print (np.__version__)

	# Turns above arrays into numpy arrays:
	#x_numpy = np.array(x_answer)
	#y_numpy = np.array(y_answer)
	#r_numpy = np.array(r_answer)
	#theta_numpy = np.array(theta_answer)
	#Power_Rx_numpy = np.array(Power_Rx)
	#Vr_numpy = np.array(Voltage_Rx)
	#Phi_numpy = np.array(Phi_Rx)
	#d_answer_numpy = np.array(d_answer)
	#angles_numpy = np.array(angles)

# Throw numpy arrays into text files:
#np.savetxt("sim_database_x.txt", x_numpy)
#np.savetxt("sim_database_y.txt", y_numpy)
#np.savetxt("sim_database_r.txt", r_numpy)
#np.savetxt("sim_database_theta.txt", theta_numpy)
#np.savetxt("sim_database_PowerRx.txt", Power_Rx_numpy)
#np.savetxt("sim_database_Vr.txt", Vr_numpy)
#np.savetxt("sim_database_Phi.txt", Phi_numpy)
#np.savetext("sim_database_d.txt", d_answer_numpy)
#np.savetext("sim_database_angles", angles_numpy)
