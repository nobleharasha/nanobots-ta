from constants import *

class AgentState:

	def __init__(self, agent_id, type, vertex, claw_markers=set(), receptor_markers=set(), payload=None):
		self.reset(agent_id, type, vertex, claw_markers, receptor_markers, payload)


	def reset(self, agent_id, type, vertex, claw_markers=set(), receptor_markers=set(), payload=None):
		self.id = agent_id

		self.claw_markers = claw_markers
		self.claws = {}
		for m in claw_markers:
			self.claws[m] = -1

		self.receptor_markers = receptor_markers
		self.receptors = {}
		for m in receptor_markers:
			self.receptors[m] = 0

		self.payload = payload

		self.bound = False

		self.type = type

		if type == "S":
			self.ct = SCOUT_TIME
		else:
			self.ct = 0
