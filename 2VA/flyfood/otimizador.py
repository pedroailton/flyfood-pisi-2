import random
import numpy as np
from deap import base, creator, tools, algorithms

# --- Função de Aptidão (Fitness Function) ---
def _calcularAptidao(individuo, distancias):
    """
    Função interna para calcular o custo (aptidão).
    """
    # O ponto 'R' é sempre o índice 0 na matriz
    ponto_r = 0
    custo_total = 0

    # CORREÇÃO: O AG usa 0..N-1, mas a matriz usa 1..N para os pontos de entrega.
    # Então somamos +1 em todos os índices vindos do indivíduo.

    # 1. Custo do 'R' (0) até o primeiro ponto
    primeiro_ponto = individuo[0] + 1
    custo_total += distancias[(ponto_r, primeiro_ponto)]

    # 2. Custo entre os pontos intermediários
    for i in range(len(individuo) - 1):
        ponto_atual = individuo[i] + 1
        proximo_ponto = individuo[i + 1] + 1
        custo_total += distancias[(ponto_atual, proximo_ponto)]

    # 3. Custo do último ponto de volta para o 'R'
    ultimo_ponto = individuo[-1] + 1
    custo_total += distancias[(ultimo_ponto, ponto_r)]

    return (custo_total,)


# --- Função Principal de Otimização ---
def otimizarRotaGa(
    distancias,
    qtd_pontos_entrega,
    tam_populacao=100,
    num_geracoes=500,
    taxa_crossover=0.8,
    taxa_mutacao=0.2
):
    """
    Executa o Algoritmo Genético para encontrar a melhor rota, dentro de um determinado intervalo de gerações.
    """

    # --- 1. Definição dos Tipos ---
    # (Verifica se já existe para evitar erro de re-criação no notebook/console)
    if not hasattr(creator, "FitnessMin"):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMin)

    # --- 2. Configuração da Toolbox ---
    toolbox = base.Toolbox()

    # Genes vão de 0 até (qtd - 1).
    # Ex: se são 4 pontos, índices serão [0, 1, 2, 3]
    indices_pontos = list(range(qtd_pontos_entrega))

    toolbox.register("genes", random.sample, indices_pontos, len(indices_pontos))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # --- 3. Operadores ---
    toolbox.register("evaluate", _calcularAptidao, distancias=distancias)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Isso cria o monitoramento igual ao notebook enviado
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    # --- 4. Execução ---
    print(f"\nExecutando AG para {qtd_pontos_entrega} pontos:")
    print(f" População: {tam_populacao} | Gerações: {num_geracoes}")
    
    populacao_inicial = toolbox.population(n=tam_populacao)
    hof = tools.HallOfFame(1)

    _, logbook = algorithms.eaSimple(
        populacao_inicial,
        toolbox,
        cxpb=taxa_crossover,
        mutpb=taxa_mutacao,
        ngen=num_geracoes,
        halloffame=hof,
        stats=stats,
        verbose=True
    ) # Ignora-se o primeiro retorno da função eaSimple() com um underline, para ficar evidente

    # --- 5. Retorno ---
    melhor_individuo_indices = hof[0]
    melhor_custo = melhor_individuo_indices.fitness.values[0]

    return melhor_individuo_indices, melhor_custo, logbook
