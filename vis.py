# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx


def draw_net(net):
	g = nx.Graph()

	combined_nodes = net.input_nodes + net.compute_nodes + net.output_nodes
	g.add_nodes_from([round(node.id, 2) for node in combined_nodes])

	val_map = {}
	for node in net.input_nodes:
		val_map[round(node.id, 2)] = 1.0
	for node in net.compute_nodes:
		val_map[round(node.id, 2)] = 0.5
	for node in net.output_nodes:
		val_map[round(node.id, 2)] = 0.0
	colors = [val_map[round(node.id, 2)] for node in combined_nodes]

	nx.draw(g, cmap=plt.get_cmap("gnuplot"), node_color=colors)

	plt.show()