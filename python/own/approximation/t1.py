import re

s = '/linkp1/linkp2?112233=12345'
my_re = '(\\/+)?(\\?.*?)?$'

r = re.compile(my_re)

test = re.sub(my_re, '', s)

print(test)

