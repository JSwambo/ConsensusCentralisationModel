from tinydb import TinyDB, Query
import os

class SimData():
	def __init__(self, db_path, new_sim = True):

		if new_sim:
			self.clear_sim_data(db_path)
		self.db = TinyDB(db_path)

	def insert_data_point(self, time, pool_set):
		self.db.insert({'time' : time, 'P' : pool_set})

	def search_by_time(self, time):
		return self.db.get(Query().time == time)

	def get_sim_length(self):
		return len(self.db)

	def clear_sim_data(self, db_path):
		os.remove(db_path)

class EmpricialData():
	def __init__(self, db_path, new_sim = True):

		if new_sim:
			self.clear_sim_data(db_path)
		self.db = TinyDB(db_path)

	def insert_data_point(self, block_height, coinbase_tx_data):
		self.db.insert({"block": block_height, "coinbase_tx_data": coinbase_tx_data})

	def search_by_block(self, block):
		return self.db.get(Query().block == block)

	def get_data_length(self):
		return len(self.db)

	def clear_sim_data(self, db_path):
		os.remove(db_path)

