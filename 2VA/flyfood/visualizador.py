import matplotlib.pyplot as plt
import numpy as np

def plotar_dados_logbook(logbook, save_path="grafico_convergencia.png"):
    """
    Plota o gráfico de evolução do Algoritmo Genético baseado nos dados do Logbook.
    Gera linhas para: Média e Melhor Caso (Mínimo).
    """
    # Extrai os dados do logbook (lista de dicionários)
    gen = logbook.select("gen")
    min_vals = logbook.select("min")
    avg_vals = logbook.select("avg")

    plt.figure(figsize=(10, 6))
    
    # Plota a média da população (linha tracejada laranja)
    plt.plot(gen, avg_vals, label="Média da População", color="orange", linestyle="--", alpha=0.7)
    
    # Plota o melhor indivíduo (linha sólida azul)
    plt.plot(gen, min_vals, label="Melhor Solução (Mínimo)", color="blue", linewidth=2)

    # Configurações visuais para o relatório
    plt.title("Convergência do Algoritmo Genético (TSP)", fontsize=14, fontweight='bold')
    plt.xlabel("Gerações", fontsize=12)
    plt.ylabel("Custo Total (Distância Manhattan)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    print(f"-> Salvando gráfico de convergência em: {save_path}")
    plt.savefig(save_path, dpi=300) # dpi=300 garante alta qualidade para impressão/PDF
    plt.close() # Fecha para não sobrepor gráficos futuros

def plotar_mapa_flyfood(coords, rota_indices, nomes_mapa, save_path="mapa_rota.png"):
    """
    Plota a rota final em um grid 2D simulando o mapa do FlyFood.
    
    :param coords: Dicionário {'Nome': (linha, coluna)} vindo do arquivo original.
    :param rota_indices: Lista de índices [0, 2, 1...] retornada pelo AG.
    :param nomes_mapa: Dicionário {0: 'R', 1: 'A'...} para traduzir índices.
    """
    if not coords:
        print("[Aviso] Coordenadas originais não encontradas. Mapa 2D não será gerado.")
        return

    # Traduzir a rota de índices para Nomes (ex: 'R', 'A', 'B')
    # O AG retorna índices 0..N-1 que mapeiam para os pontos de entrega.
    # Precisamos garantir que o 'R' (ponto 0 no mapa_nomes ou via coords) seja o início e fim.
    
    rota_nomes = []
    
    # Adiciona Ponto de Partida (assumindo 'R')
    rota_nomes.append("R")
    
    # Adiciona os pontos intermediários
    for idx in rota_indices:
        # O AG usa índices 0, 1, 2... precisamos pegar o nome correspondente
        # Se seu mapa_nomes usa chaves 1, 2, 3... ajustamos aqui:
        nome = nomes_mapa.get(idx + 1, f"?{idx}?") 
        rota_nomes.append(nome)
        
    # Fecha o ciclo
    rota_nomes.append("R")

    # Extrai X (coluna) e Y (linha) para o plot
    x_val = []
    y_val = []
    
    for nome in rota_nomes:
        if nome in coords:
            l, c = coords[nome]
            x_val.append(c) # Coluna no eixo X
            y_val.append(l) # Linha no eixo Y
        else:
            print(f"[Aviso] Ponto {nome} não encontrado nas coordenadas.")

    plt.figure(figsize=(8, 8))
    
    # Desenha o caminho (linhas)
    # Nota: Usamos 'steps-mid' ou plot direto. Como é Manhattan, plot direto é aceitável
    # se entendermos que o drone só anda em L, mas visualmente a linha reta polui menos.
    plt.plot(x_val, y_val, color='gray', linestyle='--', alpha=0.5, zorder=1)
    
    # Desenha as setas de direção
    for i in range(len(x_val) - 1):
        # Apenas desenha seta se os pontos não forem idênticos
        if x_val[i] != x_val[i+1] or y_val[i] != y_val[i+1]:
            mid_x = (x_val[i] + x_val[i+1]) / 2
            mid_y = (y_val[i] + y_val[i+1]) / 2
            dx = (x_val[i+1] - x_val[i]) * 0.1 # reduz tamanho da seta
            dy = (y_val[i+1] - y_val[i]) * 0.1
            
            plt.arrow(x_val[i], y_val[i], 
                      (x_val[i+1]-x_val[i])*0.95, (y_val[i+1]-y_val[i])*0.95,
                      head_width=0.3, color='blue', length_includes_head=True, zorder=2)

    # Desenha os Pontos
    for nome, (l, c) in coords.items():
        cor = 'red' if nome == 'R' else 'green'
        tamanho = 150 if nome == 'R' else 100
        plt.scatter(c, l, c=cor, s=tamanho, zorder=3, edgecolors='black')
        plt.text(c, l - 0.4, nome, fontsize=12, ha='center', fontweight='bold')

    plt.title(f"Melhor Rota: {' -> '.join(rota_nomes)}", fontsize=11)
    plt.xlabel("Coluna (X)")
    plt.ylabel("Linha (Y)")
    
    # Inverte o eixo Y para ficar igual à matriz (linha 0 no topo)
    plt.gca().invert_yaxis() 
    plt.grid(True)
    
    print(f"-> Salvando mapa da rota em: {save_path}")
    plt.savefig(save_path, dpi=300)
    plt.close()