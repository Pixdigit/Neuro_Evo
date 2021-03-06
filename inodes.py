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
		self.callers = {}  # node_obj: weights
		self.function = self.rand.choice(funcs)
		self.value = 0

	def add_in(self, node):
		self.callers[node] = 0

	def set_weights(self):
		for caller in self.callers:
			self.callers[caller] = self.rand.random() * 2 - 0.5

	def get_callers(self):
		return list(self.callers.keys())

	def input(self, value):
		self.value = value

	def compute(self, input_dict):
		value = 0
		for node in input_dict.keys():
			value += self.callers[node] * input_dict[node]
		self.value = self.function(value)

	def get_clone(self):
		clone = new_node(seed=self.rand.random())

		clone.id = self.id
		clone.function = self.function

		clone.callers = {}

		for caller in self.callers:
			if caller == -1:
				clone.callers[-1] = 1
			else:
				new_caller = new_node()
				new_caller.id = caller.id
				clone.callers[new_caller] = self.callers[caller]
		return clone

	def get_mutate(self, mutation_factor=1):
		child = self.get_clone()

		mut_type = child.rand.random()

		#Complete new weights in 10%
		if 0.8 <= mut_type < 0.9:
			child.set_weights()

		#Change weights in 80%
		if mut_type < 0.8:
			#small change in 60%
			limit = 2
			#big change in 20%
			if mut_type < 0.2:
				limit = 3

			for index in range(len(child.weights)):
				#-limit < factor < limit
				factor = (child.rand.random() * (limit - 1)) + 1

				#very seldomly change polarity with 5%
				if mut_type < 0.05:
					factor *= -1

				if child.rand.random() < 0.6:
					factor = 1 / factor

				child.weights[index] *= factor

		return child
