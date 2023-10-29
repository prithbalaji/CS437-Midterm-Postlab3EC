import matplotlib.pyplot as plt

# Sample data
data = [
	(2.49,5.42,28),(1.72,2.16,50)
,(3.82,3.91,45),
(1.28,9.45,34),
(3.57,10.42,39),
(2.12,8.82,49),
(3.21,-9.30,48),
(1.4,10.27,48),
(1.9,3.20,35),
(1.3,2.5,47),
(-1.1,2.28,32)
	


]

# Organize data into RSSI ranges and colors
rssi_ranges = {
    (25, 35): 'green',
    (36, 43): 'yellow',
    (44, 100): 'red',
}

# Create empty lists to store points for each RSSI range
data_by_rssi = {color: [] for color in rssi_ranges.values()}

for x, y, rssi in data:
    for (rssi_min, rssi_max), color in rssi_ranges.items():
        if rssi_min <= rssi <= rssi_max:
            data_by_rssi[color].append((x, y))

# Create the scatter plot for each RSSI range
for color, data_points in data_by_rssi.items():
    if data_points:
        x, y = zip(*data_points)
        plt.scatter(x, y, color=color, label=f'RSSI Range: {color}')

# Add labels and legend
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(-4,4)
plt.ylim(0,12)
plt.title('Scatter Plot of X and Y Color-Coded by RSSI Range')
plt.legend()

# Show the plot
plt.show()
