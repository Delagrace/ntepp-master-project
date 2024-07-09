import requests
import json
import random
from datetime import datetime
import time

# Base URL for the REST API
base_url = "http://localhost:5000/api"

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

# Main function to send data
def main():
    username = "user5"
    data_responses = []
    for i in range(5000):
        sensor_id = f"sensor{i+10000}"
        
        # Generate random data
        kwh = round(random.uniform(100, 500), 2)
        gps = f"{round(random.uniform(40.0, 42.0), 6)},{round(random.uniform(28.0, 30.0), 6)}"
        voltage = random.randint(210, 230)
        power_factor = round(random.uniform(0.8, 1.0), 2)
        
        data_response = add_temp(username, "channel0", "chaincode0", sensor_id, kwh, gps, voltage, power_factor)
        data_responses.append(data_response)
        print(f"Data sent to sensor {sensor_id} response:", data_response)

        # Optional sleep to avoid overwhelming the server (adjust as necessary)
        time.sleep(0.001)

if __name__ == "__main__":
    main()
