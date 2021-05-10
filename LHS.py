#!/usr/bin/python3.8


# Import all necessary Python libraries:
import lhsmdu
import numpy as np
import matplotlib.pyplot as plt
from numpy import savetxt


###########################################################################################################
###########################################################################################################
## The Straw Hats: The Seer - EE493 Senior Design                                                      ####
## Latin Hypercube Sampling (LHS) of Testing Enviroment                                                ####
## Author: Evan Peelen & Tate Harsch-Hudspeth                                                          ####
## Last Edit Made: April 15, 2021                                                                      ####
## University: Sonoma State University                                                                 ####
###########################################################################################################
###########################################################################################################


# Objective: 
# To use an unbiased method of random sampling, implmenting the Latin Hypercube function 
# with multi-dimensional uniformity. The following Python code calls two Latin Hypercube functions
# where n data points are plotted on a square of side length L.
# The grid and data set is color coded. Note: 
# The authors of the following code would use the Latin Hypercube function in sequence with
# The Seer, to plot an unbiased amount of data points to train The Seer's neural network.
# The origin of The Seer's test envrionment would be at 2.75 meters and 
# due to the radiation patterns and hardware implemented within The Seer.
# The following code would account for this shift of origin from (0,0) to
# (2.75,0), as well as a 0.5 meter padding space needed between The Seer's receiving antenna array 
# and the closest test data points.


# Set number of sample points:
n = 100

k = lhsmdu.sample(2,n) # Latin Hypercube Function  with multi-dimensional uniformity
# The project only utilized 2D but more dimensions could be included, check out 
# the lhsmdu project at pypi.org/project/lhsmdu/
k = np.array(k*5) # Set grind size or dimensions of of testing environment for first Latin Hypercube function

# Uncomment to include a second set of LHS points
#randSeed = 11 # Create random Latin Hypercube seed to have two unbiased data sets and samples
# The random seed does not need to be LHS, other methods are available.
#l = lhsmdu.sample(2,50, randomSeed=randSeed) #Second Latin Hypercube Function with (2D) uniformity
#l = np.array(l*5.5) #Set grind size or dimensions of testing environment for second Latin Hypercube function

fig = plt.figure()
ax = fig.gca()
ax.set_xticks(np.arange(0,7,.5)) # Set the number of ticks on the axis and the spacing between them
ax.set_yticks(np.arange(0,7,.5)) # Set the number of ticks on the axis and the spacing between them

ax.set_title('The Seer - Latin Hyper Cube Sample')
ax.set_xlabel('Distance (Meters)', fontsize = 12)
ax.set_ylabel('Distance (Meters)', fontsize = 10)

plt.scatter(k[0], k[1], color="g", label="LHS-MDU") # Plot the LHS points
#plt.scatter(l[0], l[1], color="r", label="LHS-MDU") # Plot the second set of LHS points
print (k)

plt.grid() # Plots the sampling space


# Shifts the points from the origin at the bottom left corner of the sampling space to the origin
# being placed at the center of the y = 0 line, at (2.5,0) relative to the original frame and then prints the
# new set of (x,y) values relative to the new coordinate frame.

# Initialize array
x = []
# Adjust the x coordinate to meet the new coordinate frame
for i in range(len(k[0])):
	if (k[0][i] < 2.5):
		x2 = -1*(2.5 - k[0][i])
		x.append(x2)
	elif (k[0][i] > 2.5):
		x2 = k[0][i] - 2.5
		x.append(x2)
	elif (k[0][i] == 2.5):
		x2 = 0
		x.append(x2)

# Initialize array		
y = []
# Append the y coordinate to an array of a different form
for j in range(len(k[1])):
	y2 = k[1][j]
	y.append(y2)

# Initialize arrays
xy = []
xy2 = []
xy3 = []
# Prepare the new coordiante pairs to be printed as an array
for q in range(len(x)):
	for t in range(0,1):
		xy.append(x[q])
		xy.append(y[q])
	xy2.append(xy)
for j in range(n):
	c1 = ((2*j) + 1)
	c2 = (2*j)
	if (c1 > (2*n)):
        	break
	print("[",xy2[0][c2],",",xy2[0][c1],"]")
	xy3_row = [xy2[0][c2],xy2[0][c1]]
	xy3.append(xy3_row)
	
plt.show()


# Save the (x,y) coordinates as a CSV file:
savetxt('xyLHS.csv', xy3, delimiter=',')


## End ####################################################################################################
###########################################################################################################

