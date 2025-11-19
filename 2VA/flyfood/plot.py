import matplotlib.pyplot as plt
import numpy as np

def plotar_evolucao(logbook, salvar=False, nome_arquivo="evolucao_custo.png"):
    """
    Plota o gráfico de linha mostrando a evolução do custo ao longo das gerações.
    
    Args:
        logbook: Objeto Logbook do DEAP contendo o histórico.
        salvar (bool): Se True, salva a imagem em disco.
        nome_arquivo (str): Nome do arquivo para salvar.
    """
    # Extrai dados do logbook
    gen = logbook.select("gen")
    min_fit = logbook.select("min")
    avg_fit = logbook.select("avg")

    plt.figure(figsize=(10, 6))
    
    # Plota Média e Mínimo
    plt.plot(gen, min_fit, 'b-', label="Melhor Custo (Mínimo)", linewidth=2)
    plt.plot(gen, avg_fit, 'r--', label="Custo Médio", alpha=0.7)
    
    plt.title("Evolução do Algoritmo Genético (Convergência)", fontsize=14)
    plt.xlabel("Geração", fontsize=12)
    plt.ylabel("Custo (Distância)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=300)
        print(f"Gráfico de evolução salvo como '{nome_arquivo}'")
    
    plt.show()

def plotar_rota(melhor_individuo, coordenadas, salvar=False, nome_arquivo="mapa_rota.png"):
    """
    Plota a rota física em um plano 2D.
    
    Args:
        melhor_individuo (list): Lista de índices retornada pelo AG (ex: [0, 2, 1]).
        coordenadas (dict/list): Dicionário onde chave é o ID do ponto e valor é (x, y).
                                 Ex: {0: (10,20), 1: (30,50)...}
                                 Assumindo que 0 é o Ponto de Partida (Restaurante).
        salvar (bool): Se True, salva a imagem.
    """
    plt.figure(figsize=(10, 10))
    
    # --- Construção do Caminho (X e Y) ---
    x_path = []
    y_path = []

    # 1. Começa no Ponto R (Índice 0 nas coordenadas)
    x_path.append(coordenadas[0][0])
    y_path.append(coordenadas[0][1])

    # 2. Adiciona os pontos intermediários
    # ATENÇÃO: Se o AG retorna indices 0, 1, 2... referentes aos pontos de entrega,
    # e no seu mapa os pontos de entrega são 1, 2, 3... (porque 0 é o R), some +1.
    for gene in melhor_individuo:
        idx_real = gene + 1  # Ajuste conforme sua lógica de indexação
        x_path.append(coordenadas[idx_real][0])
        y_path.append(coordenadas[idx_real][1])

    # 3. Fecha o ciclo voltando ao R
    x_path.append(coordenadas[0][0])
    y_path.append(coordenadas[0][1])

    # --- Plotagem ---
    # Linha da rota
    plt.plot(x_path, y_path, 'o-', color='royalblue', zorder=1, label='Rota Otimizada')
    
    # Destacar Ponto Inicial (Restaurante)
    plt.scatter(x_path[0], y_path[0], color='green', s=200, marker='*', label='Início/Fim', zorder=3)
    
    # Anotar a ordem de visita (opcional, ajuda a visualizar o fluxo)
    for i in range(len(x_path)-1):
        # Pega o ponto médio para colocar a seta ou número
        meio_x = (x_path[i] + x_path[i+1]) / 2
        meio_y = (x_path[i] + y_path[i+1]) / 2
        plt.text(meio_x, meio_y, f'{i+1}º', fontsize=8, color='darkred', fontweight='bold')

    plt.title(f"Melhor Rota Encontrada (AG)", fontsize=14)
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend()
    plt.grid(True)

    if salvar:
        plt.savefig(nome_arquivo, dpi=300)
        print(f"Gráfico do mapa salvo como '{nome_arquivo}'")

    plt.show()