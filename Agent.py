from AgentState import AgentState
from geo_utils import *
import random
from math import pi, floor
from constants import *
from scipy.interpolate import interp1d
from scipy.stats import levy
import copy
from Vertex import *

class Agent:
	def __init__(self,agent_id, vertex, l=L):
		self.location = vertex
		# self.type = type
		self.state = AgentState(agent_id, vertex, l)

	def find_nearby_task(self,local_vertex_mapping):
		ret = None
		min_dist = 10000000000
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			if vertex.state.is_task and vertex.state.residual_demand > 0:
				this_dist = l2_distance(self.location.x, self.location.y, self.location.x+dx, self.location.y+dy)
				if  this_dist < min_dist:
					min_dist = this_dist
					ret = vertex.state
		return ret

	def within_site(self, x, y, site):
		if site == None:
			x_range = (0, M-1)
			y_range = (0, N-1)

		if x >= x_range[0] and x <= x_range[1] and y >= y_range[0] and y <= y_range[1]:
			return True
		return False


	def get_travel_direction(self, new_agent_state):
		if self.state.travel_distance == 0:
			new_agent_state.travel_distance = int(min(self.state.levy_cap, levy.rvs(loc=levy_loc))) #Twice the distance to the nest? maybe make this a variable
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)

		new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
		new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)

		bounding_site = None

		while not self.within_site(new_location[0], new_location[1], bounding_site):
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)
			new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
			new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)
		new_agent_state.travel_distance = new_agent_state.travel_distance-1
		return new_direction


	def random_rw(self):
		curr_loc = self.location.coords()
		dirs = []
		for dir in ['S', 'U', 'D', 'L', 'R']:
			new_loc = (curr_loc[0] + dir_to_dxdy[dir][0], curr_loc[1] + dir_to_dxdy[dir][1])
			if within_bounds(new_loc[0], new_loc[1]):
				dirs.append(dir)
		return random.choice(dirs)



	def generate_transition(self, local_vertex_mapping, P):
		# new_agent_state = copy.copy(self.state)
		# new_agent_state.ct += 1
		# if self.type == "C":
		# 	mark = self.location.state.h_f
		# 	if self.location.state.is_task:
		# 		new_agent_state.found_tumor = True
		# 	if new_agent_state.found_tumor:
		# 		# if mark <= 0 and new_agent_state.prev[1] > 0:
		# 		# 	new_dir = dir_to_opp[new_agent_state.prev[0]]
		# 		if mark > new_agent_state.prev[1]:
		# 			new_dir = new_agent_state.prev[0]
		# 		else:
		# 			new_dir = self.random_rw()
		# 	else:
		# 		new_dir = self.random_rw()
		# 	if new_agent_state.found_tumor and new_agent_state.load > 0:
		# 		self.location.state.c_f += 1
		# 		new_agent_state.load -= 1
		# elif self.type == "H":
		# 	mark = self.location.state.c_f
		# 	# if mark <= 0 and new_agent_state.prev[1] > 0:
		# 	# 	new_dir = dir_to_opp[new_agent_state.prev[0]]
		# 	if mark > new_agent_state.prev[1]:
		# 		new_dir = new_agent_state.prev[0]
		# 	else:
		# 		new_dir = self.random_rw()
		# 	if new_agent_state.load > 0:
		# 		self.location.state.h_f += 1
		# 		new_agent_state.load -= 1
		#
		# new_agent_state.prev = (new_dir, mark)
		# return self.location.state, new_agent_state, new_dir







		new_agent_state = copy.copy(self.state)
		new_agent_state.ct += 1
		mark = self.location.state.marker

		if new_agent_state.mode == "S":
			new_dir = "S"
		elif new_agent_state.mode == "D":
			new_dir = "S"
			if new_agent_state.ct >= T:
				new_agent_state.mode = "P"
				new_agent_state.ct = 0
		elif new_agent_state.mode == "P":
			self.location.state.marker = True
			if new_agent_state.ct >= P:
				new_dir = "S"
				new_agent_state.mode = "S"
				new_agent_state.ct = 0
			else:
				new_dir = self.random_rw()
		else:  # mode == "E"
			if self.location.state.is_task:
				new_dir = "S"
				new_agent_state.mode = "D"
				new_agent_state.ct = 0
				# new_agent_state.no_tmr_ct = 0
			else:
				# if not mark and new_agent_state.prev[1]:
				# 	new_dir = dir_to_opp[new_agent_state.prev[0]]
				# else:
				# 	new_dir = self.random_rw()

				new_dir = self.random_rw()

		new_agent_state.prev = (new_dir, mark)
		return self.location.state, new_agent_state, new_dir















		# new_agent_state.ct += 1
		#
		# sig_tmp = self.location.state.sig
		# sig_tmp = max(0, random.uniform(sig_tmp - EPSILON, sig_tmp + EPSILON))
		#
		# if new_agent_state.mode == "S":
		# 	new_dir = "S"
		# elif new_agent_state.mode == "D":
		# 	new_dir = "S"
		# 	if new_agent_state.ct >= T:
		# 		new_agent_state.mode = "P"
		# 		new_agent_state.ct = 0
		# 		new_agent_state.prop_time = random.randrange(0, M/2)
		# elif new_agent_state.mode == "P":
		# 	if new_agent_state.ct >= new_agent_state.prop_time:
		# 		new_dir = "S"
		# 		new_agent_state.mode = "S"
		# 		new_agent_state.ct = 0
		# 	else:
		# 		new_dir = self.get_travel_direction(new_agent_state)
		# else:  # mode == "E"
		# 	if self.location.state.is_task:
		# 		new_dir = "S"
		# 		new_agent_state.mode = "D"
		# 		new_agent_state.ct = 0
		# 	else:
		# 		if sig_tmp > new_agent_state.prev[1]:
		# 			new_dir = new_agent_state.prev[0]
		# 		else:
		# 			new_dir = self.get_travel_direction(new_agent_state)
		#
		# 		#new_dir = self.get_travel_direction(new_agent_state)
		#
		# if random.random() <= p_m:
		# 	dirs = []
		# 	for dxdy in local_vertex_mapping:
		# 		try:
		# 			dirs.append(dxdy_to_dir[dxdy])
		# 		except:
		# 			pass
		# 	new_dir = random.choice(dirs)
		#
		# new_agent_state.prev = (new_dir, sig_tmp)
		# return self.location.state, new_agent_state, new_dir
