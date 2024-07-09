import sys
import random
from datetime import datetime
import json

def generate_record():
    sensor_id = f"sensor{500+1}"
    kwh = round(random.uniform(100, 500), 2)
    gps = f"{round(random.uniform(40.0, 42.0), 6)},{round(random.uniform(28.0, 30.0), 6)}"
    voltage = random.randint(210, 230)
    power_factor = round(random.uniform(0.8, 1.0), 2)
    time_str = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    return {
        "sensor_id": sensor_id,
        "kwh": kwh,
        "gps": gps,
        "voltage": voltage,
        "power_factor": power_factor,
        "time_str": time_str
    }

# Generate a sample record
record = generate_record()

# Calculate the size of a single record
record_size = sys.getsizeof(record)
print(f"Size of a single record: {record_size} bytes")

# Specify the number of records
num_records = 5000  
# Number of servers
number_servers=4


# Calculate total size
total_size = record_size * num_records
print(f"Total size for {num_records} records: {total_size} bytes --------------")

record_json = json.dumps(record)

# Calculate the size of the JSON string
record_json_size = len(record_json.encode('utf-8'))
print(f"Size of a single record in JSON: {record_json_size} bytes")

# Calculate total size for a specified number of records
total_json_size = record_json_size * num_records
print(f"Total size for {num_records} records in JSON: {total_json_size} bytes")

# Calculate the prefered max byte
prefered_max_byte = total_json_size
print(f"prefered_max_byte= {prefered_max_byte}")

#Calculate the absolute max byte
absolute_max_byte = record_json_size*number_servers*num_records
print(f"absolute_max_byte= {absolute_max_byte}")

# Calculate the max message count
max_message_count = num_records
print(f"the max_massage_count= {max_message_count}")

# Calculate the batch time out
batch_time_out=20*60/number_servers
print(f"batch_time_out={batch_time_out}")
