from geo_utils import l2_distance
from constants import *
import random

class VertexState:

	def __init__(self, loc, is_task=False, demand=None, task_location=None, is_home = False):
		self.is_task = is_task
		self.is_home = is_home
		self.demand = demand
		self.residual_demand = demand
		self.task_location = task_location

		# self.markers = 0

		self.marker = False

		# self.c_f = 0
		# self.h_f = 0



		#self.fuel = max( int(10 - l2_distance(loc[0], loc[1], int(M / 2), int(N / 2))), 0 )
		# A, B = 8, 4
		# d = l2_distance(loc[0], loc[1], int(M / 2), int(N / 2))
		# if d <= 0.5 * A:
		# 	self.fuel = A
		# elif d <= 0.5 * A + 2 * B:
		# 	self.fuel = B
		# else:
		# 	self.fuel = 0

		self.cancer = False

		self.num_bound = 0

		d = l2_distance(loc[0], loc[1], int(M / 2), int(N / 2))
		self.fuel = max(-1 * (d - 20) * (d + 20) * (10 / 20**2), 0 )

		self.residual_fuel = self.fuel
		#self.fuel = random.randint(0,10)

		self.visits = 0
