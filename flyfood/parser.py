def lerArquivo(caminho_arquivo):
    """
    Lê o conteúdo de um arquivo de texto e retorna uma lista de linhas.
    Args:
        caminho_arquivo (str): Caminho para o arquivo .txt contendo a matriz.
    Returns:
        list[str]: Lista de linhas do arquivo sem quebras de linha.
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as arq:
        linhas = [linha.strip() for linha in arq.readlines()]
    return linhas


def parseArquivo(caminho_arquivo):
    """
    Processa o arquivo de entrada e retorna uma estrutura com a matriz e os pontos.
    Args:
        caminho_arquivo (str): Caminho para o arquivo .txt contendo a matriz.
    Returns:
        dict: Estrutura com dimensões, matriz e coordenadas dos pontos.
    """
    linhas = lerArquivo(caminho_arquivo)

    # Lê e guarda as dimensões da matriz 
    num_linhas, num_colunas = map(int, linhas[0].split())

    # Monta a matriz 
    matriz = []
    for linha in linhas[1:]:
        matriz.append(linha.split())

    # Identifica os pontos de entrega 
    pontos = {}
    for i in range(num_linhas):
        for j in range(num_colunas):
            valor = matriz[i][j]
            if valor != "0":
                pontos[valor.upper()] = (i, j)

    return {
        "num_linhas": num_linhas,
        "num_colunas": num_colunas,
        "matriz": matriz,
        "pontos": pontos
    }
    
    
# Teste de verificação
if __name__ == "__main__":
    resultado = parseArquivo("flyfood-pisi-2/flyfood/entrada.txt")
    print("Dimensões:", resultado["num_linhas"], "x", resultado["num_colunas"])
    print("Matriz:")
    for linha in resultado["matriz"]:
        print(linha)
    print("Pontos:", resultado["pontos"])