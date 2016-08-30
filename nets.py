# -*- coding: utf-8 -*-
import inodes
import name_gen
from const_rand import const_rand


class new_net():

	def __init__(self, d_in, d_comp, d_out, seed=None):
		self.rand = const_rand(seed)
		self.name = name_gen.new_name()
		self.input_nodes = []
		self.compute_nodes = []
		self.output_nodes = []

		self.build_cons(d_in, d_comp, d_out)

	def build_cons(self, d_in, d_comp, d_out):

		for i in range(d_in):
			self.input_nodes.append(inodes.new_node(seed=self.rand.random()))

		for i in range(d_comp):
			d_node_inputs = self.rand.randint(1, 10)

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
			d_node_inputs = self.rand.randint(1, 10)
			output_node = inodes.new_node(seed=self.rand.random())

			possible_nodes = self.compute_nodes + self.input_nodes
			for i in range(d_node_inputs):
				if len(possible_nodes) == 0:
					break

				node_input_node = self.rand.choice(possible_nodes)
				possible_nodes.remove(node_input_node)

				output_node.add_in(node_input_node)

			self.output_nodes.append(output_node)

	def compute(self, node_input):

		for result_node in self.output_nodes:
			needed_input = result_node.get_missing_inputs()
			self.recurse_resolve(needed_input)

	def recurse_resolve(self, node_ids):
		for node_id in node_ids:
			if node_id in [node.id for node in self.input_nodes]:
				#TODO: set inputs
				pass
			else:
				node = [nod for nod in self.compute_nodes if nod.id == node_id][0]
				more_nodes = node.get_missing_inputs()
				self.recurse_resolve(more_nodes)
				node.compute()
