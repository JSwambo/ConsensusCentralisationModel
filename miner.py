import random

class Miner():
	def __init__(self, ID):
		self.ID = ID
		self.not_pooled = True
		self.gen_risk_preferences()
		assert (self.p_join + self.p_create + self.p_dn) == 1

	def gen_risk_preferences(self):
		risk_preferences = ["seeking", "neutral", "averse"]
		pref = random.choice(risk_preferences)

		if pref == "seeking":
			self.p_join = 0.
			self.p_create = 0.
			self.p_dn = 1.

		if pref == "neutral":
			self.p_join = 0.25
			self.p_create = 0.25
			self.p_dn = 0.5
	
		if pref == "averse":
			self.p_join = 0.5
			self.p_create = 0.5
			self.p_dn = 0.

	def get_action(self):
		r = random.uniform(0,1)
		
		if r <= self.p_join:
			return "join"

		elif self.p_join < r <= self.p_join + self.p_create:
			return "create"

		elif self.p_join + self.p_create < r <= 1:
			return "dn"


