import requests
import random
from datetime import datetime
import threading
import time
import tkinter as tk
from tkinter import ttk

# Base URL for the REST API
base_url = "http://localhost:3000/api"

# Event to signal threads to stop
stop_event = threading.Event()

# Function to add temperature data
def add_temp(username, channel, smartcontract, sensor_id, kwh, gps, voltage, power_factor):
    url = f"{base_url}/addTemp"
    date = datetime.now()
    time_str = date.strftime('%d-%m-%Y %H:%M:%S')
    
    payload = {
        "username": username,
        "channel": channel,
        "smartcontract": smartcontract,
        "args": {
            "sensorID": sensor_id,
            "kwh": str(kwh),
            "time": time_str,
            "gps": gps,
            "voltage": str(voltage),
            "pf": str(power_factor)
        }
    }
    response = requests.post(url, json=payload)
    return response.json()

# Function to simulate a single meter sending data every 'rate' minutes
def send_meter_data(sensor_id, rate):
    username = "user6"
    channel = "channel0"
    smartcontract = "chaincode0"
    
    while not stop_event.is_set():
        # Generate random data
        kwh = round(random.uniform(100, 500), 2)
        gps = f"{round(random.uniform(40.0, 42.0), 6)},{round(random.uniform(28.0, 30.0), 6)}"
        voltage = random.randint(210, 230)
        power_factor = round(random.uniform(0.8, 1.0), 2)
        
        data_response = add_temp(username, channel, smartcontract, sensor_id, kwh, gps, voltage, power_factor)
        print(f"Data sent to sensor {sensor_id} response:", data_response)
        
        # Wait for the specified rate before sending the next data
        stop_event.wait(rate * 60)  # rate in minutes converted to seconds

# Function to start the meter threads
def start_meters(num_meters, rate):
    global threads
    threads = []
    for i in range(num_meters):
        sensor_id = f"sensor{i+1}"
        thread = threading.Thread(target=send_meter_data, args=(sensor_id, rate))
        threads.append(thread)
        thread.start()
        
        # Sleep for a short time to avoid starting all threads at the exact same moment
        time.sleep(300 / num_meters)  # 5 minutes / num_meters to spread the starts over 5 minutes

# Function to stop all threads
def stop_meters():
    stop_event.set()
    for thread in threads:
        thread.join()
    print("All meters stopped.")

# Function to handle the start button click
def on_start_button_click():
    num_meters = int(num_meters_entry.get())
    rate = int(rate_entry.get())
    stop_event.clear()
    threading.Thread(target=start_meters, args=(num_meters, rate)).start()

# Function to handle the stop button click
def on_stop_button_click():
    stop_meters()

# Create the GUI application
app = tk.Tk()
app.title("Meter Data Sender")

# Number of meters input
tk.Label(app, text="Number of Meters:").grid(row=0, column=0, padx=10, pady=5)
num_meters_entry = tk.Entry(app)
num_meters_entry.grid(row=0, column=1, padx=10, pady=5)

# Rate input
tk.Label(app, text="Rate (minutes):").grid(row=1, column=0, padx=10, pady=5)
rate_entry = tk.Entry(app)
rate_entry.grid(row=1, column=1, padx=10, pady=5)

# Start button
start_button = ttk.Button(app, text="Start", command=on_start_button_click)
start_button.grid(row=2, columnspan=2, pady=10)

# Stop button
stop_button = ttk.Button(app, text="Stop", command=on_stop_button_click)
stop_button.grid(row=3, columnspan=2, pady=10)

# Run the application
app.mainloop()
