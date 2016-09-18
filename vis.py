# -*- coding: utf-8 -*-
import graph_tool.all as gt


def draw_net(net):
	g = gt.Graph(directed=True)

	v_color = g.new_vertex_property("int")
	v_name = g.new_vertex_property("string")

	combined_nodes = net.input_nodes + net.compute_nodes + net.output_nodes

	vertexes = {}

	for node in combined_nodes:
		vert = g.add_vertex()

		if node in net.input_nodes:
			mode = 1
		elif node in net.compute_nodes:
			mode = 2
		elif node in net.output_nodes:
			mode = 3

		v_color[vert] = mode
		v_name[vert] = str(node.id)[:4]
		vertexes[node] = vert

	for node in combined_nodes:
		for node_con in node.callers:
			if node_con != -1:
				g.add_edge(vertexes[node_con], vertexes[node])

	if not gt.is_DAG(g):
		print(("THE WORLD ENDS"))

	gt.graph_draw(g, vertex_color=[1, 1, 1, 0],
			vertex_fill_color=v_color, vertex_text=v_name)