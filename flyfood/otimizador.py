from itertools import permutations

def _calcular_distancia(ponto_a, ponto_b):
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

def _calcular_custo_total_da_rota(rota, pontos):
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
    custo_total += _calcular_distancia(ponto_r, primeiro_ponto)

    # 2. Calcula o custo entre os pontos intermediários da rota
    # O loop vai do primeiro ponto até o penúltimo
    for i in range(len(rota) - 1):
        ponto_atual = pontos[rota[i]]
        proximo_ponto = pontos[rota[i+1]]
        custo_total += _calcular_distancia(ponto_atual, proximo_ponto)

    # 3. Calcula o custo do último ponto da rota de volta para a origem 'R'
    ultimo_ponto = pontos[rota[-1]]
    custo_total += _calcular_distancia(ultimo_ponto, ponto_r)

    return custo_total

def otimizar_rota(pontos):
    """
    parte mais importante
    
    Encontra a rota de menor custo possível que visita todos os pontos de entrega. [cite: 11]
    Utiliza uma abordagem de força bruta, testando todas as permutações possíveis.

    Args:
        pontos (dict): Dicionário com os nomes e coordenadas de todos os pontos, incluindo 'R'.

    Returns:
        str: Uma string com a sequência de pontos da rota otimizada, 
             separada por espaços. Exemplo: "A D C B".
    """
    # 1. Isola os pontos de entrega (todos exceto 'R')
    pontos_de_entrega = [p for p in pontos if p != 'R']
    
    # Se não houver pontos de entrega, retorna uma mensagem
    if not pontos_de_entrega:
        return "Nenhum ponto de entrega foi especificado."

    # 2. Gera todas as sequências (permutações) possíveis para os pontos de entrega
    rotas_possiveis = list(permutations(pontos_de_entrega))
    
    # 3. Inicializa variáveis para acompanhar a melhor rota encontrada até agora
    melhor_rota = None
    menor_custo = float('inf')  # 'inf' representa um número infinito

    # 4. Itera sobre cada rota possível para encontrar a de menor custo
    for rota_atual in rotas_possiveis:
        # Calcula o custo da rota que está sendo verificada
        custo_da_rota_atual = _calcular_custo_total_da_rota(rota_atual, pontos)

        # Se o custo desta rota for menor que o menor custo já registrado,
        # ela se torna a nova melhor rota.
        if custo_da_rota_atual < menor_custo:
            menor_custo = custo_da_rota_atual
            melhor_rota = rota_atual
            
    # 5. Formata a melhor rota encontrada em uma string para exibição
    resultado_formatado = " ".join(melhor_rota)
    
    return resultado_formatado