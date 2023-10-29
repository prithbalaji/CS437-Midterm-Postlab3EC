import csv
from datetime import datetime
from scapy.all import *
import time
from sense_hat import SenseHat
import os
#import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path="/home/pi/Desktop/MidtermData/"
timestamp_fname = "21:21:03"
filename=path+timestamp_fname+".csv"

def positions_calc(x_acc, y_acc, timestamps) :
    x_calib_mean = np.mean(x_acc)
    x_calib = x_acc - x_calib_mean
    x_calib = x_calib[:]
    y_calib_mean = np.mean(y_acc)
    y_calib = y_acc - y_calib_mean
    y_calib = y_calib[:]
    timestamps = timestamps[:]
    
    time_format = "%H:%M:%S"
    time_obj1 = datetime.strptime(timestamps[len(timestamps)-1], time_format)
    obj1_secs = time_obj1.second+ 60*time_obj1.minute
    time_obj_first = datetime.strptime(timestamps[1],time_format)
    obj_first_secs = time_obj_first.second+ 60*time_obj_first.minute
   
    dt = (obj1_secs-obj_first_secs)/len(timestamps)
    print(dt)
    y_vel = [0]
    for i in range(len(y_calib)-1):
        y_vel.append(y_vel[-1] + dt * y_calib[i])
    y = [0]
    for i in range(len(y_vel)-1):
        y.append(y[-1] + dt * y_vel[i])

    ## Integrations along X axis
    x_vel = [0]
    for i in range(len(x_calib)-1):
        x_vel.append(x_vel[-1] + dt * x_calib[i])

    x = [0]
    for i in range(len(x_vel)-1):
        x.append(x[-1] + dt * x_vel[i])

    return x,y

df = pd.read_csv(filename, header=None)
df = df.dropna()
print(df[0])
x_acc = df[0]
print(x_acc)
x_acc = [float(i) for i in x_acc]
y_acc = df[1]
y_acc = [float(i) for i in y_acc]
rssi_vals = df[2]
timestamps = df[3]
x,y = positions_calc(x_acc,y_acc, timestamps)

rssi_int = [float(i) for i in rssi_vals]
test_rssi = [-40 for i in range(len(x))]
plt.scatter(x,y, c=test_rssi, cmap = "viridis", alpha = 0.7)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
print("x",x)
print("y", y)
plt.show()


