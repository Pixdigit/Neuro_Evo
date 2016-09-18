# -*- coding: utf-8 -*-
import render


def prepare(graphical=True):
	global visible

	#init
	if graphical:
		visible = True
		render.init()
