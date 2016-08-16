# -*- coding: utf-8 -*-
import random
import math


class const_rand():

	def __init__(self, seed=None):
		if seed is None:
			seed = random.randint(0, 999999)
		self.seed = seed

	def randint(self, a, b):
		random.seed(self.seed)
		result = random.randint(a, b)
		self.seed = random.randint(0, 999999)
		return result

	def random(self):
		random.seed(self.seed)
		result = random.random()
		self.seed = int(999999 * result)
		return result

	def choice(self, iterable):
		random.seed(self.seed)
		result = random.choice(iterable)
		self.seed = random.randint(0, 999999)
		return result


def get_reaction_type(random_float):
	if random_float < 1:
		return "memory"
	elif random_float < 5:
		return "constant"
	elif random_float <= 100:
		return "calcing"


def get_operation_type(random_float):
	if random_float < 1:
		#sinus
		return lambda x: math.sin(x)
	elif random_float < 6:
		#1 / value
		return lambda x: 1.0 / x if x != 0 else 999999999
	elif random_float < 11:
		#invert
		return lambda x: -x
	elif random_float < 26:
		#linear decreasement
		return lambda x: x / 2.0
	elif random_float < 31:
		#linear increasement
		return lambda x: 2 * x
	elif random_float < 100:
		#sigmoid
		return lambda x: float(x) / (1 + abs(x))


class new_node():

	def __init__(self):
		self.random = const_rand()
		self.value = 1
		self.react_type = None
		self.state = "Idle"
		self.weights = []
		self.callers = []
		self.output_nodes = []

	def set_behaviour(self, possible_output_nodes):
		self.id = self.random.random()
		self.value = self.id
		reaction = self.random.random() * 100
		self.react_type = get_reaction_type(reaction)
		operation = self.random.random() * 100
		self.operation = get_operation_type(operation)

		#remove linkage to given list
		possible_output_nodes = list(possible_output_nodes)

		if len(possible_output_nodes) <= 0:
			d_out_going_connections = 0
		else:
			random_connection_amount = self.random.randint(1, len(possible_output_nodes))
			d_out_going_connections = min(9, random_connection_amount)

		for conenction in range(d_out_going_connections):
			node = self.random.choice(possible_output_nodes)
			node.add_caller(self)
			self.output_nodes.append(node)
			possible_output_nodes.remove(node)

	def set_caller_weights(self):
		for caller in list(self.callers):
			weight = self.random.random() * 2 - 0.5
			if -0.01 < weight < 0.01:
				caller.remove_connection(self)
				self.callers.remove(caller)
			else:
				self.weights.append(weight)

	def input(self, data_in):
		self.state = "Waiting"
		if self.react_type == "calcing":
			merged_input = 0
		elif self.react_type == "constant":
			merged_input = self.id
		elif self.react_type == "memory":
			merged_input = self.value
		else:
			raise Exception("Type has not been set properly")

		#Test if all inputs are finished
		if (all([node.state == "Idle" for node in self.callers])
				and len(self.callers) > 0):
			if not self.react_type == "constant":
				for input_num in range(len(self.callers)):
					try:
						merged_input += self.callers[input_num].value * self.weights[input_num]
					except:
						print input_num
						print len(self.callers)
						print len(self.weights)
						exit()
		elif len(self.callers) == 0:
			merged_input = data_in
		else:
			raise Exception("Caller Idle. Should not have happened")

		self.value = self.operation(merged_input)
		self.state = "Idle"
		for out_node in self.output_nodes:
			out_node.input(self.value)

	def add_caller(self, caller):
		self.callers.append(caller)

	def remove_connection(self, node):
		self.output_nodes.remove(node)
