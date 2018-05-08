import random
from miner import Miner
from db import SimData
import os

class Simulator():
	def __init__(self):
		self.NUM_MINERS = 50
		self.T = 300

		self.M = self.init_miner_set(self.NUM_MINERS)	# Miner Set
		self.P = []										# Pool Set

		dir_path = os.path.dirname(os.path.realpath(__file__))
		sim_root_path = dir_path + '/SimData'
		if not os.path.exists(sim_root_path):
			os.makedirs(sim_root_path)

		self.SimData = SimData(sim_root_path + '/db.json', True)

	def init_miner_set(self, N):
		""" 
		N - number of miners
		"""
		return [Miner(ID = i) for i in range(0,N)]

	def create_pool(self, miner):
		"""
		i - miner ID that is creating a pool
		"""
		self.P.append([miner])
		miner.not_pooled = False

	def join_pool(self, miner):
		"""
		i - miner ID that is joining a pool
		"""
		if self.P == []:
			return

		else: 
			#Unpack all subsets in P and randomly select a miner with which to join.
			#This weights the choice according to a preferential attachment rule.
			dist = []
			for pool in self.P:
				for member in pool:
					dist.append(member)

			selected_pool_member = random.choice(dist)

			#Add new miner to the selected pool.
			for pool in self.P:
				if selected_pool_member in pool:
					pool.append(miner)
					miner.not_pooled = False

	def assign_actions(self):
		A = [] 						# Action Set
		for miner in self.M:		#Only Not Pooled Miners will act
			if miner.not_pooled == True:
				A.append([miner, miner.get_action()])
		return A		

	def simulate_time_step(self):
		"""
		Order of events: Create all pools to be created, then join pools where appropriate.
		"""
		A = self.assign_actions()
		#print "Action Set: ", A, "\n" 
		for [miner, action] in A:
			if action == "create":
				self.create_pool(miner)

		for [miner, action] in A:
			if action == "join":
				self.join_pool(miner)

	def test_run(self):
		print "Miner Set:", self.M, "\n"

		print "Pool Set:", self.P, "\n"

		self.simulate_time_step()

		print "New Pool Set:", self.P, "\n"

	def get_pool_set_IDs(self):
		P = []
		for pool in self.P:
			P.append([member.ID for member in pool])
		return P

	def full_sim(self, save_pool_set = True):

		for t in range(0, self.T):

			self.simulate_time_step()

			print self.SimData.get_sim_length()

			if save_pool_set == True:
				pool_IDs = self.get_pool_set_IDs()
				self.SimData.insert_data_point(t, pool_IDs)


Sim = Simulator()
Sim.full_sim()
