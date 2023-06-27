import random
from constants import L, MARKER_DEATH
from math import ceil, pi

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

		self.phase = "C"  # {"Cancer", "Home"}
		self.mode = "E"  # {"E", "D", "P", "S"} = {"Explore", "Deliver Drug", "Propagate", "Stationary"}
		self.ct = 0
		self.found_tumor = False
		self.prev = ("S", False)


		self.phaseswitch_ct = 0

		self.found_tumor = False
		self.found_home = False



		expected_runtime = 50000
		BEAC_RAD = 5

		self.tumor_markers = ceil( .5 * (expected_runtime / MARKER_DEATH) * ceil(pi * BEAC_RAD**2) )
		self.home_markers = ceil( .5 * (expected_runtime / MARKER_DEATH) * ceil(pi * BEAC_RAD**2) )


		# self.found_tumor = False
		# self.load = 100
