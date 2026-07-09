'''
L = ["M", "o", "n", "t", "y", " ", "P", "y", "t", "h", "o", "n"]
print(L)

print(len(L))
print(L[6:12])
print(L[-12:-7])

nome = ''.join(L)
print(nome)

ciencias = ['física', 'química', 'matemática']
numeros = [1,2,3,4,5,6,7,8,9,10]
hibrida = [1,2.3,"Rafael"]

print(ciencias[0:2])
print(numeros[2])
print(hibrida[-1])
print(ciencias[:])
print(numeros[:6])
print(numeros[2:])
print(numeros[0:10:2])
print(ciencias[slice(0,2)])
print(numeros[slice(0,10,2)])
ciencias[0] = "computação"
print(ciencias[0])

ciencias += ['astronomia', 'biologia']
print(ciencias)

for n in numeros:
    print(n)

print("química" in ciencias)
print("cosmologia" in ciencias)

numeros.append(11)
print(numeros)

numeros.extend([12,13])
print(numeros)

hibrida.insert(0, "Gabriel")
print(hibrida)

lista = [2,1,3,6,3,7,0]
print(lista)
lista.remove(2)
print(lista)
lista.remove(3)
print(lista)
del(lista[1])
print(lista)
lista.pop()
print(lista)

ciencias.remove("química")
print(ciencias)

del ciencias[0]
print(ciencias)

ciencias.pop()
print(ciencias)

ciencias.clear()
print(ciencias)

pares = list((2,4,6,8))
print(pares)

primos = [2,7,11,13,17]
negativos = [-1,-2,-5,-8,-3]
reais = [1.5,3.7,3/4,1,-0.1]

concat = primos + negativos
print(concat)

print(primos*2)

reais.sort()
print(reais)
print(sorted(negativos))
print(sorted(negativos, reverse=True))

total = 0
for i in range(len(primos)):
    total += primos[i]
print(total)

total = 0
for i in primos:
    total += i
print(total)

valores = [-5,7,1,0,10,100,33,2]
quadrados = []
for v in valores:
        quadrados.append(v**2)
print(quadrados)
print([v**2 for v in valores])

print ([v for v in valores if v%2==0])
print([v for v in valores if v > 0])
print([v for v in valores if v <= 0 ])

matriz = [[i for i in range (5)] for _ in range (6)]
print (matriz)

celsius = [33.2, 26.7, 38.5, 40.8]
fahrenheit = [((float (9)/5)*t + 32) for t in celsius]
print (fahrenheit)

animais = ['gato', 'cachorro', 'lagarto']
alimentos = ['tomate', 'alface', 'abacate']
print ([(animal,alimento) for animal in animais for alimento in alimentos])

#from math import sqrt
#print ([sqrt (n) for n in range (1000)])

soma = sum([n for n in range (37)])
print (soma)
'''
print ([x for x in range (2,50) if all (x % y != 0 for y in range (2,x))])
