# -*- coding: utf-8 -*-
import nodes
import copy
import name_gen
import random


class net():

	def __init__(self, d_nodes, d_in_nodes, d_out_nodes, energy=-1):
		"""Create a new net"""

		self.energy = energy
		self.id = name_gen.new_name()
		self.result = []

		d_compute_nodes = d_nodes - d_in_nodes - d_out_nodes

		self.output_nodes = [nodes.new_node() for a in range(d_out_nodes)]
		self.input_nodes = [nodes.new_node() for a in range(d_in_nodes)]

		self.compute_nodes = list(self.input_nodes)

		for node in range(d_compute_nodes):
			new_node = nodes.new_node()
			d_in_cons = random.randint(0, 5)

			for con_nr in range(d_in_cons):

				possible_in_nodes = [in_node for in_node in self.compute_nodes
						if in_node not in new_node.input_nodes]

				max_index = len(possible_in_nodes) - 1

				if max_index < 0:
					break
				else:
					index = int(random.triangular(0, max_index, max_index))
					in_node = possible_in_nodes[index]
					new_node.input_nodes.append(in_node)
					new_node.influence_nodes.append(in_node.influence_nodes + [in_node])
					in_node.output_nodes.append(new_node)

			new_node.set_caller_weights()
			self.compute_nodes.append(new_node)

		for node in self.input_nodes:
			self.compute_nodes.remove(node)

		for node in self.compute_nodes:
			if len(node.output_nodes) + len(node.input_nodes) == 0:
				self.compute_nodes.remove(node)
			elif len(node.output_nodes) == 0:
				for in_node in node.input_nodes:
					in_node.output_nodes.remove(node)
				self.compute_nodes.remove(node)

		for node in self.output_nodes:
			d_in_cons = random.randint(0, 5)
			if d_in_cons > len(self.input_nodes + self.compute_nodes):
				d_in_cons = len(self.input_nodes + self.compute_nodes)

			for con_nr in range(d_in_cons):
				con_node = random.choice(self.input_nodes + self.compute_nodes)

				while con_node in node.input_nodes:
					con_node = random.choice(self.input_nodes + self.compute_nodes)

				node.input_nodes.append(con_node)
				con_node.output_nodes.append(node)

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

		child = copy.deepcopy(self)
		child.energy = cost
		child.id = name_gen.new_name()
		#print "Node ID: " + str(child.compute_nodes[0].id)
		#print "First wheight: " + str(child.compute_nodes[0].weights[0])
		for node in child.compute_nodes:
			node = node.repro(child.output_nodes, 10)
		#print "After mutation"
		#print "Node ID: " + str(child.compute_nodes[0].id)
		#print "First wheight: " + str(child.compute_nodes[0].weights[0])
		#print

		return child

	def use_energy(self, amount):
		if not self.energy < 0:
			self.energy -= amount
		if self.energy < 0:
			self.energy = 0
