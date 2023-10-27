import csv
from datetime import datetime
from scapy.all import *
import time
from sense_hat import SenseHat
import os
import random

red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)

sense = SenseHat()


dev_mac = ""  
iface_n = "wlan1"  
duration = 180  
timestamp_fname = datetime.now().strftime("%H:%M:%S")
path = "/home/pi/Desktop/lab3/IMU/newdata/"
sense.set_imu_config(True, True, True)  
filename = path + timestamp_fname + ".csv"

max_rssi = (0, 0, -1000)

learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 0.1

state_space = [(x, y) for x in range(8) for y in range(8)]
action_space = ["move_up", "move_down", "move_left", "move_right"]

q_table = {}
for state in state_space:
    q_table[state] = {action: 0 for action in action_space}

def choose_action(state):
    if random.uniform(0, 1) < exploration_prob:
        return random.choice(action_space)
    else:
        return max(q_table[state], key=q_table[state].get)

def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    header = ['x', 'y', 'RSSI', 'Timestamp']
    with open(filename, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

def update_q_table(state, action, reward, next_state):
    max_next_action_value = max(q_table[next_state].values())
    q_table[state][action] = (1 - learning_rate) * q_table[state][action] + learning_rate * (reward + discount_factor * max_next_action_value)

def captured_packet_callback(pkt):
    global max_rssi
    """Save MAC addresses, time, and RSSI values to CSV file if MAC address of src matches"""
    missed_count = 0  # Number of missed packets while attempting to write to the file
    cur_dict = {}
    try:
        
        cur_dict["mac_1"] = pkt.addr1
        cur_dict["mac_2"] = pkt.addr2
        cur_dict["rssi"] = pkt.dBm_AntSignal
    except AttributeError:
        return  # Packet formatting error

    x = sense.get_accelerometer_raw()['x']
    y = sense.get_accelerometer_raw()['y']
    accel_state = (int(x * 8), int(y * 8))

    if cur_dict['mac_1'] == "e4:5f:01:d4:9f:f9":
        rssi_val = abs(cur_dict['rssi'])
        if rssi_val > 48:
            reward = 10
        elif rssi_val <= 48 and rssi_val >= 42:
            reward = 5
        elif rssi_val < 42 and rssi_val > 36:
            reward = 2
        else:
            reward = 1
    else:
        reward = 0

    action = choose_action(accel_state)
    next_x, next_y = accel_state
    if action == "move_up":
        next_y += 1
    elif action == "move_down":
        next_y -= 1
    elif action == "move_left":
        next_x -= 1
    elif action == "move_right":
        next_x += 1
    next_state = (next_x, next_y)

    update_q_table(accel_state, action, reward, next_state)

    timestamp = datetime.now().strftime("%H:%M:%S")

if __name__ == "__main":
    create_rssi_file()
    t = AsyncSniffer(iface=iface_n, prn=captured_packet_callback, store=0)
    t.daemon = True
    t.start()
    start_date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f")

    time.sleep(duration)
    t.stop()

    print("Start Time: ", start_date_time)




