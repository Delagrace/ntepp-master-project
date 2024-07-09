import json

# Read the flow.json file
with open('C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/node-red/flows-registration.json', 'r') as file:
    flow_data = json.load(file)


# Function to update sensorID values
def update_sensor_id(node, start, end):
    for rule in node['rules']:
        # Parse 'to' string to dictionary
        to_dict = json.loads(rule['to'])
        if 'username' in to_dict:
            sensor_id = to_dict['username']
            if sensor_id.startswith('user'):
                current_sensor_number = int(sensor_id.split('user')[-1])
                if start <= current_sensor_number <= end:
                    new_sensor_number = 4 #current_sensor_number + 250
                    to_dict['username'] = 'user' + str(new_sensor_number)
                    # Update 'to' string in the rule
                    rule['to'] = json.dumps(to_dict)

# Update sensorID values
for node in flow_data:
    if node['type'] == 'change':
        update_sensor_id(node, 1, 250)

# Update sensorID values
for node in flow_data:
    if node['type'] == 'change':
        update_sensor_id(node, 1, 250)

# Write the updated JSON back to the file
with open('C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/node-red/flows-registration.json', 'w') as file:
    json.dump(flow_data, file, indent=2)