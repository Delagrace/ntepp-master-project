#!/bin/bash

for ((i=1; i<=1502; i++)); do
    sensor="sensor$i"
    kubectl exec -it blockchain-org2peer1-c98896c8c-zddrv  -- bash -c "peer chaincode invoke -o blockchain-orderer:31010 -C channel0 -n chaincode0 -c '{\"Args\":[\"getHistory\", \"$sensor\"]}'" > $sensor.json
done
