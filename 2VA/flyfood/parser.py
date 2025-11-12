def lerArquivo(caminho_arquivo):
    """
    Lê o conteúdo de um arquivo de texto (.txt) e
    retorna uma lista de linhas.
    """

    linhas = []

    with open(caminho_arquivo, "r", encoding="utf-8") as arq:
        for linha in arq:
            linhas.append(linha.strip())
                
    return linhas

def parseArquivoTsplib(caminho_arquivo):
    """
    Processa o arquivo de entrada e constrói a estrutura de dados principal do programa.
    Retorna o dicionário "distancias" com a chave sendo os dois pontos considerados, sequencialmente, e o valor sendo a distância;
    E retorna a variável "qtd_pontos" com a quantidade de pontos presente no documento (desconsiderando "R")
    """
    linhas = lerArquivo(caminho_arquivo)

    # Identifica os pontos de entrega 
    distancias = {}

    # Verifica a quantidade de elementos a partir dos elementos presentes na primeira linha do arquivo
    elementos_primeira_linha = linhas[0].split(" ")
    qtd_elementos = len(elementos_primeira_linha)

    # Loop de varredura das linhas(i)
    for i in range(0, qtd_elementos-1): # primeira linha -> (quantidade de elementos - 1) pois a última linha nao terá aresta para si própria

        # lista com os elementos da i-ésima linha
        lista = linhas[i].split() # obs: não int ainda

        # Loop de varredura das colunas(j), que começa a partir de i+1 (já que não há distância de i para i)
        for j in range(i+1, qtd_elementos): #colunas i+1 -> quantidade de elementos
            if len(lista) > 0:
                peso = int(lista.pop(0))
            else:
                print(f"Erro! linha {i} do arquivo não possui elementos suficientes")
                exit()
            #gravando a aresta em (i, j) e (j, i), dada a simetria das distâncias:
            distancias[(i,j)] = peso
            distancias[(j,i)] = peso

    qtd_pontos = qtd_elementos - 1 # desconsidera o ponto "R" para posterior print da quantidade de elementos.

    return distancias, qtd_pontos

def parseArquivoMatriz(caminho_arquivo):
    """
    Processa o arquivo de entrada e constrói a estrutura de dados principal do programa.
    Retorna as dimensões da matriz, o conteúdo do mapa e as coordenadas dos pontos de interesse.
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