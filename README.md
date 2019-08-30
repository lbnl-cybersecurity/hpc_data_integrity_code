# Blockchain Based Remote Data Integrity Checking Tool

A 'Smart' Data Integrity checking tool ...
 
## Getting Started
To test the tool on your local machine, get a copy of this project and follow installation process below. See deployment for notes on how to deploy a custom blockchain network. The tool can be used in the following ways, 
* A command line tool (DataIntc.py) and
* An interface / simple API (DataInt.py)

### Prerequisites

* This tool uses [Hyperledger Fabric (HLF)](https://www.hyperledger.org/projects/fabric) as a backend blockchain. Follow the link to see more about HLF. 
* To deploy HLF on a multi-node setup we use [Cello](https://www.hyperledger.org/projects/cello), which is a blockchain provision and operation system. It manages the infrastructure for Blockchain network and provides blockchain as a service (BaaS). 
* We provide a script to install all the requirements and setup cello    

```
cd cello-deployment/ && ./cello-setup.sh
```

[TODO] * 

### Testing

 There are two options to test this tool on HLF network
   * Using [Hyperledger Fabric Samples](http://hyperledger-fabric.readthedocs.io/en/latest/samples.html) code (mainly for non-linux machine users)
   * Using cello setup

1. Using Hyperledger Fabric Samples

* Follow [this link](http://hyperledger-fabric.readthedocs.io/en/latest/samples.html) and install / setup the example 
* In the setup find a folder named "fabric-samples"
* Add everything in the folder `papers_and_presentations/hpc_data_integrity/code/data-integrity/chaincode/data_integrity/` to `fabric-samples/chaincode/`
* Follow similar procedure as in the [example](http://hyperledger-fabric.readthedocs.io/en/latest/chaincode4ade.html#install-hyperledger-fabric-samples) 
* While starting a chaincode select the data_integrity folder to use `data_integrity.go`  

2. Using cello (single node setup) 

* Get `cello-setup.sh` from this github repo under  `papers_and_presentations/hpc_data_integrity/code/data-integrity/cello-deployment/` and run  `./cello-setup.sh -w`

* Replace `fabric-solo-4.yaml` file in  `cello/src/agent/docker/_compose_files/fabric-1.0` with the same file name from this repo under `papers_and_presentations/hpc_data_integrity/code/data-integrity/cello-deployment/`

* Add everything inside `papers_and_presentations/hpc_data_integrity/code/data-integrity/chaincode/data_integrity/` to `cello/src/agent/docker/_compose_files/fabric-1.0/examples/chaincode/go`

* Pull couchDB docker image `docker pull hyperledger/fabric-couchdb:x86_64-1.0.5`

* Copy `papers_and_presentations/hpc_data_integrity/code/data-integrity/bc-app/` to `cello/src/agent/docker/_compose_files/fabric-1.0/scripts`

* Export environment variables by `source cello/src/agent/docker/_compose_files/fabric-1.0/scripts/vars.sh` 

* Start docker compose `docker-compose -f cello/src/agent/docker/_compose_files/fabric-1.0/fabric-solo-4.yaml up -d`

* All the commands you need to run  DataInt tool 

```
git clone https://github.com/lbnl-cybersecurity/papers_and_presentations.git

mv papers_and_presentations/hpc_data_integrity/code/data-integrity/cello-deployment/cello-setup.sh .

chmod +x cello-setup.sh

./cello-setup.sh -w

cd papers_and_presentations/hpc_data_integrity/code/data-integrity/

cp cello-deployment/fabric-solo-4.yaml  ~/cello/src/agent/docker/_compose_files/fabric-1.0/

cp -r chaincode/* ~/cello/src/agent/docker/_compose_files/fabric-1.0/examples/chaincode/go

docker pull hyperledger/fabric-couchdb:x86_64-1.0.5

cp -r bc-app/* ~/cello/src/agent/docker/_compose_files/fabric-1.0/scripts

cp -r DataSourceModules*  ~/cello/src/agent/docker/_compose_files/fabric-1.0/scripts

cd ~/cello/src/agent/docker/_compose_files/fabric-1.0 && source scripts/vars.sh

docker-compose -f fabric-solo-4.yaml up -d

```

### Running example with dummy data (add random data to the chain and check its integrity)

* Connect to `*_cli` container and `cd /tmp/scripts`
* run `./DataIntc.py setup` 
* To add hash of random data run `./DataIntc.py add -r` 
   - The random string will be stored in a folder named `/output` 
* To check if a given file is in the blockchain run `./DataIntc.py verify -f PATH_TO_FILE` or if the input is string `./DataIntc.py verify -s STRING`


### How to use with other codes 

* Once the blockchain network is up and running 
* import DataInt.py into your project

```
from Dataint import *
```

* To check the integrity of a given data (assuming a signature is already stored in the system)
* create an instance of DataInt class and call _verify(data, dataType)_

```
dataInt = DataInt()
dataInt.verify(data, dataType)
```
* _data:_ can be a path to a file or a string
* _dataType:_ can be "file" if the data is path to file or "string" if the given data is string

* To store a signature in the blockchain

```
dataInt = DataInt()
dataInt.add(data, dataType)
```
* The parameters are the same as above

### Installing

* See [Cello](https://www.hyperledger.org/projects/cello) for more detail and its architecture
* Once Cello is running, connect to the container with '_cli' in the name
 
* To get container name run 

``` 
docker ps 
```
 
* To connect to CLI_CONTAINER 

```
docker exec -it CLI_CONTAINER bash
```

* TO setup the the chaincode

```
cd /tmp/scripts && ./DataIntc.py setup
```

* This will 
   1. Create channel
   2. Peers will join the channel  
   3. It will install the chain code (aka Smart Contract)
   4. Instantiate the contract



## Deployment

[TODO]
* explain how to deploy cello and configure fabric network 

## Built With

* [Hyperledger Fabric](https://www.hyperledger.org/projects/fabric) - Permissioned blockchain implementation
* [Cello](https://www.hyperledger.org/projects/cello) - Blockchain infrastructure management


## Versioning

[TODO] 

## Authors

* [Amir Teshome](http://people.rennes.inria.fr/Amir-Teshome.Wonjiga/)  
* [Sean Peisert](http://crd.lbl.gov/sean-peisert)

## License and Copyright

* [License](license.txt)  
* [Copyright](Legal.txt)  
