# -*- coding: utf-8 -*-
import random


global used_names
global vovels
global consonants
global length

used_names = [""]
vovels = ["a", "e", "i", "o", "u"]
consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m",
		"n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
length = 1


def new_name(choice=random.choice):

	global length
	global used_names
	name = ""

	if len(used_names) == 105 ** length:
		length += 1

	while name in used_names:
		name = ""

		for i in range(length):
			name = name + choice(consonants)
			name = name + choice(vovels)

	used_names.append(name)
	return name
