from db import SimData
import os
import matplotlib.pyplot as plt
from utils import lengths


class Analysis():
	def __init__(self):
		
		dir_path = os.path.dirname(os.path.realpath(__file__))
		sim_root_path = dir_path + '/SimData'
		if not os.path.exists(sim_root_path):
			os.makedirs(sim_root_path)

		self.SimData = SimData(sim_root_path + '/db.json', new_sim = False)

	def read_historic_pool_set_data(self):

		for time in range(0, self.SimData.get_sim_length()):
			print self.SimData.search_by_time(time)

	def plot_final_pool_size_distribution(self):
		
		end_time = self.SimData.get_sim_length()
		raw_pool_data = self.SimData.search_by_time(end_time-1)
		pool_IDs = raw_pool_data['P']

		LARGEST_POOL_SIZE = max(lengths(pool_IDs))

		n_bins = LARGEST_POOL_SIZE
		counts = []

		for pool in pool_IDs:
			counts.append(len(pool))

		dis = [0 for i in range(0,LARGEST_POOL_SIZE+1)]

		for i in range(0, len(counts)):
			dis[counts[i]] += 1

		# print pool_IDs
		plt.plot(range(0,len(dis)), dis, 'o-')
		plt.show()		

	def plot_pool_size_dynamics(self):
		
		pass




A = Analysis()
# A.read_historic_pool_set_data()
# A.plot_final_pool_size_distribution()

