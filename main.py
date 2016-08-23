# -*- coding: utf-8 -*-
import competition
import time
import random
import json
import vis


conf = [5, 1, 1]
gens = []

random.seed(1)


def av_perf(pop):
	total_perf = 0
	for net in pop:
		total_perf += perf_func(net)
	return total_perf / float(len(pop))


def all_perf(pop):
	return sorted({net.id: round(perf_func(net), 2) for net in pop}.items(),
			key=lambda t: t[1], reverse=True)

perf_func = lambda net: (sum(net.result) / float(len(net.result))
			if len(net.result) != 0 else 0)


compo = competition.create_compo(5, conf)
compo.set_perf_func(perf_func)

#for net in compo.population:
#	vis.draw_net(net)

for a in range(200):
	compo.calc([10])
	compo.repro(min_performance=0.01, random_kills=0.5)
	print((all_perf(compo.population)))
#	time.sleep(1)
	#gens.append(all_perf(compo.population))
#	if a % 100 == 0:
#		print a / 1000.0 * 100

#json.dump(gens, open("./data.json", "w"))
