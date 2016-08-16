# -*- coding: utf-8 -*-
import nodes


class net():

	def __init__(self, d_nodes, d_in_nodes, d_out_nodes):
		"""Create a new net"""

		d_compute_nodes = d_nodes - d_in_nodes - d_out_nodes

		self.output_nodes = [nodes.new_node() for a in range(d_out_nodes)]
		self.compute_nodes = [nodes.new_node() for a in range(d_compute_nodes)]
		self.input_nodes = [nodes.new_node() for a in range(d_in_nodes)]

		for node in self.output_nodes:
			node.set_behaviour([])
		for node in self.compute_nodes:
			node.set_behaviour(self.output_nodes)
		for node in self.input_nodes:
			node.set_behaviour(self.compute_nodes + self.output_nodes)
			node.set_caller_weights()
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

		return out_data
