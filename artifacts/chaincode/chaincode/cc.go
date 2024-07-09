package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"strconv"
	"time"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	"github.com/hyperledger/fabric/protos/peer"
)

// SmartContract defines the Smart Contract structure
type SmartContract struct {
}

// Value defines the structure of the data stored in the ledger
type Value struct {
	SensorID string `json:"sensorID"`
	Temp     string `json:"kwh"`
	Time     string `json:"time"`
	GPS      string `json:"gps"`
	Voltage  string `json:"voltage"`
	PF       string `json:"pf"`
}

func main() {
	err := shim.Start(new(SmartContract))
	if err != nil {
		fmt.Println("Error when starting SmartContract", err)
	}
}

// Init is called when the chaincode is instantiated
func (s *SmartContract) Init(stub shim.ChaincodeStubInterface) peer.Response {
	fmt.Println("Chaincode instantiated")
	return shim.Success(nil)
}

// Invoke is called per transaction on the chaincode
func (s *SmartContract) Invoke(stub shim.ChaincodeStubInterface) peer.Response {
	function, args := stub.GetFunctionAndParameters()

	switch function {
	case "registerSensor":
		return s.registerSensor(stub, args)
	case "addTemp":
		return s.addTemp(stub, args)
	case "getHistory":
		return s.getHistory(stub, args)
	default:
		return shim.Error("Invalid function name")
	}
}

// registerSensor registers a new sensor
func (s *SmartContract) registerSensor(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	if len(args) != 1 {
		return shim.Error("Invalid number of arguments. Expecting 1")
	}
	sensorID := args[0]
	value := Value{SensorID: sensorID}
	valueAsBytes, _ := json.Marshal(value)
	err := stub.PutState(sensorID, valueAsBytes)
	if err != nil {
		return shim.Error("Failed to register sensor: " + err.Error())
	}
	return shim.Success(nil)
}

// addTemp adds a temperature record for a sensor
func (s *SmartContract) addTemp(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	if len(args) != 6 {
		return shim.Error("Invalid number of arguments. Expecting 6")
	}
	sensorID := args[0]

	valueAsBytes, err := stub.GetState(sensorID)
	if err != nil {
		return shim.Error("Failed to read sensor state: " + err.Error())
	}
	if valueAsBytes == nil {
		return shim.Error("Sensor does not exist")
	}

	var value Value
	err = json.Unmarshal(valueAsBytes, &value)
	if err != nil {
		return shim.Error("Failed to unmarshal sensor state: " + err.Error())
	}

	value.Temp = args[1]
	value.Time = args[2]
	value.GPS = args[3]
	value.Voltage = args[4]
	value.PF = args[5]

	valueAsBytes, err = json.Marshal(value)
	if err != nil {
		return shim.Error("Failed to marshal sensor state: " + err.Error())
	}

	err = stub.PutState(sensorID, valueAsBytes)
	if err != nil {
		return shim.Error("Failed to update sensor state: " + err.Error())
	}

	return shim.Success(nil)
}

// getHistory retrieves the history of transactions for a given sensor
func (s *SmartContract) getHistory(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	if len(args) != 1 {
		return shim.Error("Invalid number of arguments. Expecting 1")
	}
	sensorID := args[0]

	iterator, err := stub.GetHistoryForKey(sensorID)
	if err != nil {
		return shim.Error("Failed to get history for key: " + err.Error())
	}
	defer iterator.Close()

	var buffer bytes.Buffer
	buffer.WriteString("[")
	bArrayMemberAlreadyWritten := false
	for iterator.HasNext() {
		queryResponse, err := iterator.Next()
		if err != nil {
			return shim.Error("Failed to iterate over history results: " + err.Error())
		}
		if bArrayMemberAlreadyWritten {
			buffer.WriteString(",")
		}
		buffer.WriteString("{\"TxId\":\"")
		buffer.WriteString(queryResponse.TxId)
		buffer.WriteString("\", \"Value\":")
		if queryResponse.IsDelete {
			buffer.WriteString("null")
		} else {
			buffer.WriteString(string(queryResponse.Value))
		}
		buffer.WriteString(", \"Timestamp\":\"")
		buffer.WriteString(time.Unix(queryResponse.Timestamp.Seconds, int64(queryResponse.Timestamp.Nanos)).String())
		buffer.WriteString("\", \"IsDelete\":\"")
		buffer.WriteString(strconv.FormatBool(queryResponse.IsDelete))
		buffer.WriteString("\"}")
		bArrayMemberAlreadyWritten = true
	}
	buffer.WriteString("]")

	fmt.Printf("getHistory:\n%s\n", buffer.String())

	return shim.Success(buffer.Bytes())
}
