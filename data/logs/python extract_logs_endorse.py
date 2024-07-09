
import re
import json
import os

# Define the regular expression pattern to match the log lines
pattern = r".*Validated block \[\d+\] in \d+ms.*"

# Check if the log file exists
log_file_path = 'C:/cygwin64/home/delag/project/blockchain-network-on-kubernetes-correct/data/logs/logsOrg1peer2.json'
if not os.path.exists(log_file_path):
    print(f"Error: File '{log_file_path}' not found.")
    exit(1)

# Open the log file for reading
with open(log_file_path, 'r') as log_file:
    # Read the log file line by line
    log_data = log_file #json.load(log_file)

    # Initialize an empty list to store matching log lines
    matching_lines = []

    # Iterate over the log lines
    for line in log_data:
        #print(line)  # Print each line for debugging
        # Check if the line matches the pattern
        # Check if the line matches the pattern
        if re.match(pattern, line):
            # If it matches, append it to the list
            matching_lines.append(line.strip())

# Write the matching log lines to a JSON file
with open('C:/cygwin64/home/delag/project/blockchain-network-on-kubernetes-correct/data/logs/parsed-endorse/peerEndorseOrg1peer2.json', 'w') as json_file:
    json.dump(matching_lines, json_file, indent=4)

print("Matching log lines written to peerMetric.json.")
