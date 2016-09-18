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
		self.nets = [nets.new_net(d_in_nodes, d_comp_nodes, d_out_nodes, seed=self.rand.random())
				for i in xrange(d_nets)]

		self.performance = {}

		self.perf_func = lambda net: 0

	def set_perf_func(self, func):
		self.perf_func = func

	def do_gen(self):
		self.nets.sort(key=self.perf_func, reverse=self.reverse_sort)
