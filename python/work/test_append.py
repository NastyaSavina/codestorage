my_list = [(1, 2), (3, 4), (5, 6)]
res = []
res = [each for each in my_list if isinstance(each, tuple)]
print(res)