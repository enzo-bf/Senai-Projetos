nome = 'enzo'
idade = 18
altura = 1.80
print (nome)
print (idade)
print (altura)

a, b, c = 5, 3.1, "hello"
print (a)
print (b)
print (c)

meuNome = 'Enzo'
minhaIdade = 18
meuEndereco= "Rua Luiz Silveira"

print (meuNome)
print (minhaIdade)
print (meuEndereco)

PI = 3.14
GRAVIDADE = 9.8

print (PI)
print (GRAVIDADE)

v = 1000
print (v)

v= 'eu sou uma string'
print (v)

x = 27
y = 22.2
z = 3j

print (x)
print (y)
print (z)

print (type(x))
print (type(y))
print (type (z))

d = 3
e = 1231089471982549175
f = -100
print (type(d))
print (type(e))
print (type (f))

g = 34.5
h = 1.0
i = 0.33

print (type (g))
print (type (h))
print (type (i))

j =  43e4
l = 3.5e-2
print (type (j))
print (j)
print (type (l))
print (l)
 
print (1.79e308)
print (1.8e308)

print (5e-324)
print (5e-325)

a = 2+4j
b = -3j
c = complex (3,4)
print (type(a))
print (type(b))
print (type(c))

print (c.real)
print  (c.imag)

x = complex (4,4)
y = complex (-1, 4)
z = complex (2.1)

print (x+y)
print (x+1)
print (x*2)

import cmath

print (cmath.phase(x))
print (cmath.phase(complex(-1.0, 0.0)))
print (cmath.phase(complex(-1.0, -0.0)))

import random

print (random.randrange(1,10))

x = 3
y = 7.7
z = 4j

print (type (x))
print (type (y))
print (type (z))

print (complex(x))

print (float(x))
print (int(y))

print (0b01111111)
print (0o10)
print (0xff)

print (int ('0b11111111',2))
print (int ('0xff',16))

print ("podemos usar aspas dentro \"strings\"")
print ('podemos usar aspas dentro das \'strings\'')

print ("dessa forma não há 'problema'")
print ('dessa fomra também não há "problema"')

s = "rafael" 
print (s [0])
print (s [-6])
print (s[5])
print (s[-1])

nome = "john von neumann"
print (nome [5:12])

print (nome [::-1])

nome = " meu nome e Enzo Francisco "
print (nome.strip())

print (len(nome))

print (nome.lower())
print (nome.upper())

print (nome.swapcase())

print (nome.title())

print (nome.replace("Enzo", "ken"))

print (nome.split(" "))

filosofos = ['kant', 'kierkegaard', 'Nietzsche', 'lebiniz']
print (', ' .join (filosofos))
print ('- ' .join (filosofos))

list ('aeiou')
print ('|'.join('aeiou'))

print ("Ra Ra Ja Ra Ta" .count ("Ra"))

print ("existencialismo" .endswith ("exist"))
print ("existencialismo" .endswith ("ismo"))
print ("existencialismo" .startswith ("exist"))
print ("existencialimo".startswith ("ismo"))

print ('Amar, é encontrar a própria felicidade na felicidade alheia' .find('amar'))
print ('Amar, é encontrar a própria felicidade na felicidade alheia' .find('é'))

print ('xyz678' .isalnum())
print ('xyz#678' .isalnum())
print (' ' .isalnum())

print ('exemplo' .isalpha())
print ('exemplo 2' .isalpha())

print ('33'.isdigit())
print ('a33z'.isdigit())
print (' '.isdigit())

print ('nome' .isidentifier())
print ('nome2' .isidentifier())
print ('2nome' .isidentifier())
print ('nome#' .isidentifier())

from keyword import iskeyword 

print (iskeyword ("or"))
print (iskeyword ("else"))
print (iskeyword ("while"))
print (iskeyword ("switch"))

print ('Gabriel\tfelippe'.isprintable())
print ('Gabriel felippe' .isprintable())
print ('' .isprintable())
print ('x\ny' .isprintable())

print (''.isspace())
print ('x'.isspace())
print (' '.isspace())
print ('\t\n'.isspace())

print ("STRING".isupper())
print ("String".isupper())

print ("STRING".islower())
print ("string".islower())

print ('enzo'.center(20))
print ('enzo'.center(25,'.'))

print ('x\n'.expandtabs(10))

print ('c++' .ljust(10))
print ('c++'.ljust (10,'.'))

print ('javascript'.rjust(20))
print ('javascript'.rjust(20,'-'))

print ('67'.zfill(4))

print ('letra'.zfill(7))

nome = "enzo"
profissao = "programador"

print("A profissão de {0} é {1}".format (nome,profissao))

tag = 'p'
texto = 'este é um paragráfo'

setenca = '<{0}>{1}</{0}>'.format(tag,texto)
print (setenca)

valor = '1 GB é igual a {:,}bytes'.format(10**9)
print (valor)

print ("{:d}".format(4))

print ("{:b}".format(55))
print ("{:x}".format(15))

print ("{:}".format([20,30]))

nome = "alan"
amigo = "jones"

print ("%s é amigo de %s" %(nome, amigo))

print ("%d" % (4545))

first_name = "alan"
last_name = "turing"

sentenca = f'meu nome e {first_name.upper()} {last_name.lower()}'
print (sentenca)

pessoa = {'nome': "muhammad", 'idade':22}
setenca = f'meu nome é {pessoa["nome"]} e eu tenho {pessoa["idade"]} anos de idade'

print (setenca)

calculo = f'4 vezes 11 é igual a {4*11}'
print (calculo)

from datetime import datetime
nascimento = datetime(1991, 6, 6)
setenca = f'O nascimento é no dia {nascimento:%B, %d, %y}'
print(setenca)













































































