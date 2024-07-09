import re
import json

def extract_block_number(log_line):
    # Extract the block number from the log line
    match = re.search(r'\[([0-9]+)\]', log_line)
    if match:
        return match.group(1)
    else:
        return None

def update_logs(endorse_logs, commit_logs):
    updated_logs = []
    for endorse_log in endorse_logs:
        endorse_block_number = extract_block_number(endorse_log)
        for commit_log in commit_logs:
            commit_block_number = extract_block_number(commit_log)
            if endorse_block_number == commit_block_number:
                # Update the endorse log line with the number of committed transactions
                commit_transactions = re.search(r'Committed block \[([0-9]+)\] with ([0-9]+) transaction', commit_log)
                if commit_transactions:
                    committed_block = commit_transactions.group(1)
                    committed_transactions = commit_transactions.group(2)
                    endorsed_transactions_match = re.search(r'Validated block \[([0-9]+)\]', endorse_log)
                    if endorsed_transactions_match:
                        endorsed_transactions = endorsed_transactions_match.group(1)
                        updated_log = re.sub(r'Validated block \[([0-9]+)\]', f'Validated block [{committed_block}] with {committed_transactions} transactions', endorse_log)
                        updated_logs.append(updated_log)
                break
        else:
            updated_logs.append(endorse_log)  # If no matching commit log found, keep the endorse log as it is
    return updated_logs

# Read log lines from files
with open('C:/cygwin64/home/delag/project/blockchain-network-on-kubernetes-correct/data/logs/parsed-logs/peerCommitMetricOrg1peer2.json', 'r') as commit_file:
    commit_logs = commit_file.readlines()

with open('C:/cygwin64/home/delag/project/blockchain-network-on-kubernetes-correct/data/logs/parsed-endorse/peerEndorseOrg2peer1.json', 'r') as endorse_file:
    endorse_logs = endorse_file.readlines()

# Update logs
updated_logs = update_logs(endorse_logs, commit_logs)

# Write updated logs to file
with open('C:/cygwin64/home/delag/project/blockchain-network-on-kubernetes-correct/data/logs/parsed-endorse/updatePeer2EndorseMetric.json', 'w') as update_file:
    update_file.writelines(updated_logs)
