import requests
import json
import time

# Base URL for the REST API
base_url = "http://localhost:6000/api"

# Function to enroll an admin
def enroll_admin(admin_name, password):
    url = f"{base_url}/enrollAdmin"
    payload = {
        "adminName": admin_name,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response.json()

# Function to register a user
def register_user(admin_name, username):
    url = f"{base_url}/registerUser"
    payload = {
        "adminName": admin_name,
        "username": username
    }
    response = requests.post(url, json=payload)
    return response.json()

# Function to register a sensor
def register_sensor(username, channel, smartcontract, sensor_id):
    url = f"{base_url}/registerSensor"
    payload = {
        "username": username,
        "channel": channel,
        "smartcontract": smartcontract,
        "args": {
            "sensorID": sensor_id
        }
    }
    response = requests.post(url, json=payload)
    return response.json()

# Main function to perform the registration
def main():
    # Register a single user (user0)
    username = "user5"
    channel = "channel0"
    smartcontract = "chaincode0"

    # Register sensors for user0 5000
    sensor_responses = []
    for i in range(5000):
        sensor_id = f"sensor{15000+i}"
        sensor_response = register_sensor(username, channel, smartcontract, sensor_id)
        sensor_responses.append(sensor_response)
        print(f"Sensor {sensor_id} registration response:", sensor_response)

        # Optional sleep to avoid overwhelming the server (adjust as necessary)
        time.sleep(0.001)

if __name__ == "__main__":
    main()
