import pygame
import sys
from scipy.interpolate import interp1d
from geo_utils import signal_amt
from random import uniform
from constants import HOME_LOC, TMR_DST
from math import pi, cos, sin

home_center = (HOME_LOC[0][0] + int((HOME_LOC[1][0] - HOME_LOC[0][0]) / 2), HOME_LOC[0][1] + int((HOME_LOC[1][1] - HOME_LOC[0][1]) / 2))
ang = uniform(0, 2*pi)
tumor_start = (int(home_center[0] + cos(ang)*TMR_DST), int(home_center[1] + sin(ang)*TMR_DST))



class ViewController:
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 200, 0)
	RED = (200,0,0)
	BLUE = (0,0,200)
	YELLOW = (200, 200, 0)
	VERTEX_SIZE = 17
	FPS = 1000
	#FPS = 60

	def __init__(self, configuration):
		self.configuration = configuration
		self.WINDOW_HEIGHT = self.configuration.N*self.VERTEX_SIZE
		self.WINDOW_WIDTH = self.configuration.M*self.VERTEX_SIZE
		pygame.init()
		self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		self.make_grid()

		self.font = pygame.font.SysFont(None, int(self.VERTEX_SIZE*1.2))

	def make_grid(self):
		self.SCREEN.fill(self.WHITE)
		for x in range(0, self.configuration.M):
			for y in range(0, self.configuration.N):
				rect = pygame.Rect(x*self.VERTEX_SIZE, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE, self.VERTEX_SIZE, self.VERTEX_SIZE)
				pygame.draw.rect(self.SCREEN, self.BLACK, rect, 1)
		pygame.display.update()

	def draw_configuration(self):
		beacon_locs = set()
		for x in range(0, self.configuration.M):
			for y in range(0, self.configuration.N):
				for a in self.configuration.vertices[(x,y)].agents:
					if a.state.mode == "S":
						beacon_locs.add((x,y))

		#m = interp1d([0,4], [255,0], bounds_error=False, fill_value=(0,4))
		m = interp1d([0,20], [0,255], bounds_error=False, fill_value=(0,200))

		for x in range(0, self.configuration.M):
			for y in range(0, self.configuration.N):
				rect = pygame.Rect(x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1, self.VERTEX_SIZE-2, self.VERTEX_SIZE-2)
				num_active_agents = len([_ for _ in self.configuration.vertices[(x,y)].agents if _.state.mode == "E"])
				num_beac_agents = len([_ for _ in self.configuration.vertices[(x,y)].agents if _.state.mode != "E"])
				#marker_amt = len([_ for _ in self.configuration.vertices[(x,y)].agents if _.state.type == "C"])

				# signal = 0
				# for beac_loc in beacon_locs:
				# 	signal += signal_amt((x,y), beac_loc)
				# self.configuration.vertices[(x,y)].state.sig = signal

				# if (x,y) == tumor_start:
				# 	pygame.draw.rect(self.SCREEN, self.BLACK, rect, 0)
				# if self.configuration.vertices[(x,y)].state.markers > 0:
				# 	col = float(m(self.configuration.vertices[(x,y)].state.markers))
				# 	pygame.draw.rect(self.SCREEN, (col,col,255), rect, 0)
				if num_active_agents > 0:
					pygame.draw.rect(self.SCREEN, self.GREEN, rect, 0)
				elif num_beac_agents > 0:
					pygame.draw.rect(self.SCREEN, self.BLACK, rect, 0)
				elif self.configuration.vertices[(x,y)].state.is_task:
					pygame.draw.rect(self.SCREEN, self.YELLOW, rect, 0)
					# demand_text = self.font.render(str(self.configuration.vertices[(x,y)].state.residual_demand), True, self.BLACK)
					# self.SCREEN.blit(demand_text, (x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1))
				elif self.configuration.vertices[(x,y)].state.is_home:
					pygame.draw.rect(self.SCREEN, self.RED, rect, 0)
				# elif self.configuration.vertices[(x,y)].state.c_f > 0 and self.configuration.vertices[(x,y)].state.h_f > 0:
				# 	pygame.draw.rect(self.SCREEN, (255,0,255), rect, 0)
				elif self.configuration.vertices[(x,y)].state.marker:
					# col = 255 - m(self.configuration.vertices[(x,y)].state.c_f)
					pygame.draw.rect(self.SCREEN, (100,100,255), rect, 0)
					# demand_text = self.font.render(str(self.configuration.vertices[(x,y)].state.c_f), True, self.BLACK)
					#self.SCREEN.blit(demand_text, (x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1))
				# elif self.configuration.vertices[(x,y)].state.h_f > 0:
				# 	col = 255 - m(self.configuration.vertices[(x,y)].state.h_f)
				# 	pygame.draw.rect(self.SCREEN, (255,col,col), rect, 0)
				# 	demand_text = self.font.render(str(self.configuration.vertices[(x,y)].state.h_f), True, self.BLACK)
					#self.SCREEN.blit(demand_text, (x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1))
				# elif self.configuration.vertices[(x,y)].state.markers > 0:
				# 	col = float(m(self.configuration.vertices[(x,y)].state.markers))
				# 	pygame.draw.rect(self.SCREEN, (col,col,255), rect, 0)
				# elif self.configuration.vertices[(x,y)].state.sig > 0:
				# 	col = float(m(self.configuration.vertices[(x,y)].state.sig))
				# 	pygame.draw.rect(self.SCREEN, (col,col,255), rect, 0)
				else:
					pygame.draw.rect(self.SCREEN, self.WHITE, rect, 0)

	def update(self):
		self.draw_configuration()
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		if self.FPS is not None:
			pygame.time.delay(int(1000/self.FPS))

	def quit(self):
		pygame.quit()
