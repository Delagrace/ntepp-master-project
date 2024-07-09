import re
import json
import os
import pandas as pd

import json

def process_log_file(file_path):
    transactions_data = {}

    with open(file_path, 'r') as file:
        for line in file:
            if "[channel0] Validated block" in line:
                start_index = line.find("with") + len("with")
                end_index = line.find("transactions")
                transaction_count = int(line[start_index:end_index].strip())

                time_start_index = line.find("in") + len("in")
                time_end_index = line.find("ms", time_start_index)
                time_taken = int(line[time_start_index:time_end_index].strip())

                if transaction_count is not None and time_taken is not None:
                    if transaction_count not in transactions_data:
                        transactions_data[transaction_count] = []
                    transactions_data[transaction_count].append(time_taken)

    return transactions_data

def main():
    log_file_path = "C:/cygwin64/home/delag/project/blockchain-network-on-kubernetes-correct/data/logs/parsed-endorse/updatePeer2EndorseMetric.json"
    transactions_data = process_log_file(log_file_path)

    for transactions, times in transactions_data.items():
        avg_time = sum(times) / len(times)
        print(f"{transactions} transaction(s) took an average of {avg_time:.2f} ms.")

if __name__ == "__main__":
    main()


