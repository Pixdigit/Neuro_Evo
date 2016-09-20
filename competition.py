# -*- coding: utf-8 -*-
import nets
import const_rand


class compo():

	def __init__(self, d_nets, net_conf, seed=None, reverse_sort=True):

		self.rand = const_rand.const_rand(seed=seed)

		self.reverse_sort = reverse_sort

		d_in_nodes = net_conf[0]
		d_comp_nodes = net_conf[1]
		d_out_nodes = net_conf[2]
		self.nets = [nets.new_net(
				d_in_nodes, d_comp_nodes, d_out_nodes, seed=self.rand.random())
				for i in xrange(d_nets)]

		self.performance = {}

		self.perf_func = lambda net: 0

	def set_perf_func(self, func):
		self.perf_func = func

	def do_gen(self, d_kills=None, mutation_level=1):

		results = {net.name: self.perf_func(net) for net in self.nets}
		get_perf = lambda net: results[net.name]
		self.nets.sort(key=get_perf, reverse=self.reverse_sort)

		if d_kills is None:
			d_kills = int(len(self.nets) / 20.0 + 1)
		elif 0 <= d_kills <= 1:
			d_kills = int(len(self.nets) * d_kills + 1)

		for i in range(d_kills):
			rand_index = int(self.rand.triangular(0, len(self.nets), len(self.nets)))
			kill = self.nets.pop(rand_index)

		for i in range(d_kills):
			rand_index = int(self.rand.triangular(0, len(self.nets), 0))
			self.nets.append(self.nets[rand_index].get_child())

		return results
