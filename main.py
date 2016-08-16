# -*- coding: utf-8 -*-
import net

new_net = net.net(14, 2, 2)
result = new_net.compute([1, 3])
print "Result :" + str(result)
result = new_net.compute([2, 2])
print "Result :" + str(result)
result = new_net.compute([3, 1])
print "Result :" + str(result)
