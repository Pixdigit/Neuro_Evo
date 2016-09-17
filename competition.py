# -*- coding: utf-8 -*-
import nets
import const_rand


class compo():
	
	def __init__(self, d_nets, net_conf, seed=None):

		self.rand = const_rand.const_rand(seed=seed)

		d_in_nodes = net_conf[0]
		d_comp_nodes = net_conf[1]
		d_out_nodes = net_conf[2]
		self.nets = [nets.new_net(d_in_nodes, d_comp_nodes, d_out_nodes, seed=self.rand.random())]

		self.perf_func = lambda net: 0

	def set_perf_func(self, func):
		self.perf_func = func
