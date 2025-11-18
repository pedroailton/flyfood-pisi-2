import random
from deap import base, creator, tools, algorithms

# --- Função de Aptidão (Fitness Function) ---
def _calcularAptidao(individuo, distancias):
    """
    Função interna para calcular o custo (aptidão).
    """
    # O Ponto 'R' é sempre o índice 0 na matriz
    pontoR = 0
    custoTotal = 0
    
    # CORREÇÃO: O AG usa 0..N-1, mas a matriz usa 1..N para os pontos de entrega.
    # Então somamos +1 em todos os índices vindos do indivíduo.
    
    # 1. Custo do 'R' (0) até o primeiro ponto
    primeiroPonto = individuo[0] + 1 
    custoTotal += distancias[(pontoR, primeiroPonto)]
    
    # 2. Custo entre os pontos intermediários
    for i in range(len(individuo) - 1):
        pontoAtual = individuo[i] + 1
        proximoPonto = individuo[i+1] + 1
        custoTotal += distancias[(pontoAtual, proximoPonto)]
        
    # 3. Custo do último ponto de volta para o 'R'
    ultimoPonto = individuo[-1] + 1
    custoTotal += distancias[(ultimoPonto, pontoR)]
    
    return (custoTotal,)

# --- Função Principal de Otimização ---

def otimizarRotaGa(distancias, qtdPontosEntrega, 
                   tamPopulacao=100, 
                   numGeracoes=500, 
                   taxaCrossover=0.8, 
                   taxaMutacao=0.2):
    
    # --- 1. Definição dos Tipos ---
    # (Verifica se já existe para evitar erro de re-criação no notebook/console)
    if not hasattr(creator, "FitnessMin"):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMin)

    # --- 2. Configuração da Toolbox ---
    toolbox = base.Toolbox()
    
    # CORREÇÃO: Genes agora vão de 0 até (qtd - 1). 
    # Ex: se são 4 pontos, índices serão [0, 1, 2, 3]
    indicesPontos = list(range(qtdPontosEntrega)) 

    toolbox.register("genes", random.sample, indicesPontos, len(indicesPontos))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # --- 3. Operadores ---
    toolbox.register("evaluate", _calcularAptidao, distancias=distancias)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # --- 4. Execução ---
    print(f"\nExecutando AG para {qtdPontosEntrega} pontos:")
    print(f" População: {tamPopulacao} | Gerações: {numGeracoes}")
    
    populacaoInicial = toolbox.population(n=tamPopulacao)
    hof = tools.HallOfFame(1) 
    
    algorithms.eaSimple(populacaoInicial, 
                        toolbox, 
                        cxpb=taxaCrossover,
                        mutpb=taxaMutacao,
                        ngen=numGeracoes,
                        halloffame=hof,
                        verbose=True)

    # --- 5. Retorno ---
    melhorIndividuoIndices = hof[0]
    melhorCusto = melhorIndividuoIndices.fitness.values[0]

    return melhorIndividuoIndices, melhorCusto