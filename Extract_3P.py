#!/usr/bin/python3.8


# Import Satements:
import math
import numpy as np
from numpy import loadtxt
from numpy import savetxt


###########################################################################################################
###########################################################################################################
## The Straw Hats: The Seer - EE493 Senior Design                                                      ####
## Data Extraction - For Extracting Values from GNU Radio Flowgraph                                    ####
## Author: Tate Harsch-Hudspeth                                                                        ####
## Last Edit Made: 04/15/2021                                                                          ####
## University: Sonoma State University                                                                 ####
###########################################################################################################
###########################################################################################################


# Set choice to 1 for training data, set choice to 2 for validation data:
#choice = 1
choice = 2

if (choice == 1):
	xy = loadtxt('xyLHS.csv', delimiter=',') # Load data from CSV file
	n = len(xy) # Number of samples to process
	x = []
	y = []
	for i in range(0,n):
		x.append(xy[i][0])
		y.append(xy[i][1])
		# print (xy[i])

	# Read binary files from GNU Radio:
	data_xy = []
	data_rtheta = []
	m = 1
	for i in range(0,n):
		# Measurement 12 was corrupted, so skip M12:
		if (i == 11):
			m +=1
			continue
		else:
			# Power 1
			read_data_mag1 = np.fromfile(file='A1_mag_M'+str(m)+'.dat', dtype=np.float32)
			Power_1 = read_data_mag1[len(read_data_mag1)-1]
			#print ("Power_01 = ", Power_1)
			# Power 2
			read_data_mag2 = np.fromfile(file='A2_mag_M'+str(m)+'.dat', dtype=np.float32)
			Power_2 = read_data_mag2[len(read_data_mag2)-1]
			#print ("Power_02 = ", Power_2)
			# Power 3
			read_data_mag3 = np.fromfile(file='A3_mag_M'+str(m)+'.dat', dtype=np.float32)
			Power_3 = read_data_mag3[len(read_data_mag3)-1]
			#print ("Power_03 = ", Power_3)
			
			# Determine the length of the array extracted from the binary data file:
			#print (len(read_data_mag1))

			# Add (x,y) and (r,theta):
			x_M = x[i]
			y_M = y[i]
			r = math.sqrt((x_M ** 2) + (y_M ** 2))
			theta_rad = math.atan2(y_M,x_M)
			theta = (theta_rad * 180) / math.pi
			if (theta < 0):
				theta = theta + 360
			m += 1
			
			# Put the measurement data into an array:
			data_xy_row = [Power_1,Power_2,Power_3,x_M,y_M]
			data_rtheta_row = [Power_1,Power_2,Power_3,r,theta]
			data_xy.append(data_xy_row)
			data_rtheta.append(data_rtheta_row)

	# Save the measurements into a format where we can combine them into a larger NumPy array made up of these tensors.
	data_xy_numpy = np.array(data_xy)
	data_rtheta_numpy = np.array(data_rtheta)
	print ("data XY = ",data_xy_numpy)
	print ("data RTH = ",data_rtheta_numpy)

	# Save as CSV File:
	savetxt('data_xy.csv', data_xy_numpy, delimiter=',')
	savetxt('data_rtheta.csv', data_rtheta_numpy, delimiter=',')

elif (choice == 2):
	# For Validation Data:

	V_xy = loadtxt('validation.csv', delimiter=',') # Load data from CSV file
	vn = len(V_xy) # Number of samples to process
	xv = []
	yv = []
	for i in range(0,vn):
		xv.append(V_xy[i][0])
		yv.append(V_xy[i][1])
		# print (V_xy[i])

	# Read binary files from GNU Radio:
	datav_xy = []
	datav_rtheta = []
	m = 101
	for i in range(0,vn):
			# Power 1
			read_data_mag1 = np.fromfile(file='A1_mag_M'+str(m)+'.dat', dtype=np.float32)
			Power_1 = read_data_mag1[len(read_data_mag1)-1]
			#print ("Power_01 = ", Power_1)
			# Power 2
			read_data_mag2 = np.fromfile(file='A2_mag_M'+str(m)+'.dat', dtype=np.float32)
			Power_2 = read_data_mag2[len(read_data_mag2)-1]
			#print ("Power_02 = ", Power_2)
			# Power 3
			read_data_mag3 = np.fromfile(file='A3_mag_M'+str(m)+'.dat', dtype=np.float32)
			Power_3 = read_data_mag3[len(read_data_mag3)-1]
			#print ("Power_03 = ", Power_3)
			
			# Determine the length of the array extracted from the binary data file:
			#print (len(read_data_mag1))

			# Add (x,y) and (r,theta):
			x_vM = xv[i]
			y_vM = yv[i]
			rv = math.sqrt((x_vM ** 2) + (y_vM ** 2))
			theta_radv = math.atan2(y_vM,x_vM)
			thetav = (theta_radv * 180) / math.pi
			if (thetav < 0):
				thetav = thetav + 360
			m += 1
			
			# Put the measurement data into an array:
			datav_xy_row = [Power_1,Power_2,Power_3,x_vM,y_vM]
			datav_rtheta_row = [Power_1,Power_2,Power_3,rv,thetav]
			datav_xy.append(datav_xy_row)
			datav_rtheta.append(datav_rtheta_row)
		
	# Save the measurements into a format where we can combine them into a larger NumPy array made up of these tensors.
	datav_xy_numpy = np.array(datav_xy)
	datav_rtheta_numpy = np.array(datav_rtheta)
	print ("data XY = ",datav_xy_numpy)
	print ("data RTH = ",datav_rtheta_numpy)

	# Save as CSV File:
	savetxt('data_xy_validation.csv', datav_xy_numpy, delimiter=',')
	savetxt('data_rtheta_validation.csv', datav_rtheta_numpy, delimiter=',')
	

## End ###############################################################################################################
######################################################################################################################
