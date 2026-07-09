'''
linguagens=("python", "ruby", "javascript", "perl", "haskell")
print (linguagens)
print (type(linguagens))
print (linguagens[0:2])
print (linguagens[-1])
print (linguagens[:-2])
print (linguagens[:])
linguagens [0] = "C++"
'''
x = (1,2)
y = (3,4)
z = x + y
print (z)

estudante = ("miguel", 29, 1990, "Brasil")       
for e in estudante:
    print(e)
print ([e for e in estudante])
print ('gabriel' in estudante)
print (1990 in estudante)
print ("japão" not in estudante)
print ('Brasil' not in estudante)
print (len(estudante))
del estudante
print (estudante)