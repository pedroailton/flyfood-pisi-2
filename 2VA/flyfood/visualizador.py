import matplotlib.pyplot as plt
import numpy as np

def plotarDadosLogbook(logbook, save_path="grafico_convergencia.png"):
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

def plotarMapaFlyfood(coords, rota_indices, nomes_mapa, save_path="mapa_rota.png"):
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

    plt.figure(figsize=(10, 10)) # Aumentei um pouco para caber melhor os "cotovelos"

    # 2. Desenhar o trajeto Ponto a Ponto (Estilo Manhattan)
    for i in range(len(rota_nomes) - 1):
        nome_atual = rota_nomes[i]
        nome_prox = rota_nomes[i+1]

        if nome_atual in coords and nome_prox in coords:
            # Coordenadas: (Linha, Coluna) -> Matplotlib usa (X=Coluna, Y=Linha)
            l1, c1 = coords[nome_atual]
            l2, c2 = coords[nome_prox]

            # Lógica Manhattan: Primeiro move Horizontal, depois Vertical
            # Ponto 1: (c1, l1)
            # Ponto Intermediário (Cotovelo): (c2, l1) -> Mantém linha, muda coluna
            # Ponto 2: (c2, l2)
            
            # Arrays para plotagem do segmento
            x_seg = [c1, c2, c2]
            y_seg = [l1, l1, l2]
            
            # Plota a linha tracejada (caminho do drone)
            plt.plot(x_seg, y_seg, color='gray', linestyle='--', alpha=0.5, zorder=1)
            
            # Adiciona uma seta no meio do segmento horizontal (se houver movimento)
            if c1 != c2:
                mid_x = (c1 + c2) / 2
                mid_y = l1
                dx = (c2 - c1) * 0.001 # Apenas para dar direção à seta
                plt.arrow(mid_x, mid_y, dx, 0, head_width=0.2, color='blue', length_includes_head=True, zorder=2)
            
            # Adiciona uma seta no meio do segmento vertical (se houver movimento)
            if l1 != l2:
                mid_x = c2
                mid_y = (l1 + l2) / 2
                dy = (l2 - l1) * 0.001
                plt.arrow(mid_x, mid_y, 0, dy, head_width=0.2, color='blue', length_includes_head=True, zorder=2)

    # 3. Desenhar os Pontos (Locais de Entrega)
    # Separamos X e Y de todos os pontos para ajustar os eixos depois
    all_x = []
    all_y = []

    for nome, (l, c) in coords.items():
        all_x.append(c)
        all_y.append(l)
        
        cor = 'red' if nome == 'R' else 'green'
        tamanho = 150 if nome == 'R' else 100
        
        # Plota o ponto
        plt.scatter(c, l, c=cor, s=tamanho, zorder=3, edgecolors='black')
        
        # Adiciona o rótulo (Nome) um pouco deslocado para não ficar em cima da linha
        plt.text(c + 0.15, l - 0.15, nome, fontsize=12, fontweight='bold', zorder=4)

    # Configurações Finais do Gráfico
    plt.title(f"Rota Otimizada (Manhattan): {' -> '.join(rota_nomes)}", fontsize=11)
    plt.xlabel("Coluna (X)")
    plt.ylabel("Linha (Y)")
    
    # Ajuste de Eixos para garantir que tudo apareça e fique quadrado (proporcional)
    if all_x and all_y:
        margem = 1
        plt.xlim(min(all_x) - margem, max(all_x) + margem)
        plt.ylim(min(all_y) - margem, max(all_y) + margem)

    plt.gca().invert_yaxis() # Inverte Y (matriz começa em cima)
    plt.grid(True, linestyle=':', alpha=0.3)
    
    print(f"-> Salvando mapa da rota em: {save_path}")
    plt.savefig(save_path, dpi=300)
    plt.close()