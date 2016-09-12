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
	test_net = nets.new_net(4, 50, 4, seed=1)
	test_net.compute([1, 2, 3, 4])


def test_graphs():
	import vis
	test_net = nets.new_net(4, 50, 4, seed=1)
	vis.draw_net(test_net)

#test_graphs()
test_net()
