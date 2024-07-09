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
old_url = f"data = msg.payload;\n\nvar date = new Date();\nvar options = {{ timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' }};\nvar time = date.toLocaleDateString('tr-TR', options);\n\n\nmsg.payload = {{'username':'user1','channel':'channel0', 'smartcontract':'chaincode0', 'args': {{'sensorID':'sensor1', 'kwh':data.kwh,'time':time, 'gps':data.gps, 'voltage':data.voltage, 'pf':data.powerFactor}} }};\nmsg.headers = {{'content-type':'application/json'}};\n\nreturn msg;"
new_url = f"data = msg.payload;\n\nvar date = new Date();\nvar options = {{ timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' }};\nvar time = date.toLocaleDateString('tr-TR', options);\n\n\nmsg.payload = {{'username':'user4','channel':'channel0', 'smartcontract':'chaincode0', 'args': {{'sensorID':'sensor1', 'kwh':data.kwh,'time':time, 'gps':data.gps, 'voltage':data.voltage, 'pf':data.powerFactor}} }};\nmsg.headers = {{'content-type':'application/json'}};\n\nreturn msg;"
update_flow_json('C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/node-red/flows-Meterdata.json', old_url, new_url)
