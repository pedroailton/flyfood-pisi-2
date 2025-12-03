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

def _mutacaoInversao(individuo, indpb):
    """
    Mutação por Inversão (Standard para TSP).
    Seleciona dois pontos aleatórios na rota e inverte o trecho entre eles.
    Isso ajuda a 'descruzar' caminhos no mapa.
    """
    if random.random() < indpb:
        tam = len(individuo)
        if tam < 2: return individuo,
        
        # Escolhe dois índices aleatórios (ex: corte no ponto 5 e no ponto 20)
        a, b = random.sample(range(tam), 2)
        
        # Garante que 'a' seja menor que 'b' para fatiar corretamente
        if a > b:
            a, b = b, a
        
        # Inverte o trecho do meio (slicing do Python [::-1] inverte a lista)
        individuo[a:b+1] = individuo[a:b+1][::-1]
        
    return individuo,

def algoritmo_elitista(pop, toolbox, cxpb, mutpb, ngen, stats=None, halloffame=None, verbose=True):
    """
    Versão personalizada do eaSimple com ELITISMO.
    Garante que o melhor indivíduo da geração anterior seja copiado
    para a próxima geração sem alterações.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Avalia a primeira geração
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(pop)

    record = stats.compile(pop) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose: print(logbook.stream)

    # Começa a evolução
    for gen in range(1, ngen + 1):
        # 1. Seleção (Gera descendentes)
        offspring = toolbox.select(pop, len(pop))
        
        # Clona para não alterar os originais
        offspring = list(map(toolbox.clone, offspring))

        # 2. Aplica Crossover e Mutação
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # 3. Avalia os novos indivíduos
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # 4. Atualiza o Hall of Fame (O melhor de todos os tempos)
        if halloffame is not None:
            halloffame.update(offspring)

        # Substitui o primeiro indivíduo da nova população pelo Melhor de Todos (HoF[0])
        # Isso garante que a melhor solução nunca se perde.
        offspring[0] = toolbox.clone(halloffame[0])
        # ---------------------------------

        # Substitui a população antiga pela nova
        pop[:] = offspring

        # Log e Print
        record = stats.compile(pop) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose: print(logbook.stream)

    return pop, logbook

# --- Função Principal de Otimização ---
def otimizarRotaGa(
    distancias,
    qtd_pontos_entrega,
    tam_populacao=100,
    num_geracoes=150,
    taxa_crossover=0.85,
    taxa_mutacao=0.15
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
    toolbox.register("mutate", _mutacaoInversao, indpb=0.2)
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

    _, logbook = algoritmo_elitista(
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
