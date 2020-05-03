my_str = "заборчиком"
print(my_str)

arr = list(my_str)
for i in range(0, len(my_str), 2):
    arr[i] = arr[i].upper()
my_str = ''.join(arr)

print(my_str)