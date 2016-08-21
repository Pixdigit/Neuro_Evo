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


def get_reaction_type(random_percent):
	if random_percent < 1:
		return "memory"
	elif random_percent < 5:
		return "constant"
	elif random_percent <= 100:
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

	def __init__(self, seed=None):
		if seed is None:
			self.seed = random.randint(0, 999999)
		else:
			self.seed = seed
		self.random = const_rand(seed)
		self.state = "Idle"
		self.weights = []
		self.influence_nodes = []
		self.input_nodes = []
		self.output_nodes = []

		self.id = self.random.random()
		self.value = self.id

		reaction = self.random.random() * 100
		self.react_type = get_reaction_type(reaction)

		operation = self.random.random() * 100
		self.operation = get_operation_type(operation)

	def set_caller_weights(self):
		for caller in list(self.input_nodes):
			weight = self.random.random() * 2 - 0.5
			if -0.01 < weight < 0.01:
				caller.remove_connection(self)
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
		if (all([node.state == "Idle" for node in self.input_nodes])
				and len(self.input_nodes) > 0):
			if not self.react_type == "constant":
				for input_num in range(len(self.input_nodes)):
					merged_input += self.input_nodes[input_num].value * self.weights[input_num]
					#print self.input_nodes[input_num].value - self.input_nodes[input_num].value * self.weights[input_num]
		elif len(self.input_nodes) == 0:
			merged_input = data_in
		else:
			raise Exception("Caller Idle. Should not have happened")

		self.value = self.operation(merged_input)
		self.state = "Idle"
		for out_node in self.output_nodes:
			out_node.input(self.value)

	def add_caller(self, caller):
		self.input_nodes.append(caller)

	def rm_caller(self, caller):
		self.input_nodes.remove(caller)

	def add_connection(self, node):
		self.output_nodes.append(node)
		node.add_caller(self)

	def remove_connection(self, node):
		self.output_nodes.remove(node)
		node.rm_caller(self)

	def copy(self):
		child = new_node(self.seed)
		child.output_nodes = list(self.output_nodes)
		child.weights = list(self.weights)
		child.callers = list(self.input_nodes)
		return child

	def repro(self, possible_output_nodes, relative_mutation=1):
		child = self.copy()
		child.random = const_rand()
		config_list = [child.random.random() for a in range(6)]

		remove_rand_out_con = lambda child: child.remove_connection(
						child.random.choice(child.output_nodes))
		add_rand_out_con = lambda child: child.add_connection(
						child.random.choice(possible_output_nodes))

		connection_changes = [remove_rand_out_con, add_rand_out_con]

#		if config_list[0] <= 0.00001 * relative_mutation:
#			#change connections
#			for a in range(len(child.output_nodes) / 5):
#				child.random.choice(connection_changes)(child)
#		elif config_list[1] <= 0.000001 * relative_mutation:
#			child.react_type = get_reaction_type(child.random.random() * 100)
#		elif config_list[2] <= 0.000005 * relative_mutation:
#			child.operation = get_operation_type(child.random.random() * 100)
#		elif config_list[3] <= 0.0000001 * relative_mutation:
#			for node in child.callers:
#				node.remove_connection(child)
#			for node in child.output_nodes:
#				child.output_nodes.remove_connection(node)
#			child.energy = 0
		if config_list[5] <= 0.1 * relative_mutation:
			d_weights_change = random.randint(0,
						int(len(child.callers) / 3.0 * 2 * relative_mutation))
			for a in range(d_weights_change):
				for caller_num in range(len(child.callers)):
					child.weights[caller_num] *= 500000 + child.random.random() / 10
					print child.weights[caller_num]
		return child
