# -*- coding: utf-8 -*-
from const_rand import const_rand


class new_node():

	def __init__(self, seed=None):
		self.rand = const_rand(seed)
		self.id = self.rand.random()
		self.callers = {}  # id: true if satisfied
		self.value = 0
		self.finished = False

	def add_in(self, node):
		self.callers[node.id] = False

	def set_weights(self):
		self.weights = [self.rand.random() * 2 - 0.5
				for i in range(len(self.callers))]

	def get_missing_inputs(self):
		return [caller for caller in self.callers if not self.callers[caller]]

	def input(self, value):
		self.value = value

	def compute(self):
		self.finshed = True