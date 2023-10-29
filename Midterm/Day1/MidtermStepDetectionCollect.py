import csv
from datetime import datetime
from scapy.all import *
import time
from sense_hat import SenseHat
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

red= (255,0,0)
orange = (255,165,0)
yellow = (255,255,0)
green = (0,255,0)

sense = SenseHat()

"""
Run monitor_mode.sh first to set up the network adapter to monitor mode and to
set the interface to the right channel.
To get RSSI values, we need the MAC Address of the connection 
of the device sending the packets.
"""

# Variables to be modified
dev_mac = ""  # Assigned transmitter MAC
iface_n = "wlan1"  # Interface for network adapter
duration = 10  #1Number of seconds to sniff for
#file_name = "new.csv"  # Name of CSV file where RSSI values are stored

sense=SenseHat()
path="/home/pi/Desktop/MidtermData/StepDetect/"
timestamp_fname=datetime.now().strftime("%H:%M:%S")
sense.set_imu_config(True,True,True) ## Config the Gyroscope, Accelerometer, Magnetometer
filename=path+timestamp_fname+".csv"

max_rssi = (0,0,-1000)
x_acc = []
y_acc = []
timestamps = []


def get_acc():
    begin_time = datetime.now()
    while True:
        
        accel=sense.get_accelerometer_raw()  ## returns float values representing acceleration intensity in Gs
        gyro=sense.get_gyroscope_raw()  ## returns float values representing rotational intensity of the axis in radians per second
        mag=sense.get_compass_raw()  ## returns float values representing magnetic intensity of the ais in microTeslas

        x=accel['x']

        y=accel['y']
        z=accel['z']
        xgyro = gyro['x']
        ygyro = gyro['y']
        zgyro = gyro['z']
        curr_time = datetime.now()
        timestamp=curr_time.strftime("%H:%M:%S")
        
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, x, y,z, xgyro, ygyro, zgyro])
        
        print(curr_time.second-begin_time.second)
        if abs(curr_time.second-begin_time.second)>=20:
            break

def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    #header = ["date", "time", "dest", "src", "rssi"]
    header = ['Timestamp','xacc', 'yacc', 'zacc','xgyro', 'ygyro', 'zgyro']
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

    x=accel['x']

    y=accel['y']
    z=accel['z']
    
    x_acc.append(x)
    y_acc.append(y)
   # print("cur d-", cur_dict)
    #if cur_dict['mac_1'] == 'e4:5f:01:d4:9f:f9'
    new_tuple = (x, y, cur_dict['rssi'])
    
    color = ()
    #print("jere")
    #insert MAC address here
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
            
        print("NEW RSSI: ", rssi_val)
            
    
        #print(cur_dict['rssi'],cur_dict['mac_1'],cur_dict['mac_2'])
        
    timestamp=datetime.now().strftime("%H:%M:%S")
    #with open(filename, 'a', newline='') as csvfile:
       # writer = csv.writer(csvfile)
       # writer.writerow([x, y, cur_dict['rssi'],timestamp])
        

if __name__ == "__main__":
    
    #create_rssi_file()
    #acc_thread = threading.Thread(target=get_acc)
    #acc_thread.start()
    
   # t = AsyncSniffer(iface=iface_n, prn=captured_packet_callback, store=0)
   # t.daemon = True
    #t.start()
    
    
    start_date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f") #Get current date and time

    
   #time.sleep(duration)
    #acc_thread.kill()
    get_acc()
   # t.stop()
    
    #x,y = positions_calc(x_acc,y_acc, timestamps)

    #rssi_int = [float(i) for i in rssi_vals]
   '''
   test_rssi = [-40 for i in range(len(x))]
    plt.scatter(x,y, c=test_rssi, cmap = "viridis", alpha = 0.7)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.xlim(-5,5)
    plt.ylim(-5,5)
    print("x",x)
    print("y", y)
    plt.show()
    '''
    #Plot graphs etc here 

    print("Start Time: ", start_date_time)




