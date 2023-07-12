import random
from constants import L

class AgentState:

	def __init__(self, agent_id, vertex, l=L):
		self.reset(agent_id, vertex, l)

	def reset(self, agent_id, vertex, l):
		# Initial parameters
		self.id = agent_id





		self.L = l

		# Levy parameters
		self.angle = 0
		self.starting_point = (vertex.x, vertex.y)
		self.travel_distance = 0
		self.levy_cap = 1/l




		self.mode = "E"  # {"E", "D", "P", "S"} = {"Explore", "Deliver Drug", "Propagate", "Stationary"}
		self.ct = 0
		#self.prop_time = 0
		self.prev = ("S", False)


		# self.found_tumor = False
		# self.load = 100

		self.curr_dir = random.choice(["U", "D", "L", "R"])

		self.one_stepped = False

		self.bound = False
