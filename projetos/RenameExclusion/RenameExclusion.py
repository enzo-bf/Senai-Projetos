import os
arquivo_inicial="notas_temporarias.txt"
arquivo_final="relatorio_final.txt"

try:
    
    with open(arquivo_inicial, "w") as f:
        f.write("Conteúdo importante do relatório.")
    print(f"arquivo renomeado para '{arquivo_final}'")

    if os.path.exists(arquivo_inicial):
        os.rename(arquivo_inicial, arquivo_final)
        print(f"arquivo renomeado para '{arquivo_final}'")
    else:
        print(f"Erro: O arquivo '{arquivo_inicial}' não foi encontrado.")
    
    print(f'O arquivo {arquivo_final} está pronto para ser enviado.')

    os.remove(arquivo_final)
    print(f"arquivo '{arquivo_final}' excluído para limpeza de sistema.")

    if not os.path.exists(arquivo_final):
        print("Sucesso: a pasta está limpa.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")        