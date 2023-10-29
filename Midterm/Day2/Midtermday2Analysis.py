import csv
from datetime import datetime
from scapy.all import *
import time
from sense_hat import SenseHat
import os
#import pandas as pd
import matplotlib.pyplot as plt
import threading
import pandas as pd

xpos = []
ypos= []

path="/home/pi/Desktop/lab3/MidtermComp/"
timestamp_fname=datetime.now().strftime("%H:%M:%S")
filename=path+"midterm2Analysis"+".csv"
'''

def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    #header = ["date", "time", "dest", "src", "rssi"]
    header = ['x','y', 'RSSI', 'Timestamp']
    with open(filename, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

def integrateAccs(x_accs, y_accs):
	
    timestamp = np.array([x[1] for x in x_accs])
    x_axis= np.array(x_accs)
    y_axis = np.array(y_accs)
    y_axis=df[3]

    ### CALIBERATION
    x_calib_mean = np.mean(x_axis[10:1000])
    ## caliberate x,y,z to reduce the bias in accelerometer readings. Subtracting it

    # change the upper and lower bounds for computing the mean where the RPi is in

    x_calib = x_axis - x_calib_mean
    x_calib = x_calib[:]
    timestamp = timestamp[:]
    y_calib_mean = np.mean(y_axis[10:1000])
    y_calib = y_axis - y_calib_mean
    y_calib = y_calib[:]
    timestamp = timestamp[:]
    timestamp = timestamp[:]

    dt = (timestamp[len(timestamp)-1] - timestamp[0]) / len(timestamp)

    y_vel = [0]
    for i in range(len(y_calib)-1):
        y_vel.append(y_vel[-1] + dt * y_calib[i])
    y = [0]
    for i in range(len(y_vel)-1):
        y.append(y[-1] + dt * y_vel[i])

    x_vel = [0]
    for i in range(len(x_calib)-1):
        x_vel.append(x_vel[-1] + dt * x_calib[i])
    x = [0]
    for i in range(len(x_vel)-1):
        x.append(x[-1] + dt * x_vel[i])
    
    return (x,y, timestamp)

# writes positions to csv file

def convertToCSV(x,y, timestamps):
    for rssi,timestamp in rssi_vals:
        min_time_diff = float('inf')
        closest_index = 0
        for i in range(len(x)):
            time_diff = abs(timestamps[i] - timestamp)
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_index = i
        with open(filename, "a", encoding="UTF8") as f:
			writer = csv.writer(f)
			writer.writerow([x[i],y[i], rssi, timestamp])
   '''
   
if __name__ == "__main__":
	import matplotlib.pyplot as plt
	import pandas as pd
	import numpy as np

	# Load the data from your CSV file
	fname = "/home/pi/Desktop/lab3/IMU/newdata/midterm2coords.csv"
	df = pd.read_csv(fname, header=None)
	df = df.dropna()

	# Extract data from the DataFrame
	xpos = np.array(df[0][1:])
	ypos = np.array(df[1][1:])
	rssi = np.array(df[2][1:])
	rssi_int = [abs(int(rs)) for rs in rssi]

	# Determine the limits for x and y axes
	x_min, x_max = xpos.min(), xpos.max()
	y_min, y_max = ypos.min(), ypos.max()

	# Create a colormap and normalize the data
	cmap = plt.get_cmap('viridis')
	norm = plt.Normalize(min(rssi_int), max(rssi_int))
	scalar_map = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
	colors = [scalar_map.to_rgba(num) for num in rssi_int]

	# Set axis limits based on data range
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)

	# Set the desired tick locations and labels for x-axis
	x_ticks = np.arange(x_min, x_max + 1, step=1)  # Adjust step as needed
	plt.xticks(x_ticks)

	# Set the desired tick locations and labels for y-axis
	y_ticks = np.arange(y_min, y_max + 1, step=1)  # Adjust step as needed
	plt.yticks(y_ticks)

	# Create the scatter plot
	plt.scatter(xpos, ypos, c=colors, cmap='viridis', s=20)
	plt.show()

	'''
	#create_rssi_file()
	fname = "/home/pi/Desktop/lab3/IMU/newdata/midterm2coords.csv"
	df = pd.read_csv(fname, header = None)
	df=df.dropna()
	import numpy as np
	xpos = np.array(df[0][1:])
	ypos = np.array(df[1][1:])
	rssi = np.array(df[2][1:])
	#xp, yp, tss = integrateAccs(x_accs, y_accs)
	rssi_int = [abs(int(rs)) for rs in rssi]
	cmap = plt.get_cmap('viridis')
	norm = plt.Normalize(min(rssi_int), max(rssi_int))
	scalar_map = plt.cm.ScalarMappable(cmap = cmap, norm = norm)
	colors = [scalar_map.to_rgba(num) for num in rssi_int]
	plt.xlim(-4,4)
	plt.ylim(0,12)
	plt.scatter(
	'''
