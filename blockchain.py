from random import random


class Blockchain():
    def __init__(self):
        pass

    def get_network_hash_rate(self, miner_set):
        """
        Returns the network hash rate by summing the individual hash rates of each miner in the network.
        """
        self.network_hash_rate = sum([miner.hash_power for miner in miner_set])
        return self.network_hash_rate

    def get_block_reward(self, block_height):
        """
        Returns the block reward based on the current block height. In this simplified model the block reward is constant.
        """
        if block_height >= 0:
            self.block_height = 50
            return self.block_height

    def get_tx_fees(self):
        """
        Returns the sum of a set of tx fees which is (if modeled appropriately) representative of typical fee distribution per block. 
        """
        tx_fees = [0.00001 for i in range(0, 100 * random())]
        self.transaction_fees = sum(tx_fees)
        return self.transaction_fees

    def get_difficulty(self):
        """
        Returns the difficulty, i.e. the target of the proof-of-work algorithm required by the next block.
        This may be used in calculating the probability of success for each miner.
        This could be used to stochastically simulate block generation with variable block times. However in the simple model the
        block time will remain constant.
        """
        self.difficulty = 4  # in units of the number of 0-bits required by a PoW hash to be verified.
        return self.difficulty

    def get_block_time(self):
        """
        Returns the block time interval between the current and next block.
        For this simple implementation of the model, the block time is constant.
        """
        self.block_time = 10  # minutes
        return self.block_time
