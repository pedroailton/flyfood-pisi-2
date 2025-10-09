from itertools import permutations

def calcularDistancia(ponto_a, ponto_b):
    """
    Calcula a distância de Manhattan entre dois pontos em uma grade.
    ponto_a e b são tuplas com as posições dos 2 pontos"""

    
    # Desempacota as tuplas
    linha1, coluna1 = ponto_a
    linha2, coluna2 = ponto_b
    
    # Calcula a distância de Manhattan: |x2 - x1| + |y2 - y1|
    distancia = abs(linha2 - linha1) + abs(coluna2 - coluna1)
    
    #retorna distancia de a e b
    return distancia

def calcularCustoTotalDaRota(rota, pontos):
    """
    Calcula o custo total de uma rota específica, começando e terminando no ponto 'R'.

    rota é uma tupla com os pontos da rota, ex: A, B, D, C
    pontos é um dicionário que mapeia o nome de cada ponto às suas coordenadas, ex: R: (3, 0), A: (1, 1)...
    """
    # Ponto de origem e retorno 
    ponto_r = pontos['R']
    custo_total = 0

    # 1. Calcula o custo da origem 'R' até o primeiro ponto da rota
    primeiro_ponto = pontos[rota[0]]
    custo_total += calcularDistancia(ponto_r, primeiro_ponto)

    # 2. Calcula o custo entre os pontos intermediários da rota
    # O loop vai do primeiro ponto até o penúltimo
    for i in range(len(rota) - 1):
        ponto_atual = pontos[rota[i]]
        proximo_ponto = pontos[rota[i+1]]
        custo_total += calcularDistancia(ponto_atual, proximo_ponto)

    # 3. Calcula o custo do último ponto da rota de volta para a origem 'R'
    ultimo_ponto = pontos[rota[-1]]
    custo_total += calcularDistancia(ultimo_ponto, ponto_r)

    return custo_total

def otimizarRota(pontos, melhores_rotas=False):
    """
    parte mais importante
    
    Encontra a rota de menor custo possível que visita todos os pontos de entrega. [cite: 11]
    Utiliza uma abordagem de força bruta, testando todas as permutações possíveis.
    """
    # 1. Isola os pontos de entrega (todos exceto 'R')
    pontos_de_entrega = []

    for p in pontos:
        if p != 'R':  # verifica se o elemento não é 'R'
            pontos_de_entrega.append(p)
    
    # Se não houver pontos de entrega, retorna uma mensagem
    if not pontos_de_entrega:
        return "Nenhum ponto de entrega foi especificado."

    # Gera todas as sequências (permutações) possíveis para os pontos de entrega
    rotas_possiveis = list(permutations(pontos_de_entrega))
    
    melhor_rota = None
    menor_custo = float('inf')  # 'inf' representa um número infinito
    contador_de_melhores_rotas = 0

    for rota_atual in rotas_possiveis:
        # Calcula o custo da rota que está sendo verificada
        custo_da_rota_atual = calcularCustoTotalDaRota(rota_atual, pontos)

        # Se o custo desta rota for menor que o menor custo já registrado,
        # ela se torna a nova melhor rota.
        if custo_da_rota_atual < menor_custo:
            menor_custo = custo_da_rota_atual
            melhor_rota = rota_atual

            contador_de_melhores_rotas += 1
            if melhores_rotas: # se o parâmetro for passado na chamada de função
                melhor_rota_formatada = " ".join(melhor_rota)
                print(f"{contador_de_melhores_rotas}ª atualização da melhor rota: {melhor_rota_formatada}")
            
    # Formata a melhor rota encontrada em uma string para exibição
    resultado_formatado = " ".join(melhor_rota)
    
    return resultado_formatado
