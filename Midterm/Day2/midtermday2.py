import csv
from datetime import datetime
from scapy.all import *
import time
from sense_hat import SenseHat
import os
#import pandas as pd
import matplotlib.pyplot as plt
import threading
#path="/home/pi/Desktop/lab3/IMU/newdata/"
#filename=path+"midtermcomp2+".csv"

red= (255,0,0)
orange = (255,165,0)
yellow = (255,255,0)
green = (0,255,0)

sense = SenseHat()

x_accs = []
y_accs = []
rssi_vals = []

"""
Run monitor_mode.sh first to set up the network adapter to monitor mode and to
set the interface to the right channel.
To get RSSI values, we need the MAC Address of the connection 
of the device sending the packets.
"""

# Variables to be modified
dev_mac = ""  # Assigned transmitter MAC
iface_n = "wlan1"  # Interface for network adapter
duration = 60  #1Number of seconds to sniff for
#file_name = "new.csv"  # Name of CSV file where RSSI values are stored

sense=SenseHat()
path="/home/pi/Desktop/lab3/IMU/newdata/"
timestamp_fname=datetime.now().strftime("%H:%M:%S")
sense.set_imu_config(True,True,True) ## Config the Gyroscope, Accelerometer, Magnetometer
filename=path+"midterm2"+".csv"

max_rssi = (0,0,-1000)

def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    #header = ["date", "time", "dest", "src", "rssi"]
    header = ['x','y', 'RSSI', 'Timestamp']
    with open(filename, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def captured_packet_callback(pkt):
    global max_rssi
    """Save MAC addresses, time, and RSSI values to CSV file if MAC address of src matches"""
    missed_count = 0  # Number of missed packets while attempting to write to file
    cur_dict = {}
    try:
        
        cur_dict["mac_1"] = pkt.addr1
        cur_dict["mac_2"] = pkt.addr2
        cur_dict["rssi"] = pkt.dBm_AntSignal
    except AttributeError:
        return  # Packet formatting error

    
    date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f").split(",") #Get current date and time
    date = date_time[0]
    time1 = date_time[1]
    
    accel=sense.get_accelerometer_raw()  ## returns float values representing acceleration intensity in Gs
    gyro=sense.get_gyroscope_raw()  ## returns float values representing rotational intensity of the axis in radians per second
    mag=sense.get_compass_raw()  ## returns float values representing magnetic intensity of the ais in microTeslas

    xacc=accel['x']

    yacc=accel['y']
    z=accel['z']
    new_tuple = (xacc, yacc, cur_dict['rssi'])
    
    color = ()
    if cur_dict['mac_2'] == "e4:5f:01:d4:9f:f9":# or cur_dict['mac_1'] =="e4:5f:01:d4:9c:b1":
        rssi_val = abs(cur_dict['rssi'])
        if rssi_val >48:
            color = red
        elif rssi_val <=48 and rssi_val >=42:
            color = orange
        elif rssi_val <42 and rssi_val >36:
            color = yellow
        elif rssi_val <= 36:
            color = green
            
        timestamp=datetime.now()
        timestamp_str = timestamp.strftime("%H:%M:%S")
        print("NEW RSSI: ", rssi_val, timestamp)
        
        rssi_vals.append((rssi_val*-1, timestamp))
        
        for x in range(8):
            for y in range(8):
                sense.set_pixel(x,y,color)
        
        time.sleep(0.5)
        sense.clear()

    
        #print(cur_dict['rssi'],cur_dict['mac_1'],cur_dict['mac_2'])
        

def collect_acc():
    begin_timestamp = datetime.now()
    
    while (timestamp - begin_timestamp).total_seconds() < 60:
        
        accel=sense.get_accelerometer_raw()  ## returns float values representing acceleration intensity in Gs
        gyro=sense.get_gyroscope_raw()  ## returns float values representing rotational intensity of the axis in radians per second
        mag=sense.get_compass_raw()  ## returns float values representing magnetic intensity of the ais in microTeslas

        xacc=accel['x']

        yacc=accel['y']
        timestamp=datetime.now() #.strftime("%H:%M:%S")

        x_accs.append((xacc, timestamp))
        y_accs.append((yacc, timestamp))

def integrateAccs():
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

def convertToCSV(x,y, timestamps):
    for rssi,timestamp in rssi_vals:
        min_time_diff = float('inf')
        closest_index = 0
        for i in range(len(x)):
            time_diff = abs(timestamps[i] - timestamp)
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_index = i
        # find closest timestamp in positions
        with open(filename, "a", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow([x[i],y[i], rssi, timestamp])

if __name__ == "__main__":
    create_rssi_file()
    collectThread = threading.Thread(target = collect_acc)
    collectThread.start()
    t = AsyncSniffer(iface=iface_n, prn=captured_packet_callback, store=0)
    t.daemon = True
    t.start()
    
    start_date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f") #Get current date and time

    time.sleep(duration)
    x,y,ts = integrateAccs()
    convertToCSV(x,y,ts)
    collectThread.join()
    t.stop()

    print("Start Time: ", start_date_time)



