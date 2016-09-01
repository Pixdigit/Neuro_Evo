# -*- coding: utf-8 -*-
import inodes
import nets


def test_nodes():
	test_node = inodes.new_node()
	test_node2 = inodes.new_node()
	test_node.add_in(test_node2)
	print((test_node2.id))
	print((test_node.callers))
	print((test_node.callers))


def test_net():
	test_net = nets.new_net(1, 2, 1, seed=None)
	print((test_net.name))
	print((test_net.input_nodes))
	print((test_net.input_nodes[0].id))
	print("")
	print((test_net.compute_nodes))
	for node in test_net.compute_nodes:
		print((node.id))
		print((node.callers))
	print("")
	print(test_net.output_nodes)
	print(test_net.output_nodes[0].id)
	print("")

	test_net.compute([1])


def test_graphs():
	import vis
	test_net = nets.new_net(1, 2, 1, seed=None)
	vis.draw_net(test_net)

test_graphs()
#test_net()
