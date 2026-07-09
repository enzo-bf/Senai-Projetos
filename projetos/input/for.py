#for seq in sequencia
    #print (seq)
'''
animais = ['cachorro', 'gatos', 'elefantes']
for animal in animais:
    print (animal)
for string in "programação com python":
    print (string, end='')
x = range (0,10)
print (type(x))
print (list(x))
y=range(4,30,2)
print (list(y))
for i in range(19):
    print(i)
for data in range (1995,2018):
    print(data)
paises=['China', 'India', 'Tailandia']
for pais in paises:
    print(pais)
    if pais == "India":
        break

linguagens = ['C', 'js', 'py', 'lua']
for linguagem in linguagens:
    if linguagem == 'js':
        continue
    print(linguagem)
for x in range (10):
    if x % 2 == 1:
        continue
    print(x)
for x in range (10):
    print (x)
else:
        print("loop finalizado com sucesso")
cores = ['azul','verde','amarelo']
numeros = [1,2,3]

for cor in cores:
    for numero in numeros:
        print (f'{cor.capitalize()} - {numero}')
alimentos = ['arroz','feijao','batata']
for indice,alimento in enumerate(alimentos):
    print (f'{indice}->{alimento}')
for indice,alimento in enumerate(alimentos,10):
    print (f'{indice}->{alimento}')
'''
numero = int(input("Digite um número para saber sua tabuda:"))
for i in range (1,11):
    print (f'{numero} x {i} = {numero*i}')

precos = [19.90, 5.50, 12.00, 45.00, 8.75]
total = 0
for preco in precos:
    total += preco
print("Valor total da compra:", total)
i = 1 
while i < 10:
    print(i)
    i+=1
count = 0
while (count < 5): count +=1; print("hello world")
a = 1
while a < 10:
    print(a)
    if a ==5:
        break
    a +=1
x = 0
while x <10:
    x +=1
    if x ==5:
        continue
    print(x)
n = int(input("informe o número de termos:"))
a,b = 0,1
count = 0
while count<n:
    print (a)
    c = a + b
    a,b = b, c
    count += 1