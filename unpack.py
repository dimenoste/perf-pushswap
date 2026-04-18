size = 100
runs = 6
pushswap = "./pushswap"
algos = ["simple", "medium", "complex"]
arguments = [pushswap, algos, size, runs]
run = [k for k in range(runs)]

#print(list(map(lambda x: (x, arguments), run)))


res = []
for k in range(runs):
    args_with_run = arguments.copy()
    arguments.append(k)
    res.append(args_with_run)

print(res)


algos = ["simple", "medium", "complex"]
arguments_tuple = (pushswap, algos, size, runs)
#print(list(map(lambda x: (x, arguments), run)))

k= 0
for k in range(runs):
    res = re(*arguments_tuple, k)

print(res)