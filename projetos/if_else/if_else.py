'''
num = int(input("digite um número:"))
if num > 0:
    print ("o número é positivo")
elif num < 0:
    print ("o número é negativo")
print ("esse valor é sempre impresso, pois esta fora do bloco if")

x = int(input("digite um número para X:"))
y = int(input("digite um número y:"))
if x > y:
    print ("x é maior que y")
elif x == y:
    print ("x e y possuem o mesmo valor")
else: 
    print ("y é menor que x")
a = int(input("digite um número para A:"))
b = int(input("digite um número para B:"))
if b>a:
    print ("b é maior do que a")
elif b == a:
    print ("b e a são iguais")
else:
   print ("a é maior do que b")

k = 30 
z = 22
if z>k:
    print("z é maior do que k")
else: 
    print("k é maior do que z")
num = int(input("digite um número aqui:"))
if num>=0:
    if num == 0:
        print("ZERO REDONDO")
    else: 
        print("Número positivo")
else:
    print("número negativo")

senha = '75966231325'
if not senha:
    print ('senha inexistente')
else: 
    print ('senha existe!')
print (bool(''))
print(bool('75966231325'))
print (bool(0))
print (bool(1))
print (bool(-1))
print (bool(3.3))
print (bool(3+1j))
print (bool())
n1 = 15
n2 = 30
n3 = 15
if n1<n2 and n3 == n1:
    print ("ambas as condições são verdadeiras")
if n1 > n2 or n1 == n3:
    print ("pelo menos uma condição é verdadeira")

n = 35
for n in range (1,n):
    if n % 3 is 0 and n % 5 is 0:
        print ("FizzBuzz")
    elif n % 3 is 0:
        print ("Fizz")
    elif n % 5 is 0:
        print ("buzz")
    else: 
        print (n)
'''
from datetime import date

atual = date.today().year
nascimento = int(input('ano de nascimento:'))
idade = atual - nascimento
print (f'o atleta tem {idade} anos e é considerado:')
if idade <= 9:
    print("mirim")
elif idade<=14:
    print("infantil")
elif idade<=19:
    print("junior")
elif idade <=25:
    print("senior")
else:
    print("master")