s = "20200301"
s1 = "2020.01.01"

res_s = s[:4] + "-" + s[4:6] + "-" + s[6:]

print(res_s)
print(s1.replace('.','-'))