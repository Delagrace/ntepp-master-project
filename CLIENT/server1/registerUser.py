import requests
import json
import time

# Base URL for the REST API
base_url = "http://localhost:3000/api"

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
    # Enroll the admin
    admin_response = enroll_admin("admin", "adminpw")
    print("Admin enrollment response:", admin_response)

    # Register a single user (user0)
    username = "user1"
    user_response = register_user("admin", username)
    print(f"User {username} registration response:", user_response)


if __name__ == "__main__":
    main()
