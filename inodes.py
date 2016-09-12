# -*- coding: utf-8 -*-
from const_rand import const_rand
import math


funcs = [
	lambda x: x / (0.3 + abs(x)),  # sigmoid
	lambda x: x,  # plain sum
	lambda x: math.sin(x),  # periodic
	lambda x: 1.0 / x if x != 0 else 100000000000  # inverse
]


class new_node():

	def __init__(self, seed=None):
		self.rand = const_rand(seed)
		self.id = self.rand.random()
		self.callers = {}  # id: true if satisfied
		self.value = 0

	def add_in(self, node):
		self.callers[node.id] = False

	def set_weights(self):
		for caller in self.callers:
			self.callers[caller] = self.rand.random() * 2 - 0.5

	def get_missing_inputs(self):
		return list(self.callers.keys())

	def input(self, value):
		self.value = value

	def compute(self, input_dict):
		value = 0
		for node_id in input_dict.keys():
			value += self.callers[node_id] * input_dict[node_id]
		self.value = value
		#TODO: add function

	def get_mutate(self, mutation_factor=1):
		mut_type = self.rand.random()

		#Complete new weights in 10%
		if 0.8 <= mut_type < 0.9:
			self.set_weights()

		#Change weights in 80%
		if mut_type < 0.8:
			#small change in 60%
			limit = 2
			#big change in 20%
			if mut_type < 0.2:
				limit = 3

			for index in range(len(self.weights)):
				#-limit < factor < limit
				factor = (self.rand.random() * (limit - 1)) + 1

				#very seldomly change polarity with 5%
				if mut_type < 0.05:
					factor *= -1

				if self.rand.random() < 0.6:
					factor = 1 / factor

				self.weights[index] *= factor
