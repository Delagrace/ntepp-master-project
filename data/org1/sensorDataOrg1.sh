#!/bin/bash

for ((i=1; i<=1502; i++)); do
    sensor="sensor$i"
    kubectl exec -it blockchain-org1peer1-69f785df48-2ghz8 -- bash -c "peer chaincode invoke -o blockchain-orderer:31010 -C channel0 -n chaincode0 -c '{\"Args\":[\"getHistory\", \"$sensor\"]}'" > $sensor.json
done
