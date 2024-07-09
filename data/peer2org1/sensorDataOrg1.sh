#!/bin/bash

for ((i=1; i<=70; i++)); do
    sensor="sensor$i"
    kubectl exec -it blockchain-org1peer2-74dc6657d6-hvlxm -- bash -c "peer chaincode query -C channel0 -n chaincode0 --peerAddresses blockchain-org1peer1:30110 -c '{\"Args\":[\"getHistory\", \"$sensor\"]}'" > "$sensor.json"
done
