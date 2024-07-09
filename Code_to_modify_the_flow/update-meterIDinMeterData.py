import json

# Function to update the endpoint URL in the flow.json file
def update_flow_json(filename):
    with open(filename, 'r') as file:
        flow_data = json.load(file)
    j=1
    k=2
    # Iterate over each node in the flow_data
    for i, node in enumerate(flow_data) :
        # Check if 'func' key exists in the node
        
        if 'func' in node and node['name']=='Body / Headers':
            print(j)
            # Construct the new sensorID with the incremented value
            new_sensor_id = f"sensor{j}"
            # Update the sensorID in the 'func' string
            node['func'] = node['func'].replace(f"'sensor{k}'", f"'{new_sensor_id}'")
            j=j+1
            k=k+1
            

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(flow_data, file, indent=2)

# Usage example
update_flow_json('C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/node-red/flows-Meterdata.json')
