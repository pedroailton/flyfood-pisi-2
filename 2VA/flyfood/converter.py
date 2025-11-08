import os

def coletarPontos(matriz):
    """
    Coleta todos os pontos do grid (exceto '0') e retorna:
    - pontos: lista ordenada com 'R' primeiro e os demais em ordem alfabética
    - coords: dicionário {pontos: (linha, coluna)}
    """
    coords = {}
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor != "0":
                coords[valor.upper()] = (i, j)

    if "R" not in coords:
        raise ValueError("Ponto inicial 'R' não encontrado na matriz.")

    pontos = ["R"]
    outros = sorted([p for p in coords.keys() if p != "R"]) # cria uma lista dos pontos e coloca em ordem
    pontos.extend(outros)

    return pontos, coords


def calcularDistancia(p1, p2):
    """Calcula a distância Manhattan entre dois pontos (tuplas)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def construirMatrizDistancias(pontos, coords):
    """
    Monta uma matriz com as distâncias entre todos os pontos.
    """
    n = len(pontos)  # quantidade total de pontos
    D = []  # matriz de distâncias

    # cria uma matriz n x n com zeros
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(0)
        D.append(linha)

    # preenche a parte de cima da matriz
    for i in range(n):
        for j in range(i + 1, n):  # começa no i+1 pra não repetir os pares
            p1 = coords[pontos[i]]
            p2 = coords[pontos[j]]
            dist = calcularDistancia(p1, p2)
            D[i][j] = dist
            D[j][i] = dist  # espelha o valor

    return D

def salvarUpperRow(D, caminho_saida):
    """
    Salva apenas a parte superior da matriz (acima da diagonal principal)
    no formato TSPLIB.
    """
    with open(caminho_saida, "w", encoding="utf-8") as arq:
        n = len(D)
        for i in range(n - 1):
            linha = " ".join(str(D[i][j]) for j in range(i + 1, n))
            arq.write(linha + "\n")


def salvarMapeamento(pontos, caminho_mapa):
    """
    Salva um arquivo de mapeamento índice → rótulo.
    """
    with open(caminho_mapa, "w", encoding="utf-8") as arq:
        for i, rotulo in enumerate(pontos, start=1):
            arq.write(f"{i} {rotulo}\n")


def converterGridParaUpperRow(dados_parse, pasta_saida="saida"):
    """
    Função principal da conversão.
    Recebe o resultado de parseArquivo() e gera:
      - um arquivo .upper.txt com as distâncias
      - um arquivo .map.txt com o mapeamento dos rótulos
    """
    os.makedirs(pasta_saida, exist_ok=True)

    matriz = dados_parse["matriz"]
    pontos, coords = coletarPontos(matriz)
    D = construirMatrizDistancias(pontos, coords)

    nome_base = os.path.splitext(os.path.basename(dados_parse.get("origem", "matriz")))[0]
    caminho_upper = os.path.join(pasta_saida, f"{nome_base}.upper.txt")
    caminho_map = os.path.join(pasta_saida, f"{nome_base}.map.txt")

    salvarUpperRow(D, caminho_upper)
    salvarMapeamento(pontos, caminho_map)

    print("\nConversão concluída com sucesso!")
    print(f"  Pontos detectados: {len(pontos)} ({', '.join(pontos)})")
    print(f"  Arquivo upper-row salvo em: {caminho_upper}")
    print(f"  Arquivo de mapeamento salvo em: {caminho_map}\n")

    return caminho_upper, caminho_map
