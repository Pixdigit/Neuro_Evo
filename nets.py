# -*- coding: utf-8 -*-
import inodes
import name_gen
import copy
from const_rand import const_rand


global checker
checker = 0


class new_net():

	def __init__(self, d_in, d_comp, d_out, seed=None):
		self.seed = seed
		self.rand = const_rand(self.seed)
		self.name = name_gen.new_name(self.rand.choice)
		self.input_nodes = []
		self.compute_nodes = []
		self.output_nodes = []

		self.result = []

		self.build_cons(d_in, d_comp, d_out)

	def build_cons(self, d_in, d_comp, d_out):

		for i in range(d_in):
			in_node = inodes.new_node(seed=self.rand.random())
			in_node.callers[-1] = 1
			self.input_nodes.append(in_node)

		for i in range(d_comp):
			d_node_inputs = self.rand.randint(1,
						min(len(self.compute_nodes + self.input_nodes), 10))

			compute_node = inodes.new_node(seed=self.rand.random())

			possible_nodes = self.compute_nodes + self.input_nodes
			for i in range(d_node_inputs):
				if len(possible_nodes) == 0:
					break

				node_input_node = self.rand.choice(possible_nodes)
				possible_nodes.remove(node_input_node)

				compute_node.add_in(node_input_node)

			self.compute_nodes.append(compute_node)

		for i in range(d_out):
			d_node_inputs = self.rand.randint(1,
						min(len(self.compute_nodes + self.input_nodes), 10))
			output_node = inodes.new_node(seed=self.rand.random())

			possible_nodes = self.compute_nodes + self.input_nodes
			for i in range(d_node_inputs):
				if len(possible_nodes) == 0:
					break

				node_input_node = self.rand.choice(possible_nodes)
				possible_nodes.remove(node_input_node)

				output_node.add_in(node_input_node)

			self.output_nodes.append(output_node)

		self.rm_no_out_nodes()
		self.rm_no_out_nodes()
		self.rm_no_out_nodes()

		for index in range(len(self.compute_nodes)):
			self.compute_nodes[index].set_weights()
		for index in range(len(self.output_nodes)):
			self.output_nodes[index].set_weights()

	def compute(self, node_input):

		assert len(node_input) == len(self.input_nodes)  # Not enough input given

		in_map = {self.input_nodes[index]: node_input[index]
				for index in range(len(node_input))}

		self.prepare_recursion()
		self.recurse_resolve(self.output_nodes, in_map)

		self.result = [node.value for node in self.output_nodes]

		return self.result

	def prepare_recursion(self):
		self.checked_nodes = list(self.input_nodes)

	def recurse_resolve(self, nodes, in_map):
		global checker
		checker += 1
		for node in nodes:
			if node in self.input_nodes:
				node_input = in_map[node]
				index = self.input_nodes.index(node)
				self.input_nodes[index].input(node_input)
			else:
				if node not in self.checked_nodes:
					checker += 0.000001
					more_nodes = node.get_callers()
					self.recurse_resolve(more_nodes, in_map)
					node_input = {}
					for new_node in node.get_callers():
						value = [chk_node.value for chk_node in
							self.compute_nodes + self.input_nodes
							if chk_node.id == new_node.id][0]
						node_input[new_node] = value
					node.compute(node_input)
					self.checked_nodes.append(node)

	def rm_no_out_nodes(self):
		all_callers = []
		for node in self.compute_nodes + self.output_nodes:
			for caller in node.callers:
				if caller not in all_callers:
					all_callers.append(caller)

		for node in self.compute_nodes:
			if node not in all_callers:
				self.compute_nodes.remove(node)

	def get_clone(self):
		clone = new_net(0, 0, 0, seed=self.rand.random())

		for node in list(self.input_nodes):
			clone.input_nodes.append(node.get_clone())
		for node in list(self.compute_nodes):
			clone.compute_nodes.append(node.get_clone())
		for node in list(self.output_nodes):
			clone.output_nodes.append(node.get_clone())

		all_nodes = clone.input_nodes + clone.compute_nodes + clone.output_nodes
		node_id_map = {node.id: node for node in all_nodes}

		for node in all_nodes:
			for caller in node.callers:
				if caller != -1:
					#Replace key with new reference
					node.callers[node_id_map[caller.id]] = node.callers.pop(caller)

		return clone

	def get_child(self):

		child = self.get_clone()

		return child
