To run Day 1:
- Run MidtermCode.py and specify the file name in the file that you want to save the CSV file to
- Afterwards run the MidtermCodeAnalysis.py file and use the same filename from earlier to retrieve its data and plot the RSSI values on a (x,y) cartesian map of the competition room
- Command: sudo python3 MidtermCode.py

To run Day 2:
- Run the MidtermDay2.py file and specify file name that you want to save the CSV file to
- This will result in a CSV file containing the x and y positions, along with the RSSI values
- We can then use this CSV file and put it in either MidtermDay2Analysis.py, or convert the CSV files into a list of tuples and insert that list into the data list in grapher.py, which will color code (in ranges) the RSSI values and plot them on the x-y plane.
- Command: sudo python3 MidtermDay2.py
