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
		# return random.choice(dirs)

		dirs = ['S', 'U', 'D', 'L', 'R']
		return random.choice(dirs)



	def generate_transition(self, local_vertex_mapping, beac_locs, new_beac):
		new_agent_state = copy.copy(self.state)
		new_agent_state.ct += 1

		# sig_tmp = self.location.state.sig
		# sig_tmp = max(0, random.uniform(sig_tmp - EPSILON, sig_tmp + EPSILON))

		sig = self.location.state.signal
		# if random.random() <= p_e:
		# 	sig = not sig

		if new_agent_state.mode == "S":
			new_dir = "S"
		elif new_agent_state.mode == "D":
			new_dir = "S"
			if new_agent_state.ct >= T:
				new_agent_state.mode = "P"
				new_agent_state.ct = 0
				# new_agent_state.prop_time = random.randrange(0, M/2)
		elif new_agent_state.mode == "P":
			# if new_agent_state.ct >= P or not sig:
			if not sig:
				new_dir = "S"
				new_agent_state.mode = "S"
				new_agent_state.ct = 0
				beac_locs.add(self.location.coords())
				new_beac[0] = True
			else:
				# new_dir = self.get_travel_direction(new_agent_state)
				new_dir = self.random_rw()
		else:  # mode == "E"
			if self.location.state.is_task:
				new_dir = "S"
				new_agent_state.mode = "D"
				new_agent_state.ct = 0
				new_agent_state.no_tmr_ct = 0
			# elif new_agent_state.large_step is not None:
			# 	new_dir = new_agent_state.large_step[0]
			# 	new_loc = get_coords_from_movement(self.location.coords()[0], self.location.coords()[1], new_dir)
			# 	if not within_bounds(new_loc[0], new_loc[1]):
			# 		new_dir = self.random_rw()
			# 	new_agent_state.large_step = (new_dir, new_agent_state.large_step[1] - 1)
			# 	if new_agent_state.large_step[1] <= 0:
			# 		new_agent_state.large_step = None
			else:
				# new_agent_state.no_tmr_ct += 1
				# if new_agent_state.no_tmr_ct >= 25:
				# 	new_agent_state.no_tmr_ct = 0
				# 	new_dir = self.random_rw()
				# 	new_agent_state.large_step = (new_dir, 5)


				if not sig and new_agent_state.prev[1]:
					new_dir = dir_to_opp[new_agent_state.prev[0]]
				else:
					#new_dir = self.get_travel_direction(new_agent_state)
					new_dir = self.random_rw()

				# new_dir = self.random_rw()


				#new_dir = self.get_travel_direction(new_agent_state)

		# if new_agent_state.mode == 'S':
		# 	prob_m = p_m_beacons
		# else:
		# 	prob_m = p_m
		# if random.random() <= prob_m:
		# 	dirs = []
		# 	for dxdy in local_vertex_mapping:
		# 		try:
		# 			dirs.append(dxdy_to_dir[dxdy])
		# 		except:
		# 			pass
		# 	new_dir = random.choice(dirs)

		new_agent_state.prev = (new_dir, sig)
		return self.location.state, new_agent_state, new_dir
















		# if new_agent_state.committed_task is not None:
		# 	return self.location.state, new_agent_state, "S"
		# else:
		# 	if new_agent_state.mode == "E":
		# 		self.location.state.h_f += b
		# 		if random.random() <= (1-p_e) and self.location.state.c > 0:
		# 			if random.random() <= p_c and self.location.state.residual_demand > 0:
		# 				self.location.state.residual_demand -= 1
		# 				new_agent_state.committed_task = self.location
		# 				new_dir = "S"
		# 			else:
		# 				new_agent_state.found_task = True
		# 				new_dir = "S"
		# 				new_agent_state.ctr = T
		# 				new_agent_state.mode = "H"
		# 				return self.location.state, new_agent_state, new_dir
		#
		# 		else:
		# 			dirs = []
		# 			dxdy_to_c = {}
		# 			dxdy_to_cf = {}
		# 			for dx in [-1,0,1]:
		# 				for dy in [-1,0,1]:
		# 					try:
		# 						dxdy_to_c[(dx,dy)] = local_vertex_mapping[(dx,dy)].state.c
		# 						if random.random() <= p_e:
		# 							dxdy_to_c[(dx,dy)] = 0
		# 						dxdy_to_cf[(dx,dy)] = local_vertex_mapping[(dx,dy)].state.c_f
		# 						if (dx,dy) == (0,0):
		# 							dirs.append("S")
		# 						elif (dx,dy) == (0,1):
		# 							dirs.append("U")
		# 						elif (dx,dy) == (0,-1):
		# 							dirs.append("D")
		# 						elif (dx,dy) == (1,0):
		# 							dirs.append("R")
		# 						elif (dx,dy) == (-1,0):
		# 							dirs.append("L")
		# 					except:
		# 						pass
		# 			if sum(list(dxdy_to_c.values())) > 0:
		# 				new_loc_cands = []
		# 				for dxdy in dxdy_to_c:
		# 					if dxdy_to_c[dxdy] > 0:
		# 						new_loc_cands.append( (self.location.coords()[0] + dxdy[0], self.location.coords()[1] + dxdy[1]) )
		# 				new_loc = random.choice(new_loc_cands)
		# 				new_dir = get_direction_from_destination(new_loc, self.location.coords())
		# 				new_agent_state.found_task = True
		# 				new_agent_state.ctr = T
		# 				new_agent_state.mode = "H"
		# 				return self.location.state, new_agent_state, new_dir
		# 			elif sum(list(dxdy_to_cf.values())) > 0:
		# 				probs = []
		# 				for dir in dirs:
		# 					probs.append(f([ dxdy_to_cf[dir_to_dxdy[dir]] ]) + k)
		# 				probs = [float(x) / sum(probs) for x in probs]
		# 				new_dir = random.choices(dirs, weights=probs, k=1)[0]
		# 			else:
		# 				new_dir = self.get_travel_direction(new_agent_state)
		# 			if random.random() <= p_m:
		# 				dirs = []
		# 				for dxdy in local_vertex_mapping:
		# 					try:
		# 						dirs.append(dxdy_to_dir[dxdy])
		# 					except:
		# 						pass
		# 				new_dir = random.choice(dirs)
		#
		# 		new_agent_state.ctr += 1
		# 		if new_agent_state.ctr >= T:
		# 			new_agent_state.mode = "H"
		# 			new_agent_state.ctr = 0
		#
		# 		return self.location.state, new_agent_state, new_dir
		# 	else:
		# 		if new_agent_state.found_task:
		# 			self.location.state.c_f += a
		#
		# 		dirs = []
		# 		dxdy_to_hf = {}
		# 		for dx in [-1,0,1]:
		# 			for dy in [-1,0,1]:
		# 				try:
		# 					dxdy_to_hf[(dx,dy)] = local_vertex_mapping[(dx,dy)].state.h_f
		# 					if (dx,dy) == (0,0):
		# 						dirs.append("S")
		# 					elif (dx,dy) == (0,1):
		# 						dirs.append("U")
		# 					elif (dx,dy) == (0,-1):
		# 						dirs.append("D")
		# 					elif (dx,dy) == (1,0):
		# 						dirs.append("R")
		# 					elif (dx,dy) == (-1,0):
		# 						dirs.append("L")
		# 				except:
		# 					pass
		# 		if sum(list(dxdy_to_hf.values())) > 0:
		# 			probs = []
		# 			for dir in dirs:
		# 				probs.append(f([ dxdy_to_hf[dir_to_dxdy[dir]] ]) + k)
		# 			probs = [float(x) / sum(probs) for x in probs]
		# 			new_dir = random.choices(dirs, weights=probs, k=1)[0]
		# 		else:
		# 			new_dir = self.get_travel_direction(new_agent_state)
		# 		if random.random() <= p_m:
		# 			dirs = []
		# 			for dxdy in local_vertex_mapping:
		# 				try:
		# 					dirs.append(dxdy_to_dir[dxdy])
		# 				except:
		# 					pass
		# 			new_dir = random.choice(dirs)
		#
		# 	new_agent_state.ctr += 1
		# 	if new_agent_state.ctr >= T:
		# 		new_agent_state.mode = "E"
		# 		new_agent_state.ctr = 0
		# 		new_agent_state.found_task = False
		#
		# 	return self.location.state, new_agent_state, new_dir
