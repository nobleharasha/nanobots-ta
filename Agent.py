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
		# curr_loc = self.location.coords()
		# dirs = []
		# for dir in ['S', 'U', 'D', 'L', 'R']:
		# 	new_loc = (curr_loc[0] + dir_to_dxdy[dir][0], curr_loc[1] + dir_to_dxdy[dir][1])
		# 	if within_bounds(new_loc[0], new_loc[1]):
		# 		dirs.append(dir)

		dirs = ['S', 'U', 'D', 'L', 'R']
		return random.choice(dirs)



	def generate_transition(self, local_vertex_mapping, P):
		new_agent_state = copy.copy(self.state)
		new_agent_state.ct += 1



		if new_agent_state.ct >= 2**(new_agent_state.phaseswitch_ct):
			if new_agent_state.phase == "C":
				new_agent_state.phase = "H"
			else:
				new_agent_state.phase = "C"
				new_agent_state.found_tumor = False
			new_agent_state.phaseswitch_ct += 1
			new_agent_state.ct = 0
			new_agent_state.prev = ("S", True)
			return self.location.state, new_agent_state, "S"

		if new_agent_state.mode == "D":
			new_agent_state.ct = 0
			new_agent_state.mode = "E"
			new_dir = "S"
			mark = True
		else:
			if new_agent_state.phase == "C":
				mark = self.location.state.tumor_marker
				if self.location.state.is_task:
					new_agent_state.mode = "D"
					new_dir = "S"
					new_agent_state.found_tumor = True
					new_agent_state.phase = "H"
					new_agent_state.ct = 0
					new_agent_state.phaseswitch_ct += 1
					new_agent_state.prev = ("S", True)
				elif not mark and new_agent_state.prev[1]:
					new_dir = dir_to_opp[new_agent_state.prev[0]]
				else:
					new_dir = self.random_rw()
			else:
				mark = True
				if new_agent_state.found_tumor:
					self.location.state.tumor_marker = True
				if self.location.state.is_home:
					new_dir = "S"
					new_agent_state.found_tumor = False
					new_agent_state.phase = "C"
					new_agent_state.ct = 0
					new_agent_state.phaseswitch_ct += 1
					new_agent_state.prev = ("S", True)
				else:
					new_dir = get_direction_from_destination((25, 25), self.location.coords())

		new_agent_state.prev = (new_dir, mark)
		return self.location.state, new_agent_state, new_dir





		# if self.type == "W":
		# 	if new_agent_state.mode == "S":
		# 		new_dir = "S"
		# 		mark = True
		# 		if new_agent_state.ct >= 5000:
		# 			new_agent_state.mode = "E"
		# 	elif new_agent_state.mode == "D":
		# 		new_dir = "S"
		# 		mark = True
		# 	else:
		# 		mark = self.location.state.tumor_marker
		# 		if self.location.state.is_task:
		# 			new_agent_state.mode = "D"
		# 			new_dir = "S"
		# 		else:
		# 			if not mark and new_agent_state.prev[1]:
		# 				new_dir = dir_to_opp[new_agent_state.prev[0]]
		# 			else:
		# 				new_dir = self.random_rw()
		# else:
		#
		# 	#if new_agent_state.ct >= 2**(new_agent_state.phaseswitch_ct):
		# 	if new_agent_state.ct >= 500:
		# 		if new_agent_state.phase == "C":
		# 			new_agent_state.phase = "H"
		# 			new_agent_state.found_home = False
		# 		else:
		# 			new_agent_state.phase = "C"
		# 			new_agent_state.found_tumor = False
		# 		new_agent_state.phaseswitch_ct += 1
		# 		new_agent_state.ct = 0
		# 		new_agent_state.prev = ("S", True)
		# 		return self.location.state, new_agent_state, "S"
		#
		# 	if new_agent_state.phase == "C":
		# 		mark = self.location.state.tumor_marker
		# 		#if new_agent_state.found_home and new_agent_state.home_markers > 0:
		# 		# if new_agent_state.found_home:
		# 		# 	self.location.state.home_marker = True
		# 		# 	self.location.state.home_marker_age = 0
		# 		# 	new_agent_state.home_markers -= 1
		# 		if self.location.state.is_task:
		# 			# new_agent_state.mode = "D"
		# 			new_dir = "S"
		# 			new_agent_state.found_tumor = True
		# 			new_agent_state.phase = "H"
		# 			new_agent_state.ct = 0
		# 			new_agent_state.phaseswitch_ct += 1
		# 			new_agent_state.prev = ("S", True)
		# 			return self.location.state, new_agent_state, new_dir
		# 		else:
		# 			if not mark and new_agent_state.prev[1]:
		# 				new_dir = dir_to_opp[new_agent_state.prev[0]]
		# 			else:
		# 				new_dir = self.random_rw()
		# 				if new_agent_state.found_home:
		# 					self.location.state.home_marker = True
		# 					self.location.state.home_marker_age = 0
		# 					new_agent_state.home_markers -= 1
		# 	else:
		# 		mark = self.location.state.home_marker
		# 		#if new_agent_state.found_tumor and new_agent_state.tumor_markers > 0:
		# 		# if new_agent_state.found_tumor:
		# 		# 	self.location.state.tumor_marker = True
		# 		# 	self.location.state.tumor_marker_age = 0
		# 		# 	new_agent_state.tumor_markers -= 1
		#
		#
		# 		# if self.location.state.is_task:
		# 		# 	new_agent_state.mode = "D"
		#
		# 		if self.location.state.is_home:
		# 			new_dir = "S"
		# 			new_agent_state.found_home = True
		# 			new_agent_state.phase = "C"
		# 			new_agent_state.ct = 0
		# 			new_agent_state.phaseswitch_ct += 1
		# 			new_agent_state.prev = ("S", True)
		# 			return self.location.state, new_agent_state, new_dir
		# 		else:
		# 			if not mark and new_agent_state.prev[1]:
		# 				new_dir = dir_to_opp[new_agent_state.prev[0]]
		# 			else:
		# 				new_dir = self.random_rw()
		# 				if new_agent_state.found_tumor:
		# 					self.location.state.tumor_marker = True
		# 					self.location.state.tumor_marker_age = 0
		# 					new_agent_state.tumor_markers -= 1
		#
		# new_agent_state.prev = (new_dir, mark)
		# return self.location.state, new_agent_state, new_dir
