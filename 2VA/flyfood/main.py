import time
import os

import traceback # Biblioteca para verificação de erros (deve ser apagada na versão final)

from parser import parseArquivoMatriz, parseArquivoTsplib, lerArquivoMapa
from converter import converterGridParaUpperRow
from otimizador import otimizarRotaGa
from visualizador import plotar_dados_logbook, plotar_mapa_flyfood

def limpar_graficos_antigos(pasta_graficos):
    """
    Remove arquivos de imagem antigos para evitar confusão com rodadas anteriores do programa.
    """
    arquivos_para_apagar = ["grafico_convergencia.png", "grafico_mapa.png"]
    
    if os.path.exists(pasta_graficos):
        for arquivo in arquivos_para_apagar:
            caminho_completo = os.path.join(pasta_graficos, arquivo)
            try:
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
            except Exception as e:
                print(f"[Aviso] Não foi possível limpar {arquivo}: {e}")

def main(cronometro = False, auto_continuar = False):
    """
    Função principal do programa FlyFood (Versão 2.0 - Algoritmo Genético).

    Parâmetros:
        cronometro: se True, mede o tempo de execução do AG.
        auto_continuar:
            - False -> converte e encerra.
            - True  -> após converter, pergunta se deve continuar.
    """

    print("\n::: Otimizador de Rotas FlyFood v2.0 :::")

    # --- ETAPA 0: PREPARAÇÃO DE AMBIENTE  ---
    dir_base = os.path.dirname(os.path.abspath(__file__))
    caminho_pasta_graficos = os.path.join(dir_base, "graficos")
    os.makedirs(caminho_pasta_graficos, exist_ok=True)
    
    # Apaga gráficos da rodada anterior AGORA
    limpar_graficos_antigos(caminho_pasta_graficos)

    caminho = input("Digite o caminho para o arquivo: ").strip()
    caminho_mapa_forcado = None

    # --- ETAPA 1: MODO CONVERSOR  ---
    try:
        modo_conv = input(
            "Deseja converter este arquivo [formato grid] para TSPLIB (s/n)? "
        ).strip().lower()
        
        if modo_conv == "s":
            print("\n--- Iniciando Conversão ---")
            dados = parseArquivoMatriz(caminho)
            dados["origem"] = caminho  # nome original do arquivo de grid

            # Conversão gera .upper.txt e .map.txt
            caminho_upper, caminho_map = converterGridParaUpperRow(dados)
            caminho_mapa_forcado = caminho_map 

            if not auto_continuar:
                # para aqui e avisa o usuário dos arquivos gerados
                print("Conversão concluída.")
                print("Execute novamente o programa usando o arquivo:")
                print(f"  {caminho_upper}\n")
                return
            
            else:
                # Modo interativo: pergunta o que o usuário quer fazer após conversão
                print("Conversão concluída.")
                print(f"Arquivo convertido gerado em: {caminho_upper}")
                opcao = input(
                    "Pressione ENTER para continuar usando o arquivo convertido\n"
                    "ou digite 'sair' para encerrar o programa: "
                ).strip().lower()

                if opcao == "sair":
                    print("Encerrando programa. Você pode executá-lo novamente quando quiser.")
                    return
                else:
                    print("Prosseguindo com a otimização usando o arquivo convertido...\n")
                    caminho = caminho_upper

    except FileNotFoundError:
        print(f"\n[Erro Crítico] O arquivo '{caminho}' não foi encontrado.")
        return
    except Exception as e:
        print(f"\n[Erro Inesperado] Falha na conversão: {e}")
        return
    
    # --- ETAPA 2: OTIMIZADOR ---
    print("\n--- Iniciando Otimização ---")

    try:
        # 1. Carrega a matriz de distâncias (arquivo .upper.txt)
        distancias, qtd_pontos = parseArquivoTsplib(caminho)
        
        # 2. Define o caminho do arquivo de mapeamento de nomes (.map.txt)
        if caminho_mapa_forcado is not None:
            # Veio da conversão nesta mesma execução
            caminho_mapa = caminho_mapa_forcado
        else:
            # Tenta adivinhar a partir do nome do arquivo de entrada
            caminho_mapa = caminho.lower().replace(".upper.txt", ".map.txt")
            if ".upper.txt" not in caminho.lower():
                # Fallback: troca só a extensão
                caminho_mapa = os.path.splitext(caminho)[0] + ".map.txt"
        
        mapa_nomes, coords_mapa = lerArquivoMapa(caminho_mapa)
        if mapa_nomes is None:
            print("[Aviso] Arquivo .map.txt não encontrado. Gerando nomes padrão e desativando gráfico 2D.")
            # Cria um dicionário simples: {0: "1", 1: "2", ...}
            # O AG usa índice 0..N, vamos chamar de "Ponto 1..N"
            mapa_nomes = {i: str(i + 1) for i in range(qtd_pontos)}
            coords_mapa = None # Garante que não tentaremos plotar mapa
        else:
            print("Arquivo de mapa carregado com sucesso.")

        print(f"Matriz carregada com sucesso. Otimizando rota para {qtd_pontos} pontos de entrega (+ Ponto R)...")

        # --- ETAPA 3: Execução do Algoritmo Genético ---
        duracao_algoritmo = 0
        
        if cronometro:
            tempo_inicial = time.perf_counter()

        melhor_indices, melhor_custo, logbook = otimizarRotaGa(
            distancias,
            qtd_pontos,
            tam_populacao=100,     # Ajustável
            num_geracoes=500,      # Condição de parada (ajustável)
            taxa_crossover=0.8,    # Ajustável
            taxa_mutacao=0.2       # Ajustável
        )

        if cronometro:
            tempo_final = time.perf_counter()
            duracao_algoritmo = tempo_final - tempo_inicial

        # --- ETAPA 4: Tradução e Exibição dos Resultados ---
        print("\nCálculo finalizado. Apresentando resultados...")

        nomes_rota = [mapa_nomes.get(i + 1, f"?{i}?") for i in melhor_indices]
        rota_formatada = " -> ".join(nomes_rota)

        print("\n-------------------------------------")
        print(f"Melhor rota encontrada: R -> {rota_formatada} -> R")
        print(f"Custo total: {melhor_custo} dronômetros")
        if cronometro:
            print(f"\nTempo de execução do algoritmo: {duracao_algoritmo:.4f} segundos")
        print("-------------------------------------")

        # 1. Convergência (Sempre gera se tiver logbook)
        print("\n--- Gerando Gráficos ---")

        # Pega o diretório onde este arquivo main.py está salvo
        dir_base = os.path.dirname(os.path.abspath(__file__))
        
        caminho_pasta_graficos = os.path.join(dir_base, "graficos")
        
        # Cria a pasta se ela não existir
        os.makedirs(caminho_pasta_graficos, exist_ok=True)
        print(f"Os arquivos serão salvos em: {caminho_pasta_graficos}")
        nome_arquivo_conv = os.path.join(caminho_pasta_graficos, "grafico_convergencia.png")
        plotar_dados_logbook(logbook, nome_arquivo_conv)
        
        # 2. Mapa 2D (Só gera se o .map.txt forneceu coordenadas)
        if coords_mapa:
            print("Coordenadas encontradas no .map.txt. Gerando mapa 2D...")

            nome_arquivo_mapa = os.path.join(caminho_pasta_graficos, "grafico_mapa.png")

            plotar_mapa_flyfood(coords_mapa, melhor_indices, mapa_nomes, nome_arquivo_mapa)
        else:
            print("[Aviso] O arquivo .map.txt existe mas não contém coordenadas (formato antigo?).")
            print("        O gráfico de mapa 2D não será gerado.")

    except FileNotFoundError:
        print(f"\n[Erro] O arquivo '{caminho}' não foi encontrado.")
        print("Dica: verifique se você digitou o caminho correto para o arquivo .upper.txt")
    except Exception as e:
        print("\n--- DETALHES DO ERRO ---")
        traceback.print_exc()
        print(f"\n[Erro Crítico] Ocorreu um erro durante a otimização: {e}")


if __name__ == "__main__":
    # Aqui é possível escolher o comportamento do cronometro e/ou do fluxo automatico pós conversão
    main(cronometro=True, auto_continuar=True)
