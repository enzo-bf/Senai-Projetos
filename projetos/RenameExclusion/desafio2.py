import os

pasta_inicial = "temp_logs"
pasta_final = "backup_final"
nome_arquivo = "log_sistema.txt"

try: 
    if not os.path.exists(pasta_inicial):
        os.mkdir(pasta_inicial)
        print(f"diretório '{pasta_inicial}' criado.")
    
    caminho_arquivo_inicial = os.path.join(pasta_inicial, nome_arquivo)
    with open(caminho_arquivo_inicial, "w") as f:
        f.write("Log do erro:falha na conexão as 10:00")
    print(f"Arquivo '{nome_arquivo}' criado dentro de '{pasta_inicial}'.")

    os.rename(pasta_inicial, pasta_final)
    print(f"Pasta renomeada ara '{pasta_final}'.")

    caminho_arquivo_novo = os.path.join(pasta_final, nome_arquivo)

    if os.path.exists(caminho_arquivo_novo):
        os.remove(caminho_arquivo_novo)
        print(f"Arquivo '{nome_arquivo}'removido de dentro de '{pasta_final}'.")
    
    os.rmdir(pasta_final)
    print (f"Pasta '{pasta_final}' removida com sucesso.")

    print("\nProcesso de limpeza concluído!")
except Exception as e:
    print(f"ocorreu um erro: {e}")