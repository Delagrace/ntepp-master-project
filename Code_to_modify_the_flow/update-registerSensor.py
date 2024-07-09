import json

# Function to update the endpoint URL in the flow.json file
def update_flow_json(filename, old_url, new_url):
    with open(filename, 'r') as file:
        flow_data = json.load(file)

    # Loop through all nodes
    for node in flow_data:
        if node.get('url') == old_url:
            node['url'] = new_url

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(flow_data, file, indent=2)

# Usage example
update_flow_json('C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/node-red/flows-registration.json', 'http://rest-api:4000/api/registerSensor', 'http://rest-api:3000/api/registerSensor')
