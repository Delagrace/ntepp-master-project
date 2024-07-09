import re
import json
import os

import json
import os
import re

# Define start and end markers
start_marker = r".*Got policy manager for channel \[channel0\] with flag \[true\]\.*"
end_marker = r".*\[channel0\] Committed block \[\d+\] with \d+ transaction\(s\).*"

# Check if the log file exists
log_file_path = 'C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/data/logs/logsOrg1peer2_new.json'
if not os.path.exists(log_file_path):
    print(f"Error: File '{log_file_path}' not found.")
    exit(1)

# Open the log file for reading
with open(log_file_path, 'r') as log_file:
    # Read the log file line by line
    log_data = log_file.readlines()

    # Initialize an empty list to store matching log lines
    matching_lines = []

    # Initialize a flag to indicate when to start capturing lines
    capture = False

    # Iterate over the log lines
    for line in log_data:
        # Check if the line matches the start marker
        if re.match(start_marker, line):
            # If already capturing, add an empty line to separate blocks
            if capture:
                matching_lines.append('')
            # Start capturing lines
            capture = True
        # Check if the line matches the end marker
        elif re.match(end_marker, line):
            # Stop capturing lines
            capture = False
        # If we're capturing lines, append them to the list
        elif capture:
            matching_lines.append(line.strip())

# Write the matching log lines to a JSON file
with open('C:/Users/delag/OneDrive/Documents/blockchain-network-on-kubernetes-correct/data/logscaptured_lines_throughput.json', 'w') as json_file:
    json.dump(matching_lines, json_file, indent=4)

print("Matching log lines written to captured_lines.json.")
