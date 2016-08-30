# -*- coding: utf-8 -*-
from const_rand import const_rand


class new_node():

	def __init__(self, seed=None):
		self.rand = const_rand(seed)
		self.id = self.rand.random()
		self.callers = {}  # id: true if satisfied
		self.finished = False

	def add_in(self, node):
		self.callers[node.id] = False

	def get_missing_inputs(self):
		return [caller for caller in self.callers if not self.callers[caller]]

	def compute(self):
		self.finshed = True