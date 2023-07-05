from Agent import Agent
from Vertex import Vertex
from Cell import Cell
from geo_utils import *
from res_utils import *
from constants import *
from random import randint, random




class Configuration:

	def __init__(self, N, M, torus=False):
		# Create all vertices
		self.vertices = {}
		for x in range(M):
			for y in range(N):
				self.vertices[(x, y)] = Vertex(x,y)
		self.torus = torus
		self.N = N
		self.M = M
		self.influence_radius = INFLUENCE_RADIUS
		self.agents = {}  # map from id to agent itself
		self.cells = {}  # map from id to cell itself



	def add_agents(self, agent_locations, agent_types):
		for agent_id in range(len(agent_locations)):
			location = self.vertices[agent_locations[agent_id]]
			agent = Agent(agent_id, agent_types[agent_id], location)
			self.agents[agent_id] = agent
			location.agents.add(agent)



	def add_cells(self):
		id = 0
		for v in self.vertices:
			vertex = self.vertices[v]
			num_cells = randint(CELLS_PER_LOC[0], CELLS_PER_LOC[1]+1)
			for _ in range(num_cells):
				cell = Cell(id, vertex)
				self.cells[id] = cell
				vertex.cells.add(cell)
				id += 1



	def generate_global_transitory(self):
		# Break down into local configurations and generate local transitory configurations for each to create global one
		global_transitory = {}

		for x in range(self.M):
			for y in range(self.N):
				# Get mapping from local coordinates to each neighboring vertex
				local_vertex_mapping = generate_local_mapping(self.vertices[(x,y)], self.influence_radius, self.vertices)

				global_transitory[(x,y)] = self.delta(local_vertex_mapping)

		return global_transitory



	def delta(self, local_vertex_mapping):
		vertex = local_vertex_mapping[(0,0)]

		if len(vertex.agents) == 0:
			return vertex.state, {}

		# Phase One: Each vertex uses their own transition function to propose a new
		# vertex state, agent state, and direction of motion
		proposed_vertex_states = {}
		proposed_agent_updates = {}

		for agent in vertex.agents:
			proposed_vertex_state, proposed_agent_state, direction = agent.generate_transition(local_vertex_mapping)

			proposed_vertex_states[agent.state.id] = proposed_vertex_state
			proposed_agent_updates[agent.state.id] = AgentTransition(proposed_agent_state, direction)

		# Phase Two: Use a resolution rule to handle conflicting proposed vertex states
		new_vertex_state, new_agent_updates = receptor_claiming_resolution(proposed_vertex_states, proposed_agent_updates, vertex)
		return new_vertex_state, new_agent_updates



	def execute_transition(self,global_transitory):
		for x,y in global_transitory.keys():
			vertex = self.vertices[(x,y)]
			new_vertex_state, new_agent_updates = global_transitory[(x,y)]

			# Update vertex state
			vertex.state = new_vertex_state

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



	def transition(self):
		global_transitory = self.generate_global_transitory()
		self.execute_transition(global_transitory)
