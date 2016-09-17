# -*- coding: utf-8 -*-
import inodes
import nets
import sys
#from pprint import pprint


def test_nodes():
	test_node = inodes.new_node()
	test_node2 = inodes.new_node()
	test_node.add_in(test_node2)
	print((test_node2.id))
	print((test_node.callers))
	print((test_node.callers))


def test_net():
	testing_net = nets.new_net(4, 50, 4, seed=None)
	result = testing_net.compute([1, 2, 3, 4])
	#print result
	#print nets.checker

conf = {}

if len(sys.argv) == 1:
	test_net()
else:
	#set network configuration
	try:

		try:
			conf_pos = sys.argv.index("-c")
		except:
			conf_pos = sys.argv.index("--conf")

		conf["d_in_nodes"] = int(sys.argv[conf_pos + 1])
		conf["d_comp_nodes"] = int(sys.argv[conf_pos + 2])
		conf["d_out_nodes"] = int(sys.argv[conf_pos + 3])
	except:
		conf["d_in_nodes"] = 1
		conf["d_comp_nodes"] = 3
		conf["d_out_nodes"] = 1

	#turn on graph
	if "-g" in sys.argv:
		conf["graph"] = True
	else:
		conf["graph"] = False

	#set seed
	try:
		try:
			seed_pos = sys.argv.index("-s") + 1
		except:
			seed_pos = sys.argv.index("--seed") + 1

		try:
			conf["seed"] = int(sys.argv[seed_pos])
		except:
			conf["seed"] = sys.argv[seed_pos]
	except:
		conf["seed"] = None

	#get input values
	try:
		conf["input"] = []
		for i in range(conf["d_in_nodes"]):
			conf["input"].append(int(sys.argv[i - conf["d_in_nodes"]]))
	except:
		conf["input"] = [1]

	#pprint(conf)

	testing_net = nets.new_net(
			conf["d_in_nodes"], conf["d_comp_nodes"], conf["d_out_nodes"],
			seed=conf["seed"])
	result = testing_net.compute(conf["input"])
	print(("Result: " + str(result)))
	print(("Resolves: " + str(nets.checker)))

	if conf["graph"]:
		import vis
		vis.draw_net(testing_net)
