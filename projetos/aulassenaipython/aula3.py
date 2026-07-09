'''
l = ['m','o','n','t','y',' ','p','y','t','h','o','n']
print (l)

print(len(l))
print(l[6:10])
print(l[-12:-7])

nome = ''.join(l)
print(nome)

ciencias = ['física','química','matemática']
numeros = [1,2,3,4,5,6,7,8,9,10]
hibrida = [1, 2.3, "Rafael"]

print(ciencias[0:2])
print(numeros[2])
print(hibrida[-1])
print(ciencias[:])
print(numeros[:6])
print(numeros[2:])
print(numeros[0:10:2])
print(ciencias[slice(0,2)])
print(numeros[slice(0,10,2)])

ciencias[0]="computação"
print(ciencias[0])
ciencias += ['astronomia','biologia']
print(ciencias)

for n in numeros: 
    print (n)
print ("química" in ciencias)
print ("cosmologia" in ciencias)

numeros.append(11)
print(numeros)

numeros.extend([12,13])
print(numeros)

hibrida.insert(0,"gabriel")
print(hibrida)


lista = [2, 1, 3, 6, 3, 7, 0]
print(lista)
lista.remove(2)
print(lista)
lista.remove(3)
print(lista)
del(lista[1])
print(lista)
lista.pop()

ciencias.remove("química")
print(ciencias)

del ciencias [0]
print(ciencias)

ciencias.pop()
print(ciencias)

ciencias.clear()
print(ciencias)

pares = list((2,4,6,8))
print(pares)

primos = [2,7,11,13,17]
negativos = [-1,-2,-5,-8,-3]
reais = [1.5, 3.7, 3/4, 1, -0.1]

concat = primos + negativos
print (concat)

print(primos*2)

reais.sort()
print (reais)

print ((sorted(negativos)))
print ((sorted(negativos, reverse=True)))

total=0
for i in range(len(primos)):
    total +=primos[i]
print (total)
'''
