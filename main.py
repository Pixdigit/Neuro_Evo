# -*- coding: utf-8 -*-
import competition
import time
import random
import json


conf = [5, 1, 1]
gens = []


def av_perf(pop):
	total_perf = 0
	for net in pop:
		total_perf += perf_func(net)
	return total_perf / float(len(pop))


def all_perf(pop):
	return sorted({net.id: round(perf_func(net), 2) for net in pop}.items(),
			key=lambda t: t[1], reverse=True)

perf_func = lambda net: net.result[0]

compo = competition.create_compo(5, conf)
compo.set_perf_func(perf_func)

compo.calc([10])
print all_perf(compo.population)[:10]


for a in xrange(20):
	compo.calc([10])
	compo.repro(min_performance=0, random_kills=0.25)
	print all_perf(compo.population)[:10]
#	time.sleep(1)
	#gens.append(all_perf(compo.population))
#	if a % 100 == 0:
#		print a / 1000.0 * 100

#json.dump(gens, open("./data.json", "w"))
