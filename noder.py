# -*- coding: utf-8 -*-
from const_rand import const_rand

node_functions = [
		lambda x: x]


class create_node():

	def __init__(self, seed=None):
		self.rand = const_rand(seed=seed)
		self.id = self.rand.random()
		self.d_inputs = 0
		self.result = 0
		self.merged_input = 0
		self.create_properties()

	def create_properties(self):
		self.weights = {}
		self.compute_func = self.rand.choice(node_functions)

	def add_input(self, input_node_id):
		self.weights[input_node_id] = self.rand.random() * 2 - 0.5

	def input(self, input_node_id, value):
		self.merged_input += self.weights[input_node_id] * value

	def compute(self):
		self.result = self.compute_func(self.merged_input)
		self.merged_input = 0
		return self.result
