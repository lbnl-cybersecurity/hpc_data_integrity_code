package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	//"strconv"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	"github.com/hyperledger/fabric/protos/peer"
)

// SmartContract implements a simple chaincode to manage inputs to the chain
type SmartContract struct {
}

// OriginalData bal bla
type OriginalData struct {
	Id   string `json:"id"`
	Hval string `json:"hval"`
}

// Software template for an app
type Software struct {
	Name    string `json:"name"`
	Version string `json:"version"`
}

// System reperesents a system processing some data
type System struct {
	Os   Software   `json:"os"`
	Apps []Software `json:"apps"`
}

// OutputData represents an output of a computation
type OutputData struct {
	Id        string `json:"id"`
	Input     string `json:"input"`
	Hval      string `json:"hval"`
	Processed System `json:"system"`
}

var originalDataCounter = 0
var outputDataCounter = 0

//Init method to be called when the chaincode is initalized
// to initalize the chain with data use other function, see initLedger()
func (s *SmartContract) Init(APIstub shim.ChaincodeStubInterface) peer.Response {
	return shim.Success(nil)
}

func (s *SmartContract) initLedger(APIstub shim.ChaincodeStubInterface) peer.Response {

	odata := OriginalData{
		Id:   "1",
		Hval: "this_is_the_hash_of_the_original_data"}

	//encode to JSON
	originaldata, _ := json.Marshal(odata)
	//fmt.Println(string(joutput1))

	/*os := Software{
	      Name: "ubuntu",
	      Version: "14.04"}

	  app1 := Software{
	      Name : "Snort",
	      Version : "2.9"}

	  app2 := Software{
	      Name : "Mysql",
	      Version : "5.6"}

	  sys := System{
	      Os : *os,
	      Apps : []Software{*app1, *app2}}


	  opdata := &OutputData{

	      Id : "1",
	      Input : "11",
	      Hval  : "asdfsdf4534",
	      Processed : *sys}*/

	opdata := OutputData{

		Id:    "2",
		Input: "11",
		Hval:  "sf3345345tet",
		Processed: System{
			Os:   Software{Name: "ubuntu", Version: "14.04"},
			Apps: []Software{{Name: "Snort", Version: "2.9"}, {Name: "Mysql", Version: "5.6"}}}}

	//encode to JSON
	outputdata, _ := json.Marshal(opdata)

	//add the orifginal data to blockchain

	// Using counter as ID
	//APIstub.PutState(strconv.Itoa(originalDataCounter), originaldata)
	//originalDataCounter += 1

	APIstub.PutState(odata.Id, originaldata)

	//Add the output of a computation into the blockchain
	//APIstub.PutState(strconv.Itoa(outputDataCounter), outputdata)
	//outputDataCounter += 1

	APIstub.PutState(opdata.Id, outputdata)

	return shim.Success(nil)
}

func (s *SmartContract) queryOriginalData(APIstub shim.ChaincodeStubInterface, args []string) peer.Response {

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	originalDataAsBytes, _ := APIstub.GetState(args[0])
	/*var result map[string]interface{}

	if err := json.Unmarshal(originalDataAsBytes, &result); err != nil {
		panic(err)
	}
	return shim.Success(result)*/

	//use this to return the bytes output
	return shim.Success(originalDataAsBytes)
}

func (s *SmartContract) queryOutputData(APIstub shim.ChaincodeStubInterface, args []string) peer.Response {

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	outputDataAsBytes, _ := APIstub.GetState(args[0])
	return shim.Success(outputDataAsBytes)
}

func (s *SmartContract) addOriginalData(APIstub shim.ChaincodeStubInterface, args []string) peer.Response {

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	var od = OriginalData{Id: args[0], Hval: args[1]}

	originalDataAsBytes, _ := json.Marshal(od)
	APIstub.PutState(args[0], originalDataAsBytes)

	return shim.Success(nil)
}

func (s *SmartContract) addOutputData(APIstub shim.ChaincodeStubInterface, args []interface{}) peer.Response {

	if len(args) != 4 {
		return shim.Error("Incorrect number of arguments. Expecting 4")
	}

	//check the types, specifically te 4th arg
	//if len(args) != 4 {
	//	return shim.Error("4th arg should be a type of System")
	//}

	var od = OutputData{Id: args[0].(string), Input: args[1].(string), Hval: args[2].(string), Processed: args[3].(System)}

	outputDataAsBytes, _ := json.Marshal(od)
	APIstub.PutState(args[0].(string), outputDataAsBytes)

	return shim.Success(nil)
}

//Invoke method used by apps to call functions on the chaincode
func (s *SmartContract) Invoke(APIstub shim.ChaincodeStubInterface) peer.Response {

	// Retrieve the requested Smart Contract function and arguments
	function, args := APIstub.GetFunctionAndParameters()
	// select the function to interact with the ledger appropriately
	if function == "addOriginalData" {
		return s.addOriginalData(APIstub, args)
	} else if function == "addOutputData" {

		//var arg []interface{args[0], args[1],args[2], args[3]}
		arg := make([]interface{}, len(args))
		for i, v := range args {
			arg[i] = v
		}
		return s.addOutputData(APIstub, arg)
	} else if function == "queryOriginalData" {
		return s.queryOriginalData(APIstub, args)
	} else if function == "queryOutputData" {
		return s.queryOutputData(APIstub, args)
	} else if function == "initLedger" {
		return s.initLedger(APIstub)
	} else if function == "queryByHashValue" {
		return s.queryByHashValue(APIstub, args)
	}

	return shim.Error("Invalid Smart Contract function name.")
}

// a fuction to query by hash value
func (s *SmartContract) queryByHashValue(stub shim.ChaincodeStubInterface, args []string) peer.Response {

	if len(args) < 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	hval := args[0]

	queryString := fmt.Sprintf("{\"selector\":{\"hval\":\"%s\"}}", hval)

	queryResults, err := getQueryResult(stub, queryString)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(queryResults)
}

// This method is from marble chaincode example
// It accepts a query string, which is a format of CouchDB query
func (s *SmartContract) queryByAnyColumn(stub shim.ChaincodeStubInterface, args []string) peer.Response {

	//   0
	// "queryString"
	if len(args) < 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	queryString := args[0]

	queryResults, err := getQueryResult(stub, queryString)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(queryResults)
}

// this method query the couchDB by executing the query string
func getQueryResult(stub shim.ChaincodeStubInterface, queryString string) ([]byte, error) {

	fmt.Printf("- getQueryResultForQueryString queryString:\n%s\n", queryString)

	resultsIterator, err := stub.GetQueryResult(queryString)
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	// buffer is a JSON array containing QueryRecords
	var buffer bytes.Buffer
	buffer.WriteString("[")

	bArrayMemberAlreadyWritten := false
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}
		// Add a comma before array members, suppress it for the first array member
		if bArrayMemberAlreadyWritten == true {
			buffer.WriteString(",")
		}
		buffer.WriteString("{")
		//buffer.WriteString("\"")
		//buffer.WriteString(queryResponse.Key)
		//buffer.WriteString("\"")

		buffer.WriteString("\"Record\":")
		// Record is a JSON object, so we write as-is
		buffer.WriteString(string(queryResponse.Value))
		buffer.WriteString("}")
		bArrayMemberAlreadyWritten = true
	}
	buffer.WriteString("]")

	fmt.Printf("- getQueryResultForQueryString queryResult:\n%s\n", buffer.String())

	return buffer.Bytes(), nil
}

/*func set(stub shim.ChaincodeStubInterface, args []string) (string, error) {
    if len(args) != 2 {
            return "", fmt.Errorf("Incorrect arguments. Expecting a key and a value")
    }

    err := stub.PutState(args[0], []byte(args[1]))
    if err != nil {
            return "", fmt.Errorf("Failed to set asset: %s", args[0])
    }
    return args[1], nil
}

// Get returns the value of the specified asset key
func get(stub shim.ChaincodeStubInterface, args []string) (string, error) {
    if len(args) != 1 {
            return "", fmt.Errorf("Incorrect arguments. Expecting a key")
    }

    value, err := stub.GetState(args[0])
    if err != nil {
            return "", fmt.Errorf("Failed to get asset: %s with error: %s", args[0], err)
    }
    if value == nil {
            return "", fmt.Errorf("Asset not found: %s", args[0])
    }
    return string(value), nil
}*/

func main() {
	if err := shim.Start(new(SmartContract)); err != nil {
		fmt.Printf("Error starting SimpleAsset chaincode: %s", err)
	}
}
