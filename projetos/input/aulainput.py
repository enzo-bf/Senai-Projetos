'''
n = input("insira um número: ")
print (n)

print(type(n))

m = int(input("insira um número: "))
print(type(m))

altura = float(input("digite a sua altura(em metros): "))
print(type(altura))

idade = int(input("digite sua idade: "))
print("Sua idade é", idade)


a = int(input("digite o primeiro número: "))
b = int(input("digite o segundo número: "))
print (a + b)



metros = float(input("digite um valor em metros: "))
cm = metros * 100
print (cm)

n = int(input("digite um número: "))
print (n**2)

a, b = input("digite dois números separados por espaço: ").split()
a = int(a)
b = int(b)
print (a + b)

a, b = input("digite dois números separados por virgula).split(",")
a = int(a)
b = int(b)
print (a * b)

x = 10
y = 6
z = 6.0
print("x + y = ", x+y)
print("x - y = ", x-y)
print("x * y = ", x*y)
print("x / y = ", x/y)
print(" x // y = ", x//y)
print("x ** y ", x**y)

a = 1 
a +=3
print(a)
'
x = 12 
y = 3
print(x>y)
print(x<y)
print(x==y)
print(x!=y)
print(x>=y)
print(x<=y)

n1, n2, n3 = 3, 6, 7
print (n1 < n2 and n1 < n3)
print (n1 == n2 or n3 == n2)
print (not True)

x = 1
y = 1
print (x is y)
print (x is not y)

x = "cachorro"
y = "cachorro"
print (x is y)
print (x is not y)
'''
a = [1,2,3]
b = "guilherme"

print(1 in a )
print ("o" in b)