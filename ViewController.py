import pygame
import sys
from scipy.interpolate import interp1d
from geo_utils import signal_amt
from random import uniform
from constants import HOME_LOC, TMR_DST, M, N
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
	FPS = 60

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

		for x in range(0, self.configuration.M):
			for y in range(0, self.configuration.N):
				rect = pygame.Rect(x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1, self.VERTEX_SIZE-2, self.VERTEX_SIZE-2)

				num_agents = len([_ for _ in self.configuration.vertices[(x,y)].agents if not _.state.bound])
				fuel_m = min(self.configuration.vertices[(x,y)].state.fuel / 10, 1)

				if (x, y) == (int(M / 2), int(N / 2)):
					pygame.draw.rect(self.SCREEN, self.YELLOW, rect, 0)
				elif num_agents > 0:
					pygame.draw.rect(self.SCREEN, self.GREEN, rect, 0)
				else:
					pygame.draw.rect(self.SCREEN, (255*(1-fuel_m), 255*(1-fuel_m), 255), rect, 0)

				# demand_text = self.font.render(str(self.configuration.vertices[(x,y)].state.residual_fuel), True, self.BLACK)
				# self.SCREEN.blit(demand_text, (x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1))

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
