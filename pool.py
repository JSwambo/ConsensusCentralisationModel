from miner import Miner

class Pool():
	def __init__(self, creator):
		assert isinstance(creator, Miner)
		self.ID = creator.ID
		self.members = [creator]

	def get_net_hash_power(self):
		return sum([miner.hash_power for  miner in self.members])

	def get_size(self):
		return len(self.members)

	def get_membership_cost(self):
		# Assume the cost is a small fee of Bitcoin with a nominal value
		# sampled from an appropriate distributtion
		pass

	def add_member(self, Miner):
		self.members.append(Miner)

	def remove_member(self, Miner):
		self.members.remove(Miner)


