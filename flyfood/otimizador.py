# Para fazer todas as combinações de pontos possíveis para os pontos na matriz
from itertools import permutations

def extrairPontos(pontos):
    """Funçãozinha auxiliar que filtra e retorna a lista de pontos de entrega (menos o R)."""
    return [p for p in pontos if p != 'R']

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
    rota é uma tupla com os pontos da rota, ex: A, B, C, D
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

# Versão padrão (fast)
def otimizarRota(pontos, mostrar_atualizacoes=False):
    """
    Modo rápido: percorre todas as rotas sem armazená-las e sem rastrear a pior rota.
    Retorna apenas (melhor_rota_formatada, melhor_custo).
    """
    if 'R' not in pontos:
        # Retorna um formato que não quebre o programa principal
        return "ERRO: Ponto de partida 'R' não encontrado no mapa.", 0
    
    # Chama a função auxiliar pra extrair pontos
    pontos_de_entrega = extrairPontos(pontos)

    
    # Se não houver pontos de entrega, retorna uma mensagem
    if not pontos_de_entrega:
        return "Nenhum ponto de entrega foi especificado."
    
    melhor_rota = None
    melhor_custo = float('inf')
    contador = 0

    # Calcula o custo de cada rota possível
    for rota_atual in permutations(pontos_de_entrega):
        # Calcula o custo da rota que está sendo verificada
        custo_da_rota_atual = calcularCustoTotalDaRota(rota_atual, pontos)
       
        if custo_da_rota_atual < melhor_custo:
            melhor_custo = custo_da_rota_atual
            melhor_rota = rota_atual
            contador += 1
            if mostrar_atualizacoes:
                print(f"{contador}ª atualização: {' -> '.join(rota_atual)} | Custo: {custo_da_rota_atual}")
        


    melhor_formatada = " -> ".join(melhor_rota)
    return melhor_formatada, melhor_custo

def otimizarRotaPlus(pontos, mostrar_todas=False):
    """
    Encontra a rota de menor custo possível que visita todos os pontos de entrega. [cite: 11]
    Utiliza uma abordagem de força bruta, testando todas as permutações possíveis.
    """
    if 'R' not in pontos:
        # Retorna um formato que não quebre o programa principal
        return "ERRO: Ponto de partida 'R' não encontrado no mapa.", 0
    
    # Chama função que isola pontos
    pontos_de_entrega = extrairPontos(pontos)

    # Se não houver pontos de entrega, retorna uma mensagem
    if not pontos_de_entrega:
        return "Nenhum ponto de entrega foi especificado."

    # Gera todas as sequências (permutações) possíveis para os pontos de entrega
    resultados= [] #lista com (rota,custo)
    total = 0
    # Calcula o custo de cada rota possível
    for rota_atual in permutations(pontos_de_entrega):
        # Calcula o custo da rota que está sendo verificada
        custo_da_rota_atual = calcularCustoTotalDaRota(rota_atual, pontos)
        resultados.append((rota_atual,custo_da_rota_atual))
        total += custo_da_rota_atual
    # Ordena da menor para a maior distância (custo)
    resultados.sort(key=lambda x: x[1])
    media = total/len(resultados)
    # Exibe todas as rotas avaliadas (caso ativado)
    if mostrar_todas:
        print("\nRotas avaliadas e seus custos:\n")
        for i, (rota, custo) in enumerate(resultados, start=1):
            rota_formatada = " -> ".join(rota)
            print(f"{i:>2}. {rota_formatada} | Custo total: {custo}.")
        print(f'Custo médio: {media} dronômetros')
        print()
    # Guarda melhor e pior rota
    melhor_rota, melhor_custo = resultados[0]
    pior_rota, pior_custo = resultados[-1]

    melhor_formatada = " -> ".join(melhor_rota)
    pior_formatada = " -> ".join(pior_rota)
    return melhor_formatada, melhor_custo, pior_formatada, pior_custo


# Teste de verificação individual do arquivo
if __name__ == "__main__":
    exemplo_pontos = {
        "R": (3, 0),
        "A": (1, 1),
        "B": (3, 2),
        "C": (2, 4),
        "D": (0, 4),
    }

    print("\n=== MODO RÁPIDO ===")
    melhor, mc = otimizarRota(exemplo_pontos, mostrar_atualizacoes=True)
    print(f"\nMelhor rota: {melhor} | Custo: {mc}")

    print("\n=== MODO COMPLETO ===")
    melhor, mc, pior, pc = otimizarRotaPlus(exemplo_pontos, mostrar_todas=True)
    print(f"\nMelhor rota: {melhor} | Custo: {mc}")
    print(f"Pior rota: {pior} | Custo: {pc}")