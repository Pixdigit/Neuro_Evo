# -*- coding: utf-8 -*-
import inodes
import name_gen
from const_rand import const_rand


def get_by_id(nodes_list, node_id):

	if node_id not in [node.id for node in nodes_list]:
		raise IndexError("No node with id found. " + str(node_id))

	return [node for node in nodes_list if node.id == node_id][0]


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
			in_node = inodes.new_node(seed=self.rand.random())
			in_node.callers[-1] = 1
			self.input_nodes.append(in_node)

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

		self.rm_no_out_nodes()
		self.rm_no_out_nodes()
		self.rm_no_out_nodes()

		for index in range(len(self.compute_nodes)):
			self.compute_nodes[index].set_weights()
		for index in range(len(self.output_nodes)):
			self.output_nodes[index].set_weights()

	def compute(self, node_input):

		assert len(node_input) == len(self.input_nodes)  # Not enough input given

		in_id_map = {self.input_nodes[index].id: node_input[index]
				for index in range(len(node_input))}

		for result_node in self.output_nodes:
			needed_input = list(result_node.callers.keys())
			self.recurse_resolve(needed_input, in_id_map)

	def recurse_resolve(self, node_ids, in_id_map, pre_chk_nodes=[]):
		checked_nodes = [node for node in self.input_nodes + pre_chk_nodes]
		for node_id in node_ids:
			if node_id in [node.id for node in self.input_nodes]:
				node = get_by_id(self.input_nodes, node_id)
				node_input = in_id_map[node.id]
				index = self.input_nodes.index(node)
				self.input_nodes[index].input(node_input)
			else:
				node = get_by_id(self.compute_nodes, node_id)
				if node not in checked_nodes:
					more_nodes = list(node.callers.keys())
					self.recurse_resolve(more_nodes, in_id_map, checked_nodes)
					node_input = {}
					for new_node_id in node.callers:
						node_input[new_node_id] = get_by_id(self.compute_nodes + self.input_nodes,
									new_node_id).value
					node.compute(node_input)
					checked_nodes.append(node)

	def rm_no_out_nodes(self):
		all_callers = []
		for node in self.compute_nodes + self.output_nodes:
			for caller in node.callers:
				if caller not in all_callers:
					all_callers.append(caller)

		for node in self.compute_nodes:
			if node.id not in all_callers:
				self.compute_nodes.remove(node)
