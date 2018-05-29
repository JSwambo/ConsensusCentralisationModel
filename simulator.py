import random
from numpy.random import poisson
from miner import Miner
from pool import Pool
import os
import numpy as np
import pandas as pd


class Simulator():
    def __init__(self, num_miners, T):
        self.NUM_MINERS = num_miners
        self.T = T

        self.M = self.init_miner_set(self.NUM_MINERS)  # Miner Set
        self.P = []										# Pool Set

        self.new_miner_rate = 3

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.sim_root_path = dir_path + '/SimData'
        if not os.path.exists(self.sim_root_path):
            os.makedirs(self.sim_root_path)
        # self.sim_root_path = "/home/k1768289/Desktop/Research/Modeling/ConsensusCentralisationModel/SimData"

    def init_miner_set(self, N):
        """ 
        N - number of miners
        """
        return set({Miner(ID=i) for i in range(0, N)})

    def new_miners_join(self):
        """
        Arrival process is modeled as a poisson process, with mean arrival set to 3 miners per block/round. 
        The long term growth of the network is steady under this model.
        """
        num_new_miners = poisson(self.new_miner_rate)
        len_miner_set = len(self.M)
        for i in range(len_miner_set, len_miner_set + num_new_miners):
            self.M.add(Miner(ID=i))

    def create_pool(self, miner):
        """
        miner - instance of Miner that is creating a pool
        """
        assert isinstance(miner, Miner)

        miner.pool = Pool(miner)
        self.P.append(miner.pool)

    def join_pool(self, miner):
        """
        miner - instance of Miner that is creating a pool
        """
        assert isinstance(miner, Miner)

        if self.P == []:
            return

        else:
            # Unpack all subsets in P and randomly select a miner with which to join.
            # This weights the choice according to a preferential attachment rule.
            dist = set({})
            for pool in self.P:
                dist = dist.union(pool.members)

            selected_pool_member = random.choice([i for i in dist])

            # Update miner's pool attribute
            miner.pool = selected_pool_member.pool

            # Add miner to pool
            miner.pool.add_member(miner)

    def switch_pool(self, miner):
        """
        If miner is not in a pool, then action defaults to doing nothing.
        If there are  no pools, then action defaults to doing nothing.
        Pool switching is based on preferential attachment.
        """
        assert isinstance(miner, Miner)

        if not miner.pool:
            return

        if self.P == []:
            return

        else:
            # Unpack all subsets in P and randomly select a miner with which to join.
            # This weights the choice according to a preferential attachment rule.
            dist = set({})
            for pool in self.P:
                dist = dist.union(pool.members)

            selected_pool_member = random.choice(dist)

            # Remove miner from current pool
            miner.pool.remove_member(miner)

            # Update miner's pool attribute
            miner.pool = selected_pool_member.pool

            # Add miner to pool
            miner.pool.add_member(miner)

    def assign_actions(self):
        A = [] 						# Action Set
        for miner in self.M:		# Only Not Pooled Miners will act
            if not miner.pool:
                A.append([miner, miner.get_action()])
        return A

    def simulate_time_step(self):
        """
        Order of events: New miners join the network, create all pools to be created, miners join pools and then switch pools where appropriate.
        """
        self.new_miners_join()
        A = self.assign_actions()

        for [miner, action] in A:
            if action == "create":
                self.create_pool(miner)

        for [miner, action] in A:
            if action == "join":
                self.join_pool(miner)

        for [miner, action] in A:
            if action == "switch":
                self.switch_pool(miner)

    def test_run(self):
        print "Miner Set:", self.M, "\n"

        print "Pool Set:", self.P, "\n"

        self.simulate_time_step()

        print "New Pool Set:", self.P, "\n"

    def get_pool_size_distribution(self):

        sizes = [len(pool.members) for pool in self.P]

        distribution = np.zeros((1, max(sizes)))

        for item in sizes:
            distribution[0][item - 1] += 1

        return distribution

    def full_sim(self, save_size_distributions=True):

        if save_size_distributions == True:
            # Define an upper bound which is greater than the largest pool size at the end of the simulation
            upper_bound = len(self.M) + self.T * self.new_miner_rate
            size_distribution_series = np.zeros((self.T, upper_bound))

        for t in range(0, self.T):

            self.simulate_time_step()

            print t

            if save_size_distributions == True:
                dist = self.get_pool_size_distribution()
                for i in range(len(dist)):
                    size_distribution_series[t][i] = dist[0][i]

        if save_size_distributions:
            df = pd.DataFrame(size_distribution_series)
            df.to_csv(self.sim_root_path +
                      "/size_distribution_series_T-%d_M-%d.txt" % (self.T, len(self.M)))


if __name__ == '__main__':

    # Sim = Simulator(M=50, T=50)
    # Sim.test_run()
    # Sim.full_sim()
