'''
num = int(input("Digite um número: "))

if num > 0:
    print("O número é positivo")
print("Esse valor sempre é impresso, pois está fora do bloco If")

x = 12
y = 12

if x > y:
    print("x é maior do que y")
elif x == y:
    print("x e y são iguais")

a = 100
b = 20

if b > a:
    print("b é maior do que a")
elif b == a:
    print("b e a são iguais")
else:
    print("a é maior do que b")

k = 30
z = 22

if z > k:
    print("z é maior do que k")
else:
    print("k é maior do que z")

num = int(input("Digite um número: "))

if num >= 0:
    if num == 0:
        print("Zero")
    else:
        print("Número Positivo")
else:
    print("Número Negativo")

senha = ''

if not senha:
    print("Senha Inexistente")
else:
    print("Senha Existe")

print(bool(''))
print(bool("75966231325"))

senha = '75966231325'

if not senha:
    print("Senha Inexistente")
else:
    print("Senha Existe")

print(bool(0))
print(bool(1))
print(bool(-1))
print(bool(3.3))
print(bool(3+1j))

n1 = 15
n2 = 30
n3 = 15

if n1 < n2 and n3 == n1:
    print("Ambas as condições são verdadeiras")

if n1 > n2 or n3 == n1:
    print("Pelo menos uma condição é verdadeira")

n = 35

for n in range(1,n):
    if n % 3 is 0 and n % 5 is 0:
        print("FizzBuzz")
    elif n % 3 is 0:
        print("Fizz")
    elif n % 5 is 0:
        print("Buzz")
    else:
        print(n)

'''

from datetime import date

atual = date.today().year
nascimento = int(input('Ano de Nascimento: '))
idade = atual - nascimento

print(f'O atleta tem {idade} anos.')

if idade <= 9:
    print('Classificação: MIRIM')
elif idade <= 14:
    print('Classificação: INFANTIL')
elif idade <= 19:
    print('Classificação: JUNIOR')
elif idade <= 25:
    print('Classificação: SÊNIOR')
else:
    print('Classificação: MASTER')