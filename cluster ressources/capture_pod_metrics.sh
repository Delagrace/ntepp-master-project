#!/bin/bash

while true; do
    timestamp=$(date)
    pods_info=$(kubectl top pods --all-namespaces)
    json="{\"timestamp\": \"$timestamp\", \"pods\": $pods_info}"

    echo $json >> pods-computer-ressource.json

    sleep 10
done
