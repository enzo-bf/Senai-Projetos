'''
album = {"Nome":"A Night at the Opera", "Artista":"Blind Guardian", "Lançamento":2002}
print(type(album))
print(album)
print(album["Nome"])
print(album["Artista"])
print(album["Lançamento"])

elemento = {
    "Nome":"Ouro",
    "Símbolo":"Au",
    "Número Atômico":79    
}

print(elemento["Nome"])
print(elemento.get("Nome"))

elemento["Nome"] = "Prata"
elemento["Símbolo"] = "Ag"
elemento["Número Atômico"] = 47
print(elemento)

personagem = {
    "nome":"gandalf",
    "classe":"Wizard",
    "ordem":"Istari"
}
for key in personagem:
    print(personagem[key])
    
personagem['altura'] = 1.85
print(personagem)
personagem.pop('altura')
print(personagem)
personagem.popitem()
print(personagem)
del personagem['classe']
print(personagem)
del personagem
print (personagem)

pessoa = dict (nome="Jesus", idade=33)
print(pessoa)

pessoa.update({'nome':'Immanuel'})
print(pessoa)
pessoa.clear()
print(pessoa)
pokedex = [
    {'nome':'pikachu','tipo':'elétrico'},
    {'nome':'charizard','tipo':'fogo'},
    {'nome':'bulbasaur','tipo':'planta'},
    {'nome':'squirtle','tipo':'aquatico'}
]
ordenados = sorted (pokedex, key=lambda x: x['tipo'])
print (ordenados)
autores = ['Aldous Huxley', 'George Orwell', 'Ray Bradbury', 'William Gibson']
livros = ['Brave New World', '1984', 'Fahrenheit 45', 'Neuromancer']
autores_livros = {autor: livro for autor, livro in zip(autores, livros)}
print(autores_livros)

quadrados_pares = {x: x*x for x in range (11) if x %2==0}
print (quadrados_pares)

filme = {'título':'lord of the rings', 'gênero':'Aventura'}
print (filme)
copia_filme = filme.copy()
print(copia_filme)
filme['gênero']='fantasia'
print(copia_filme)
print(filme)
copia_filme = dict(filme)
print(copia_filme)
filme ['título'] = 'the hobbit: An unexpect journey'
print (filme)
print (copia_filme)
'''