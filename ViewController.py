import pygame
import sys
from scipy.interpolate import interp1d
from geo_utils import signal_amt
from random import uniform
from constants import *
from math import pi, cos, sin


class ViewController:
	VERTEX_SIZE = 17
	FPS = 20

	def __init__(self, configuration):
		self.configuration = configuration
		self.WINDOW_HEIGHT = self.configuration.N*self.VERTEX_SIZE
		self.WINDOW_WIDTH = self.configuration.M*self.VERTEX_SIZE
		pygame.init()
		self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		self.make_grid()

		self.font = pygame.font.SysFont(None, int(self.VERTEX_SIZE*1.2))

	def make_grid(self):
		self.SCREEN.fill((255,255,255))
		for x in range(0, self.configuration.M):
			for y in range(0, self.configuration.N):
				rect = pygame.Rect(x*self.VERTEX_SIZE, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE, self.VERTEX_SIZE, self.VERTEX_SIZE)
				pygame.draw.rect(self.SCREEN, (0,0,0), rect, 1)
		pygame.display.update()

	def draw_configuration(self):
		for x in range(0, self.configuration.M):
			for y in range(0, self.configuration.N):
				rect = pygame.Rect(x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1, self.VERTEX_SIZE-2, self.VERTEX_SIZE-2)

				num_active_workers = len([_ for _ in self.configuration.vertices[(x,y)].agents if _.type == "W" and not _.state.bound])
				num_active_scouts = len([_ for _ in self.configuration.vertices[(x,y)].agents if _.type == "S" and not _.state.bound])
				num_bound_workers = len([_ for _ in self.configuration.vertices[(x,y)].agents if _.type == "W" and _.state.bound])
				num_bound_scouts = len([_ for _ in self.configuration.vertices[(x,y)].agents if _.type == "S" and _.state.bound])
				cancerous = len([_ for _ in self.configuration.vertices[(x,y)].cells if _.state.cancer]) > 0
				injection = self.configuration.vertices[(x,y)].state.is_home

				if num_active_workers > 0:
					pygame.draw.rect(self.SCREEN, (255,0,0), rect, 0)
				elif num_active_scouts > 0:
					pygame.draw.rect(self.SCREEN, (0,0,255), rect, 0)
				elif num_bound_workers > 0:
					pygame.draw.rect(self.SCREEN, (230,100,100), rect, 0)
				elif num_bound_scouts > 0:
					pygame.draw.rect(self.SCREEN, (100,100,230), rect, 0)
				elif cancerous:
					pygame.draw.rect(self.SCREEN, (0,0,0), rect, 0)
				elif injection:
					pygame.draw.rect(self.SCREEN, (255,255,0), rect, 0)
				else:
					pygame.draw.rect(self.SCREEN, (255,255,255), rect, 0)

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
