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
		self.compute_nodes = [nodes.new_node() for a in range(d_compute_nodes)]
		self.input_nodes = [nodes.new_node() for a in range(d_in_nodes)]

		for node in self.compute_nodes:
			possible_nodes = [possible_node for possible_node in self.compute_nodes
					if possible_node not in node.influence_nodes]

			if len(possible_nodes) > 1:
				possible_nodes.remove(node)

				con_node = random.choice(possible_nodes)

				node.output_nodes.append(con_node)
				con_node.input_nodes.append(node)
				con_node.influence_nodes = con_node.influence_nodes + node.influence_nodes
			elif len(possible_nodes) < 1:
				self.compute_nodes.remove(node)

		for node in self.input_nodes:
			con_node = random.choice(self.compute_nodes)
			#TODO: possible_nodes.remove(con_node)

			node.output_nodes.append(con_node)
			con_node.input_nodes.append(node)
			con_node.influence_nodes.append(node)

		for node in self.output_nodes:
			con_node = random.choice(self.compute_nodes)

			while con_node in node.influence_nodes:
				con_node = random.choice(possible_nodes)

			#TODO: possible_nodes.remove(con_node)

			node.input_nodes.append(con_node)
			con_node.output_nodes.append(node)

		for node in self.compute_nodes:
			node.set_caller_weights()
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
		child.id = self.id + "+" + name_gen.new_name()
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
