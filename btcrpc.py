# -*- coding: utf-8 -*-
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import numpy as np
import pandas as pd
import re


class CoinbaseTxData(object):
    def __init__(self):
        # rpc_user and rpc_password are set in the bitcoin.conf file
        rpc_user = "jacob"
        rpc_password = "j5wDEJTZ_3xia_O_CxGlIHqUuvrqBAeH_ove3Fow57I="
        self.rpc_connection = AuthServiceProxy(
            "http://%s:%s@127.0.0.1:8332" % (rpc_user, rpc_password))

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.data_root_path = dir_path + '/EmpiricalData'
        if not os.path.exists(self.data_root_path):
            os.makedirs(self.data_root_path)

    def extract_coinbase_data(self, block_height):

        block_hash = self.rpc_connection.getblockhash(block_height)
        block = self.rpc_connection.getblock(block_hash)
        txs = block["tx"]

        if block_height > 0:
            raw_coinbase_tx = self.rpc_connection.getrawtransaction(txs[0])
            coinbase_tx = self.rpc_connection.decoderawtransaction(
                raw_coinbase_tx)

        # coinbase_tx for genesis block is not retrievable via rpc
        elif block_height == 0:
            coinbase_tx = {
                "txid": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
                "version": 1,
                "locktime": 0,
                "vin": [
                        {
                            "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73",
                            "sequence": 4294967295
                        }
                ],
                "vout": [
                    {
                        "value": 50.00000000,
                        "n": 0,
                        "scriptPubKey": {
                            "asm": "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f OP_CHECKSIG",
                            "hex": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac",
                            "reqSigs": 1,
                            "type": "pubkey",
                            "addresses": [
                                    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
                            ]
                        }
                    }
                ]
            }

        return coinbase_tx["vin"][0]["coinbase"].decode("hex")

    def save_coinbase_tx_data(self):

        # initialise data structure for coinbase transaction data storage
        max_block_height = self.rpc_connection.getblockcount()
        coinbase_data = np.zeros((2, max_block_height))

        for i in range(max_block_height):
            coinbase_data[0][i] = i
            coinbase_data[1][i] = self.extract_coinbase_data(i)

        df = pd.DataFrame(coinbase_data)
        df.to_csv(self.data_root_path + "/coinbase_tx_data.txt")

    def load_coinbase_tx_data(self):

        self.df = pd.read_csv(self.data_root_path + "/coinbase_tx_data.txt")

    def scrape_db_for_matches(self, pool_strings):

        # match = re.search(pattern, string)
        # if match:
                # process(match)


        # Identifiable string segments used by each pool:
POOLS = {"BTC.com": "BTC.COM",
         "F2Pool": "🐟 Mined ",
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
                 "58coin": "58coin.com/",
                 "Kano CKPool": "KanoPool",
                 "HaoPool": None,
                 "BitcoinIndia": None,
                 "1Hash": None,
                 "GBMiners": None,
                 "ConnectBTC": None,
                 "Bitcoin.com": None,
                 "Other": None}
