# -*- coding: utf-8 -*-
from const_rand import const_rand
from name_gen import new_name
from noder import create_node


class create_net():

	def __init__(self, d_input_nodes, d_compute_nodes, d_output_nodes,
			seed=None):
		self.rand = const_rand(seed=seed)
		self.id = new_name()
		self.create_connections(d_input_nodes, d_compute_nodes, d_output_nodes)

	def create_connections(self, d_input_nodes, d_compute_nodes, d_output_nodes):

		self.influences = {}

		def follow_path(node_id):
			if node_id not in self.comp_connections:
				return []

			sub_nodes = self.comp_connections[node_id]
			meetings = list(sub_nodes)

			print "Called: " + str(node_id)

			for node in sub_nodes:
				try:
					subs = follow_path(node)
				except RuntimeError:
					print self.comp_connections
					exit(9)
				if subs != []:
					meetings = meetings + subs
			return meetings

		self.comp_nodes = {}
		for i in range(d_compute_nodes):
			node = create_node(seed=self.rand.random())
			self.comp_nodes[node.id] = node
			self.influences[node.id] = []

		self.in_nodes = {}
		for i in range(d_input_nodes):
			node = create_node(seed=self.rand.random())
			self.in_nodes[node.id] = node
			self.influences[node.id] = []

		self.out_nodes = {}
		for i in range(d_output_nodes):
			node = create_node(seed=self.rand.random())
			self.out_nodes[node.id] = node

		self.comp_connections = {}
		for comp_node_id in self.comp_nodes:
			possible_node_ids = list(self.comp_nodes.keys())
			possible_node_ids.remove(comp_node_id)

			d_out_cons = self.rand.randint(1, 10)

			self.comp_connections[comp_node_id] = []

			for node_id in possible_node_ids:
				if comp_node_id in follow_path(node_id):
					if round(comp_node_id, 3) == 0.864:
						a = self.comp_connections[comp_node_id]
						print a
						exit(9)
					possible_node_ids.remove(node_id)
				print
				print "Finished"

			for con in range(d_out_cons):
				if len(possible_node_ids) == 0:
					break
				node_id_con_to = self.rand.choice(possible_node_ids)
				possible_node_ids.remove(node_id_con_to)

				self.comp_nodes[node_id_con_to].add_input(comp_node_id)
				self.comp_connections[comp_node_id].append(node_id_con_to)
				self.influences[comp_node_id].append(node_id_con_to)

		self.in_connections = {}
		for in_node_id in self.in_nodes:
			possible_node_ids = list(self.comp_nodes.keys())
			d_out_cons = self.rand.randint(1, 10)

			self.in_nodes[in_node_id].add_input(-1)
			self.in_nodes[in_node_id].weights[-1] = 1

			self.in_connections[in_node_id] = []

			for con in range(d_out_cons):
				if len(possible_node_ids) == 0:
					break
				node_id_con_to = self.rand.choice(possible_node_ids)
				possible_node_ids.remove(node_id_con_to)
				self.comp_nodes[node_id_con_to].add_input(in_node_id)
				self.in_connections[in_node_id].append(node_id_con_to)
				self.influences[in_node_id].append(node_id_con_to)

		for out_node_id in self.out_nodes:
			possible_node_ids = list(self.in_nodes.keys()) + list(self.comp_nodes.keys())

			for i in range(self.rand.randint(1, 10)):
				if len(possible_node_ids) == 0:
					break
				input_node_id = self.rand.choice(possible_node_ids)
				if input_node_id in self.comp_nodes:
					self.comp_nodes[input_node_id].add_input(out_node_id)
				else:
					self.in_nodes[input_node_id].add_input(out_node_id)

				self.influences[input_node_id].append(out_node_id)
				possible_node_ids.remove(input_node_id)

	def compute(self, inputs):

		if len(inputs) != len(self.in_nodes):
			raise ValueError("Amount of inputs needs to match to amount of input nodes")

		results = {}
		results

		index = 0
		for node_id in self.in_nodes:
			self.in_nodes[node_id].input(-1, inputs[index])
			self.in_nodes[node_id].compute()
			index += 1

		for in_node_id in self.in_connections:
			result = self.in_nodes[in_node_id].result
			for node_to_id in self.in_connections[in_node_id]:
				self.comp_nodes[node_to_id].input(in_node_id, result)

		for comp_node_id in self.comp_connections:
			result = self.comp_nodes[comp_node_id].result
			for node_to_id in self.comp_connections[comp_node_id]:
				self.comp_nodes[node_to_id].input(comp_node_id, result)

#		for out_node_id in self.out_connections:
#			result = self.out_nodes[out_node_id].result
#			for node_to_id in self.out_connections[out_node_id]:
#				self.comp_nodes[node_to_id].input(out_node_id, result)
