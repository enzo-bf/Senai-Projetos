import os

def executar_comando_inseguro (nome_usuario):
    os.system(f"echo {nome_usuario}")