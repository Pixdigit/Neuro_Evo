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
		vertexes[node] = graph.add_vertex()
		names.append(str(node.id))

		if node in net.input_nodes:
			mode = 1
		elif node in net.compute_nodes:
			mode = 2
		elif node in net.output_nodes:
			mode = 3

		v_color[vertexes[node]] = mode
		v_name[vertexes[node]] = str(node.id)[:5]

	edges = []

	for node in all_nodes:
		for con in node.output_nodes:
			try:
				sec_vert = vertexes[con]
				edges.append(graph.add_edge(vertexes[node], sec_vert))
			except KeyError:
				print any(con.id == con2.id for con2 in all_nodes)
				print con.id
				print [nod.id for nod in all_nodes]
				#raise Exception

	gt.graph_draw(graph, vertex_color=[1, 1, 1, 0], vertex_fill_color=v_color, vertex_text=v_name)
