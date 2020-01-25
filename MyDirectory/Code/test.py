from time import time

times = 10000000
i = 0
add = 2
st = time()
for _ in range(times):
	i += add
print("Total time: %s" % (time() - st))# Total time: 1.3392999172210693
