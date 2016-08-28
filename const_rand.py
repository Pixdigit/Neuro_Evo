# -*- coding: utf-8 -*-
import random


class const_rand():

	def __init__(self, seed=None):
		if seed is None:
			seed = random.randint(0, 999999)
		self.seed = seed

	def randint(self, a, b):
		random.seed(self.seed)
		result = random.randint(a, b)
		self.seed = random.randint(0, 999999)
		return result

	def random(self):
		random.seed(self.seed)
		result = random.random()
		self.seed = int(999999 * result)
		return result

	def triangular(self, a, b, c):
		random.seed(self.seed)
		result = random.triangular(a, b, c)
		self.seed = int(999999 * result)
		return result

	def choice(self, iterable):
		random.seed(self.seed)
		result = random.choice(iterable)
		self.seed = random.randint(0, 999999)
		return result