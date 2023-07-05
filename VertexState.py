from constants import MARKERS


class VertexState:

	def __init__(self, is_home=False):
		self.is_home = is_home

		self.chemicals = {}
		for m in MARKERS:
			self.chemicals[m] = 0
