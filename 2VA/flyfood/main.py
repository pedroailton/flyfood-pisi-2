import time
import os

from parser import parseArquivoMatriz, parseArquivoTsplib
from converter import converterGridParaUpperRow
from otimizador import otimizarRotaGa


def lerArquivoMapa(caminho_mapa):
    """
    Lê o arquivo .map.txt gerado pelo conversor e retorna um dicionário 
    de mapeamento de índice (int) para nome (str).
    """
    if not os.path.exists(caminho_mapa):
        print(f"[Aviso] Arquivo de mapeamento não encontrado: {caminho_mapa}")
        return None
        
    mapa_nomes = {}
    try:
        with open(caminho_mapa, "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split()
                if len(partes) == 2:
                    indice = int(partes[0]) - 1  # arquivo começa em 1, AG usa 0
                    nome = partes[1]
                    mapa_nomes[indice] = nome
    except Exception as e:
        print(f"[Erro] Falha ao ler arquivo de mapa: {e}")
        return None

    return mapa_nomes


def main(cronometro = False, auto_continuar = False):
    """
    Função principal do programa FlyFood (Versão 2.0 - Algoritmo Genético).

    Parâmetros:
        cronometro: se True, mede o tempo de execução do AG.
        auto_continuar:
            - False -> converte e encerra.
            - True  -> após converter, pergunta se deve continuar.
    """
    print("\n::: Otimizador de Rotas FlyFood (v2.0 - Genetic Algorithm) :::")
    caminho = input("Digite o caminho para o arquivo: ").strip()

    # Quando usamos o auto_continuar, guardamos aqui o caminho do mapa convertido
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
    
    # --- ETAPA 2: MODO OTIMIZADOR ---
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
        
        mapa_nomes = lerArquivoMapa(caminho_mapa)
        if mapa_nomes is None:
            print("Não foi possível carregar os nomes dos pontos. O programa será encerrado.")
            return

        print(f"Matriz carregada com sucesso. Otimizando rota para {qtd_pontos} pontos de entrega (+ Ponto R)...")

        # --- ETAPA 3: Execução do Algoritmo Genético ---
        duracao_algoritmo = 0
        
        if cronometro:
            tempo_inicial = time.perf_counter()

        melhor_indices, melhor_custo = otimizarRotaGa(
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

    except FileNotFoundError:
        print(f"\n[Erro] O arquivo '{caminho}' não foi encontrado.")
        print("Dica: verifique se você digitou o caminho correto para o arquivo .upper.txt")
    except Exception as e:
        print(f"\n[Erro Crítico] Ocorreu um erro durante a otimização: {e}")


if __name__ == "__main__":
    # Aqui é possível escolher o comportamento do cronometro e/ou do fluxo automatico pós conversão
    main(cronometro=True, auto_continuar=True)
