# -*- coding: utf-8 -*-
import net
import random


def limit(value, min_value, max_value):
	return min(max(value, min_value), max_value)


class create_compo():

	def __init__(self, amount, net_config, start_energy=-1):

		self.support_amount = amount
		self.population = []
		for net_num in range(amount):
			d_all_nodes = net_config[0]
			d_input_nodes = net_config[1]
			d_output_nodes = net_config[2]
			neuro_net = net.net(d_all_nodes, d_input_nodes, d_output_nodes, start_energy)
			self.population.append(neuro_net)

		self.net_perf = lambda net: (sum(net.result) / float(len(net.result))
					if len(net.result) != 0 else 0)

	def set_perf_func(self, function):
		self.net_perf = function

	def calc(self, data_input, boost=0):
		for net in self.population:
			net.energy += boost
			net.compute(data_input)

	def death(self, min_performance=0, random_kills=0, i=None):

		pop_size = len(self.population)

		if type(random_kills) == float:
			random_kills = int(random_kills * pop_size)
		total_kills = random_kills

		def add_dead_var(obj):
			obj.dead = False
			return obj

		def rm_dead_var(obj):
			del obj.dead
			return obj

		self.population = list(map(add_dead_var, self.population))

		for net in list(self.population):
			if self.net_perf(net) <= min_performance:
				net.dead = True

		total_kills = int(total_kills)

		for kill in range(total_kills):
			index = random.triangular(0, pop_size - 1, pop_size - 1)
			index = int(index)

			net = self.population[index]
			counter_net = self.population[-index]

			if not net.dead:
				net.dead = True
			else:
				net.dead = False
				counter_net.dead = True

		self.population = [obj for obj in self.population if not obj.dead]
		self.population = list(map(rm_dead_var, self.population))

	def repro(self, min_performance=0, random_kills=0, cost=0):

		self.death(min_performance, random_kills)

#		log_func = lambda x, high: (math.log(x + 1) * high / math.log(high + 1)
#					if high != 0
#					else 0)

		old_gen_max_index = len(self.population) - 1

		if len(self.population) == 0:
			print("Population Dead!")
			exit()

		while len(self.population) < self.support_amount:
			index = int(random.triangular(0, old_gen_max_index))
			self.population.append(self.population[index].repro(cost))

	def sort(self):
		self.population = sorted(self.population, key=self.net_perf)
