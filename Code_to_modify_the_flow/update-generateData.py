import json

# Function to update the endpoint URL in the flow.json file
def update_flow_json(filename, old_url, new_url):
    with open(filename, 'r') as file:
        flow_data = json.load(file)

    # Loop through all nodes
    for node in flow_data:
        if node.get('func') == old_url:
            node['func'] = new_url
            print(node.get('func'))

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(flow_data, file, indent=2)

# Usage example
#for i in range(1, 250):
old_url = "const kwh = (Math.random() * 100).toFixed(2);const latitude = (Math.random() * 90).toFixed(6);const longitude = (Math.random() * 180).toFixed(6);const voltage = Math.floor(Math.random() * (240 - 100 + 1)) + 100;const powerFactor = (Math.random() * (1.0 - 0.5)) + 0.5;const generatedData = { kwh: kwh, gps: { latitude: latitude, longitude: longitude}, voltage: voltage, powerFactor: powerFactor};if( msg.payload === false ) {\n    return null;\n}\nmsg.payload =generatedData ;\nreturn msg;"
new_url = "const kwh = (Math.random() * 100).toFixed(2);const latitude = (Math.random() * 90).toFixed(6);const longitude = (Math.random() * 180).toFixed(6); const voltage = (Math.floor(Math.random() * (240 - 100 + 1)) + 100).toFixed(6);const powerFactor = ((Math.random() * (1.0 - 0.5)) + 0.5).toFixed(6);const generatedData = { kwh: kwh, gps: latitude + \", \" + longitude, voltage: voltage, powerFactor: powerFactor};if( msg.payload === false ) {\n    return null;\n}\nmsg.payload =generatedData ;\nreturn msg;"
update_flow_json('C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/node-red/flows-Meterdata.json', old_url, new_url)
