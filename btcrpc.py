# -*- coding: utf-8 -*-
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def extract_coinbase_data(block_height):

	# rpc_user and rpc_password are set in the bitcoin.conf file
	rpc_user = "abdfhsjbe231389dhn"
	rpc_password = "mhgfdsw345678ijhxcvbn98uygbn"
	rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))

	block_hash = rpc_connection.getblockhash(block_height)
	block = rpc_connection.getblock(block_hash)
	txs = block["tx"]

	if block_height > 0:
		raw_coinbase_tx = rpc_connection.getrawtransaction(txs[0])
		coinbase_tx = rpc_connection.decoderawtransaction(raw_coinbase_tx)
	
	# coinbase_tx for genesis block is not retrievable via rpc
	elif block_height == 0:
		coinbase_tx = {
	    	"txid" : "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
	    	"version" : 1,
			"locktime" : 0,
			"vin" : [
			    {
			        "coinbase" : "04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73",
			        "sequence" : 4294967295
			    }
			],
			"vout" : [
			    {
			        "value" : 50.00000000,
			        "n" : 0,
			        "scriptPubKey" : {
			            "asm" : "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f OP_CHECKSIG",
			            "hex" : "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac",
			            "reqSigs" : 1,
			            "type" : "pubkey",
			            "addresses" : [
			                "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
			            ]
			        }
			    }
			]
		}	

	return coinbase_tx["vin"][0]["coinbase"].decode("hex")

def update_coinbase_tx_data_db():

	dir_path = os.path.dirname(os.path.realpath(__file__))
	data_root_path = dir_path + '/EmpiricalData'
	if not os.path.exists(data_root_path):
		os.makedirs(data_root_path)

	Data = EmpiricalData(data_root_path + '/db.json', True) #clears any existing data and recreates the full set

	i = 0
	while True:
		try:
			Data.insert_data_point(i, extract_coinbase_data(i))
			i += 1
		except(bitcoinrpc.authproxy.JSONRPCException): #block height out of range
			return

#Identifiable string segments used by each pool:
Pools = {"BTC.com": "BTC.COM", 
		 "F2Pool": "🐟 Mined " , 
		 "AntPool": "AntPool",
		 "BW Pool": "BW.COM", 
		 "BitClub": "BitClub", 
		 "BTC.top": "BTC.TOP", 
		 "ViaBTC": "ViaBTC", 
		 "Canoe": "canoepool", 
		 "Slush Pool": "slush", 
		 "BTCC": "BTCC", 
		 "BitFury": "Bitfury", 
		 "Dpool": "DPOOL.TOP", 
		 "58coin": "58coin.com/" , 
		 "Kano CKPool": "KanoPool" , 
		 "HaoPool": None,
		 "BitcoinIndia": None ,
		 "1Hash": None,
		 "GBMiners": None,
		 "ConnectBTC": None, 
		 "Bitcoin.com": None, 
		 "Other": None }

# TO DO: scrape the coinbase_tx_data_db for instances of the above to generate an approximate historical distribution of blocks mined by each pool. 