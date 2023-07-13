import multiprocessing as mp
from Agent import Agent
from Vertex import Vertex
from geo_utils import generate_local_mapping, get_coords_from_movement, signal_amt, within_bounds, dir_to_dxdy, l2_distance
from res_utils import *
from constants import INFLUENCE_RADIUS, p_m_markers, M, N
import time
from random import random, choice

"""
Given a local vertex mapping, generate a proposed new vertex state and
new agent states and directions for each agent in that vertex

Parameters
local_vertex_mapping: dict
	mapping from local coordinates to the vertices at those coordiantes
"""
def delta(params):
	local_vertex_mapping, x, y = params
	print(x,y)
	vertex = local_vertex_mapping[(0,0)]

	if len(vertex.agents) == 0:
		return x, y, vertex.state, {}

	# Phase One: Each vertex uses their own transition function to propose a new
	# vertex state, agent state, and direction of motion
	proposed_vertex_states = {}
	proposed_agent_updates = {}

	for agent in vertex.agents:
		proposed_vertex_state, proposed_agent_state, direction = agent.generate_transition(local_vertex_mapping)

		proposed_vertex_states[agent.state.id] = proposed_vertex_state
		proposed_agent_updates[agent.state.id] = AgentTransition(proposed_agent_state, direction)


	# Phase Two: Use a resolution rule to handle conflicting proposed vertex states
	new_vertex_state, new_agent_updates = naive_resolution(proposed_vertex_states, proposed_agent_updates)

	# Need x and y for setting the global state for parallel processing
	return x, y, new_vertex_state, new_agent_updates

class Configuration:
	"""
	Initialize the configuration

	Parameters
	agent_locations: list
		list of integers specifying what vertex to initialize each agent in
	N: int
		the height of the configuration
	M: int
		the width of the configuration
	torus: bool
		True if the grid is a torus, False if we are considering
		edge effects
	"""
	def __init__(self, N, M, P, torus=False, pool = None):
		# Create all vertices
		self.vertices = {}
		for x in range(M):
			for y in range(N):
				self.vertices[(x, y)] = Vertex(x,y)
		self.torus = torus
		self.N = N
		self.M = M
		self.influence_radius = INFLUENCE_RADIUS # make this a class variable later; radius 0 means only self is influenced
		self.agents = {} # map from id to agent itself
		self.drug_visits_peragent = {}
		self.pool = pool

		self.P = P


	def add_agents(self, agent_locations):

		for agent_id in range(len(agent_locations)):
			location = self.vertices[agent_locations[agent_id]]
			agent = Agent(agent_id, location)
			# while agent_id in self.agents:
			# 	agent_id += 1
			self.agents[agent_id] = agent
			self.drug_visits_peragent[agent_id] = 0
			location.agents.add(agent)

	def reset_agent_locations(self, agent_locations):
		for x in range(self.M):
			for y in range(self.N):
				self.vertices[(x, y)].agents = set()
		for agent_id in range(len(agent_locations)):
			agent = self.agents[agent_id]
			vertex = self.vertices[agent_locations[agent_id]]
			vertex.agents.add(agent)
			agent.location = vertex
	"""
	Generates a global transitory state for the entire configuration
	"""
	def generate_global_transitory(self):
		# Break down into local configurations and generate local transitory configurations for each to create global one
		global_transitory = {}

		for x in range(self.M):
			for y in range(self.N):

				#Get mapping from local coordinates to each neighboring vertex
				local_vertex_mapping = generate_local_mapping(self.vertices[(x,y)], self.influence_radius, self.vertices)

				global_transitory[(x,y)] = self.delta(local_vertex_mapping)

		return global_transitory

	"""
	Given a local vertex mapping, generate a proposed new vertex state and
	new agent states and directions for each agent in that vertex

	Parameters
	local_vertex_mapping: dict
		mapping from local coordinates to the vertices at those coordiantes
	"""
	def delta(self, local_vertex_mapping):
		vertex = local_vertex_mapping[(0,0)]

		if len(vertex.agents) == 0:
			return vertex.state, {}

		# Phase One: Each vertex uses their own transition function to propose a new
		# vertex state, agent state, and direction of motion
		proposed_vertex_states = {}
		proposed_agent_updates = {}

		# global_beacon_locations = set()
		# for x in range(0, self.M):
		# 	for y in range(0, self.N):
		# 		for a in self.vertices[(x,y)].agents:
		# 			if a.state.mode == "S":
		# 				global_beacon_locations.add((x,y))

		for agent in vertex.agents:
			proposed_vertex_state, proposed_agent_state, direction = agent.generate_transition(local_vertex_mapping, self.P)

			proposed_vertex_states[agent.state.id] = proposed_vertex_state
			proposed_agent_updates[agent.state.id] = AgentTransition(proposed_agent_state, direction)



		# Phase Two: Use a resolution rule to handle conflicting proposed vertex states
		new_vertex_state, new_agent_updates = task_claiming_resolution(proposed_vertex_states, proposed_agent_updates, vertex)
		return new_vertex_state, new_agent_updates

	"""
	Given the global transitory configuration, update the configuration to the new
	global state
	"""
	def execute_transition(self,global_transitory):
		# beacon_locs = set()
		# for x in range(0, self.M):
		# 	for y in range(0, self.N):
		# 		for a in self.vertices[(x,y)].agents:
		# 			if a.state.mode == "S":
		# 				beacon_locs.add((x,y))

		for x,y in global_transitory.keys():
			vertex = self.vertices[(x,y)]
			new_vertex_state, new_agent_updates = global_transitory[(x,y)]

			# Update vertex state
			vertex.state = new_vertex_state

			if self.vertices[(int(M / 2), int(N / 2))].state.num_bound > 0:
				vertex.state.fuel = max(0, round(-1 * ( l2_distance(int(M / 2), int(N / 2), x, y)**2 / (0.5 * self.vertices[(int(M / 2), int(N / 2))].state.num_bound) ) + (0.5 * self.vertices[(int(M / 2), int(N / 2))].state.num_bound) ))


			# signal = 0
			# for beac_loc in beacon_locs:
			# 	signal += signal_amt((x,y), beac_loc)
			# vertex.state.sig = signal


			# if random() <= p_m_markers and vertex.state.markers > 0:
			# 	vertex.state.markers = max(0, vertex.state.markers - .5)
			# 	dirs = []
			# 	for dir in ["S", "U", "D", "L", "R"]:
			# 		new_x, new_y = vertex.coords()[0] + dir_to_dxdy[dir][0], vertex.coords()[1] + dir_to_dxdy[dir][1]
			# 		if within_bounds(new_x, new_y):
			# 			dirs.append(dir)
			# 	new_dir = choice(dirs)
			# 	new_x, new_y = vertex.coords()[0] + dir_to_dxdy[new_dir][0], vertex.coords()[1] + dir_to_dxdy[new_dir][1]
			# 	self.vertices[(new_x, new_y)].state.markers += .5


			# Update agents
			for agent_id in new_agent_updates:
				agent = self.agents[agent_id]
				update = new_agent_updates[agent_id]
				if update != None:
					# Update agent state
					agent.state = update.state

					# Update agent location
					movement_dir = update.direction

					# Erase agent from current location
					vertex.agents.remove(agent)

					# Move agent according to direction
					new_coords = get_coords_from_movement(vertex.x, vertex.y, movement_dir)
					agent.location = self.vertices[new_coords]

					# Add agent to updated location
					agent.location.agents.add(agent)

	"""
	Transition from the current global state into the next one
	"""
	def transition(self):
		global_transitory = self.generate_global_transitory()
		self.execute_transition(global_transitory)

	def all_agents_terminated(self):
		for agent_id in self.agents:
			if not self.agents[agent_id].terminated:
				return False
		return True
