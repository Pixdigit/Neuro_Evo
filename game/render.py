# -*- coding: utf-8 -*-
import pygame
import os


def init():
	global screen
	global res

	#set resolution
	res = (1000, 1000)

	#set screen centered
	os.environ["SDL_VIDEO_CENTERED"] = "1"

	#init screen
	pygame.init()
	screen = pygame.display.set_mode(res)
