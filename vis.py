# -*- coding: utf-8 -*-
import graph_tool.all as gt


def draw_net(net):
	graph = gt.Graph()
	v_color = graph.new_vertex_property("int")
	v_name = graph.new_vertex_property("string")
	all_nodes = net.input_nodes + net.compute_nodes + net.output_nodes
	vertexes = {}
	names = []
	for node in all_nodes:
		vertexes[node.id] = graph.add_vertex()
		names.append(str(node.id))

		if node in net.input_nodes:
			mode = 1
		elif node in net.compute_nodes:
			mode = 2
		elif node in net.output_nodes:
			mode = 3

		v_color[vertexes[node.id]] = mode
		v_name[vertexes[node.id]] = str(node.id)[:5]

	edges = []

	for node in all_nodes:
		for con in node.output_nodes:
			sec_vert = vertexes[con.id]
			edges.append(graph.add_edge(vertexes[node.id], sec_vert))

	gt.graph_draw(graph, vertex_color=[2, 1, 1, 0],
			vertex_fill_color=v_color, vertex_text=v_name)
