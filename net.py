# -*- coding: utf-8 -*-
import nodes
import name_gen
import random


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

	def triangular(self, a, b, c):
		random.seed(self.seed)
		result = random.triangular(a, b, c)
		self.seed = int(999999 * result)
		return result

	def choice(self, iterable):
		random.seed(self.seed)
		result = random.choice(iterable)
		self.seed = random.randint(0, 999999)
		return result

	def copy(self):
		return const_rand(self.seed)


class net():

	def __init__(self, d_nodes, d_in_nodes, d_out_nodes, energy=-1, seed=None):
		"""Create a new net"""

		self.energy = energy
		self.seed = seed
		self.random = const_rand(self.seed)
		self.id = name_gen.new_name(self.random.choice)
		self.result = []

		d_compute_nodes = d_nodes - d_in_nodes - d_out_nodes

		self.output_nodes = [nodes.new_node() for a in range(d_out_nodes)]
		self.input_nodes = [nodes.new_node() for a in range(d_in_nodes)]

		self.compute_nodes = list(self.input_nodes)

		for node_num in range(d_compute_nodes):
			new_node = nodes.new_node()
			d_in_cons = self.random.randint(0, 5)

			for con_nr in range(d_in_cons):

				possible_in_nodes = [in_node for in_node in self.compute_nodes
						if in_node not in new_node.input_nodes]

				max_index = len(possible_in_nodes) - 1

				if max_index < 0:
					break
				else:
					index = int(self.random.triangular(0, max_index, max_index))
					in_node = possible_in_nodes[index]
					new_node.input_nodes.append(in_node)
					new_node.influence_nodes.append(in_node.influence_nodes + [in_node])
					in_node.output_nodes.append(new_node)

			new_node.set_caller_weights()
			self.compute_nodes.append(new_node)

		for node in self.input_nodes:
			self.compute_nodes.remove(node)

		for node in self.output_nodes:
			d_in_cons = self.random.randint(0, 5)
			if d_in_cons > len(self.input_nodes + self.compute_nodes):
				d_in_cons = len(self.input_nodes + self.compute_nodes)

			for con_nr in range(d_in_cons):
				con_node = self.random.choice(self.input_nodes + self.compute_nodes)

				while con_node in node.input_nodes:
					con_node = self.random.choice(self.input_nodes + self.compute_nodes)

				node.input_nodes.append(con_node)
				con_node.output_nodes.append(node)

		for node in self.compute_nodes:
			if len(node.output_nodes) + len(node.input_nodes) == 0:
				self.compute_nodes.remove(node)
			elif len(node.output_nodes) == 0:
				for in_node in node.input_nodes:
					in_node.output_nodes.remove(node)
				self.compute_nodes.remove(node)

#		for node in self.input_nodes:
#			if len(node.output_nodes

		for node in self.output_nodes:
			node.set_caller_weights()

	def compute(self, data_input):
		"""Activate the neural net"""
		for channel in range(len(data_input)):
			self.input_nodes[channel].input(data_input[channel])

		out_data = []
		for out_node in self.output_nodes:
			out_data.append(out_node.value)

		self.result = out_data

		return out_data

	def repro(self, cost=0):
		if type(cost) == float:
			cost *= self.energy
			cost = int(cost)

		self.energy -= cost

		child = self.copy()
		child.energy = cost
		child.id = name_gen.new_name()
		new_nodes = []
		for node in child.compute_nodes:
			new_nodes.append(node.repro(child, 100))
		child.compute_nodes = new_nodes

		return child

	def copy(self):
		child = net(0, 0, 0, energy=self.energy, seed=self.seed)
		child.input_nodes = [node.copy() for node in self.input_nodes]
		child.compute_nodes = [node.copy() for node in self.compute_nodes]
		child.output_nodes = [node.copy() for node in self.output_nodes]

		enable_node = lambda node: node.get_nodes_by_id(child)
		for in_node in child.input_nodes:
			enable_node(in_node)
		for co_node in child.compute_nodes:
			enable_node(co_node)
		for ou_node in child.output_nodes:
			enable_node(ou_node)

		child.energy = self.energy
		child.id = self.id
		child.random = self.random.copy()
		return child

	def use_energy(self, amount):
		if not self.energy < 0:
			self.energy -= amount
		if self.energy < 0:
			self.energy = 0
