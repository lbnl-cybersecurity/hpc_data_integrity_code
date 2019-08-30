#!/usr/bin/python3
import os


class variables:

    def __init__(self):

        self.SYS_CHANNEL="testchainid"
        self.APP_CHANNEL="businesschannel"

        self.TIMEOUT="30"
        self.MAX_RETRY=5

        self.ORGS = 2
        self.PEERS = 2

        self.ORDERER_URL="orderer.example.com:7050"
        self.APP_CHANNEL="businesschannel"
        self.CC_NAME="dataint"   
       
        self.ORDERER_TLS_CA="/etc/hyperledger/fabric/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"
        self.ORDERER_MSP="/etc/hyperledger/fabric/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/msp"
        
        self.ORDERER_TLS_ROOTCERT="/etc/hyperledger/fabric/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt"
        self.ORG1_PEER0_TLS_ROOTCERT="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
        self.ORG1_PEER1_TLS_ROOTCERT="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.example.com/peers/peer1.org1.example.com/tls/ca.crt"
        self.ORG2_PEER0_TLS_ROOTCERT="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
        self.ORG2_PEER1_TLS_ROOTCERT="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt"
        
        self.ORDERER_ADMIN_MSP="/etc/hyperledger/fabric/crypto-config/ordererOrganizations/example.com/users/Admin@example.com/msp"
        self.ORG1_ADMIN_MSP="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
        self.ORG2_ADMIN_MSP="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp"
        self.ORG1MSP="Org1MSP"
        self.ORG2MSP="Org2MSP"
        self.ORG3MSP="Org3MSP"
        
        # Node URLS
        self.ORDERER_URL="orderer.example.com:7050"
        self.ORG1_PEER0_URL="peer0.org1.example.com:7051"
        self.ORG1_PEER1_URL="peer1.org1.example.com:7051"
        self.ORG2_PEER0_URL="peer0.org2.example.com:7051"
        self.ORG2_PEER1_URL="peer1.org2.example.com:7051"
        
        # Chaincode dataint related
        self.CC_02_NAME="dataint"
        self.CC_02_PATH="examples/chaincode/go/data_integrity"
        self.CC_02_INIT_ARGS='\'{"Args":[]}\''
        self.CC_02_UPGRADE_ARGS='{"Args":["upgrade","a","100","b","200"]}'
        self.CC_02_INVOKE_ARGS='{"Args":["initLedger"]}'
        self.CC_02_QUERY_ARGS='{"Args":["queryOriginalData","1"]}'
       
        # unique chaincode params
        self.CC_NAME=self.CC_02_NAME
        self.CC_PATH=self.CC_02_PATH
        self.CC_INIT_ARGS=self.CC_02_INIT_ARGS
        self.CC_INIT_VERSION=1.0
        self.CC_UPGRADE_ARGS=self.CC_02_UPGRADE_ARGS
        self.CC_UPGRADE_VERSION=1.1
        self.CC_INVOKE_ARGS=self.CC_02_INVOKE_ARGS
        self.CC_QUERY_ARGS=self.CC_02_QUERY_ARGS
       
        # TLS config
        self.CORE_PEER_TLS_ENABLED="true"
        
        # Generate configs
        self.GEN_IMG="yeasy/hyperledger-fabric:1.0.5  # working dir is `/go/src/github.com/hyperledger/fabric`"
        self.GEN_CONTAINER="generator"
        self.FABRIC_CFG_PATH="/etc/hyperledger/fabric"
        self.CHANNEL_ARTIFACTS="/tmp/channel-artifacts"
        self.CRYPTO_CONFIG="crypto-config"
        self.ORDERER_GENESIS="orderer.genesis.block"
        self.ORDERER_PROFILE="TwoOrgsOrdererGenesis"
        self.APP_CHANNEL_TX="new_"+self.APP_CHANNEL+".tx"
        self.UPDATE_ANCHOR_ORG1_TX="Org1MSPanchors.tx"
        self.UPDATE_ANCHOR_ORG2_TX="Org2MSPanchors.tx"
        
        # CONFIGTXLATOR
        self.CTL_IMG="yeasy/hyperledger-fabric:1.0.5"
        self.CTL_CONTAINER="configtxlator"
        self.CTL_BASE_URL="http://127.0.0.1:7059"
        self.CTL_ENCODE_URL=self.CTL_BASE_URL+"/protolator/encode"
        self.CTL_DECODE_URL=self.CTL_BASE_URL+"/protolator/decode"
        self.CTL_COMPARE_URL=self.CTL_BASE_URL+"/configtxlator/compute/update-from-configs"
        
        self.ORDERER_GENESIS_JSON=self.ORDERER_GENESIS+".json"
        self.ORDERER_GENESIS_PAYLOAD_JSON=self.ORDERER_GENESIS+"_payload.json"
        self.ORDERER_GENESIS_UPDATED_BLOCK="orderer.genesis.updated.block"
        self.ORDERER_GENESIS_UPDATED_JSON=self.ORDERER_GENESIS_UPDATED_BLOCK+".json"
        self.PAYLOAD_PATH=".data.data[0].payload"
        self.PAYLOAD_CFG_PATH=".data.data[0].payload.data.config"
        self.MAX_BATCH_SIZE_PATH=".data.data[0].payload.data.config.channel_group.groups.Orderer.values.BatchSize.value.max_message_count"
        
        # channel update config
        self.ORIGINAL_CFG_JSON="original_config.json"
        self.ORIGINAL_CFG_PB="original_config.pb"
        self.UPDATED_CFG_JSON="updated_config.json"
        self.UPDATED_CFG_PB="updated_config.pb"
        self.CFG_DELTA_JSON="config_delta.json"
        self.CFG_DELTA_PB="config_delta.pb"
        self.CFG_DELTA_ENV_JSON="config_delta_env.json"
        self.CFG_DELTA_ENV_PB="config_delta_env.pb"

    """def __init__(self):
        pass"""

    def export_locals(self, var, value):
        os.environ[var] = str(value)
        #os.system("echo $"+var)          

    def set_env_general(self):
        #os.environ["ORDERER_TLS_CA"] = "/etc/hyperledger/fabric/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"
        #os.environ['CC_INIT_VERSION'] = '1.0'
        self.export_locals("ORDERER_TLS_CA", self.ORDERER_TLS_CA)
        self.export_locals("CC_INIT_VERSION", self.CC_INIT_VERSION)
        
    def set_invoke_arg(self, arg):
        #os.environ["CC_INVOKE_ARGS"] = str(arg)
        self.CC_INVOKE_ARGS=str(arg)
	
    def set_query_arg(self, arg):
        #os.environ["CC_QUERY_ARGS"] = str(arg)
        self.CC_QUERY_ARGS=str(arg)
        
    def set_instantiate_arg(self, arg):
        #os.environ["CC_INIT_ARGS"] = str(arg)
        self.CC_INIT_ARGS=str(arg)

    def set_env_org_peer(self, org, peer):
        #TODO check if org and peer (if they are valid numbers i.e have that amount of org and peer)
        self.export_locals("CORE_PEER_LOCALMSPID", "Org"+str(org)+"MSP")
        self.export_locals("CORE_PEER_ADDRESS", getattr(self, "ORG"+str(org)+"_PEER"+str(peer)+"_URL"))

        val = getattr(self, "ORG"+str(org)+"_ADMIN_MSP")
        #print("**************************************Val is :"+val)
        self.export_locals("CORE_PEER_MSPCONFIGPATH", val)
        val2 = getattr(self, "ORG"+str(org)+"_PEER"+str(peer)+"_TLS_ROOTCERT")
        self.export_locals("CORE_PEER_TLS_ROOTCERT_FILE", val2)

"""if __name__ == "__main__":

    va = variables()
    for k, v in va.__dict__.items():
        va.export_locals(k,v)"""
