def ler_conteudo_arquivo(caminho_do_arquivo):
    try:
        with open(caminho_do_arquivo, "r", encoding="UTF-8") as arquivo:
            for linha in arquivo:
                linhas = [linhas.strip()]
    
    except FileNotFoundError:
        print(f"ERRO: O arquivo no caminho {caminho_do_arquivo} não foi encointrado.")
        raise


def parse_arquivo(caminho_do_arquivo):
    # Lógica para processar o conteúdo e mapear os pontos...
    # Exemplo:
    # conteudo = _ler_conteudo_arquivo(caminho_do_arquivo)
    # ... processa o conteudo ...
    # return {'R': (3, 0), 'A': (1, 1), ...}
    pass