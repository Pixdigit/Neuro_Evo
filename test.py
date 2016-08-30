# -*- coding: utf-8 -*-
import neter

test_net = neter.create_net(1, 5, 1, seed=1)
print test_net.id
print test_net.compute([200])