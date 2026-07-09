'''

s = {1,1,2,3,3,4}
print(type(s))
print(s)

k = set([1,2,3,4,5])
print(type(k))
print(k)

for itens in k:
    print(itens)

k.add(8)
print(k)

k.discard(1)
print(k)

k.clear()
print(k)

print(set("cachorro"))

print(len(set("cachorro")))

'''

x = {1,2,3}
y = {2,3,4}

print (x & y)
print (x.intersection(y))
print ( x - y)
print (x. difference(y))
print (y - x)
print (y.difference(x))
print (x.symmetric_difference(y))
print (y.symmetric_difference(x))
print (x ^ y)
print (y ^x)
print (x | y)
print (x.union(y))
print (1 in x )
print (5 in x )
print (10 not in x)
print (1 not in x)


