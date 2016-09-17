import time
import test

start = time.time()
for i in xrange(100):
	test.test_net()
end = time.time()
print(end - start)
