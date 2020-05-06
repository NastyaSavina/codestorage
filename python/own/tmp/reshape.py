from numpy import core as np, savetxt, loadtxt

arr = np.arange(200).reshape((2, 5, 4, 5))

with open('/Users/me/Documents/code/python/own/tmp/rse.txt', "w+") as f:
    for each_3d in arr:
        for each_2d in each_3d:
            savetxt(f, each_2d)

with open('/Users/me/Documents/code/python/own/tmp/rse.txt', "r+") as f:
    other_arr = loadtxt(f)
    reshaped_arr = other_arr.reshape((2, 5, 4, 5))

    print(reshaped_arr)