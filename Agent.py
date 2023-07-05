from AgentState import AgentState
from constants import *
import copy
from random import random


class Agent:

	def __init__(self, agent_id, type, vertex, claw_markers=set(), receptor_markers=set(), payload=None):
		self.location = vertex
		self.type = type
		if type == "S":
			claw_markers = {"m_ca"}
			receptor_markers = {"m_sc"}
			payload = "m_sc"
		else:
			claw_markers = {"m_sc"}
			payload = "chemo"
		self.state = AgentState(agent_id, type, vertex, claw_markers, receptor_markers, payload)


	def generate_transition(self, local_vertex_mapping):
		new_agent_state = copy.copy(self.state)
		new_agent_state.ct += 1

		if new_agent_state.bound:
			new_dir = "S"
		else:
			if new_agent_state.ct >= BOT_LIFESPAN:
				new_agent_state.bound = True
				new_dir = "S"
				self.location.state.chemicals[new_agent_state.payload] += 1
			elif new_agent_state.ct >= SCOUT_TIME:
				new_dir = "R"
				bound_tmp = False

				for cell in self.location.cells:
					if not bound_tmp:
						for m in new_agent_state.claw_markers:
							if m in cell.state.receptors and new_agent_state.claws[m] == -1 and random() <= P1:
								if cell.state.receptors[m] < GAMMA:
									new_dir = "S"
									cell.state.receptors[m] += 1
									new_agent_state.claws[m] = cell.id
									new_agent_state.bound = True
									self.location.state.chemicals[new_agent_state.payload] += 1
									bound_tmp = True
									break

				if not bound_tmp:
					for a in self.location.agents:
						if not bound_tmp:
							for m in new_agent_state.claw_markers:
								if m in a.state.receptors and new_agent_state.claws[m] == -1 and random() <= P2(self.location.state.chemicals[m]):
									if a.state.receptors[m] < 1:
										new_dir = "S"
										a.state.receptors[m] += 1
										new_agent_state.claws[m] = cell.id
										new_agent_state.bound = True
										self.location.state.chemicals[new_agent_state.payload] += 1
										bound_tmp = True
										break
			else:
				new_dir = "S"

		return self.location.state, new_agent_state, new_dir
