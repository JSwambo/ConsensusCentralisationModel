import random

class Miner():
	def __init__(self, ID):
		self.ID = ID
		self.pool = None
		self.gen_risk_preferences()
		assert (self.p_join + self.p_create + self.p_dn + self.p_switch) == 1

		self.compute_hash_power()

		### Additional attributes to ignore for now
		# Initialisation cost - computed based on (discretely) sampled hash power
		# Running cost - assume fixed rate in simple model


	def gen_risk_preferences(self):
		risk_preferences = ["seeking", "neutral", "averse"]
		pref = random.choice(risk_preferences)

		if pref == "seeking":
			self.p_join = 0.
			self.p_create = 0.
			self.p_dn = 0.95
			self.p_switch = 0.05

		if pref == "neutral":
			self.p_join = 0.25
			self.p_create = 0.2
			self.p_dn = 0.5
			self.p_switch = 0.05
	
		if pref == "averse":
			self.p_join = 0.5
			self.p_create = 0.45
			self.p_dn = 0.
			self.p_switch = 0.05

	def get_action(self):
		r = random.uniform(0,1)
		
		if r <= self.p_join:
			return "join"

		elif self.p_join < r <= self.p_join + self.p_create:
			return "create"

		elif self.p_join + self.p_create < r <= self.p_join + self.p_create + self.p_dn:
			return "dn"

		elif self.p_join + self.p_create + self.p_dn < r <= 1:
			return "switch"


	def compute_hash_power(self):
		"""
		Simple model - assume constant, homogeneous hash power

		Future iterations of model - Sample a distribution that has a reasonable form 
			(something like an exponential decay multiplied by a step function - where 
			the step occurs at the computing power of the typical ASIC.
		"""
		self.hash_power = 1



