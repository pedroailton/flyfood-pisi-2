# Para medição de tempo de execução do programa e manipulação de arquivos
import time
import os

# Importa os parsers de dados e o conversor
from parser import parseArquivoMatriz, parseArquivoTsplib
from converter import converterGridParaUpperRow

# Importa APENAS a nova função de otimização por Algoritmo Genético
from otimizador import otimizarRotaGa

def lerArquivoMapa(caminhoMapa):
    """
    Lê o arquivo .map.txt gerado pelo conversor e retorna um dicionário 
    de mapeamento de índice (int) para nome (str).
    
    Exemplo de entrada no arquivo: "1 A", "2 B"
    Exemplo de saída: {0: 'R', 1: 'A', 2: 'B', ...}
    (Ajustamos -1 pois o parser do AG considera R=0, mas o arquivo começa em 1)
    """
    if not os.path.exists(caminhoMapa):
        print(f"[Aviso] Arquivo de mapeamento não encontrado: {caminhoMapa}")
        return None
        
    mapaNomes = {}
    try:
        with open(caminhoMapa, "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split()
                if len(partes) == 2:
                    # O arquivo salva 1-R, 2-A... mas Python usa 0-R, 1-A...
                    indice = int(partes[0]) - 1 
                    nome = partes[1]
                    mapaNomes[indice] = nome
    except Exception as e:
        print(f"[Erro] Falha ao ler arquivo de mapa: {e}")
        return None

    return mapaNomes


def main(cronometro=False):  
    """
    Função principal do programa FlyFood (Versão 2.0 - Algoritmo Genético).
    Controla o fluxo: Conversão (opcional) -> Leitura TSPLIB -> Execução AG -> Resultados.
    """
    print("\n::: Otimizador de Rotas FlyFood (v2.0 - Genetic Algorithm) :::")
    caminho = input("Digite o caminho para o arquivo: ")

    # --- ETAPA 1: MODO CONVERSOR (Opcional) ---
    # Permite transformar um grid original (matriz completa) em formato otimizado
    try:
        modoConv = input("Deseja converter este arquivo [formato grid] para TSPLIB (s/n)? ").strip().lower()
        
        if modoConv == "s":
            print("\n--- Iniciando Conversão ---")
            dados = parseArquivoMatriz(caminho)
            dados["origem"] = caminho  # Passa o nome original para gerar os nomes de saída
            converterGridParaUpperRow(dados)
            print("Conversão concluída. Você pode rodar o programa novamente usando o arquivo .upper.txt gerado.\n")
            return # Encerra o programa após a conversão
            
    except FileNotFoundError:
        print(f"\n[Erro Crítico] O arquivo '{caminho}' não foi encontrado.")
        return
    except Exception as e:
        print(f"\n[Erro Inesperado] Falha na conversão: {e}")
        return
    
    # --- ETAPA 2: MODO OTIMIZADOR (Padrão) ---
    print("\n--- Iniciando Otimização ---")

    #try:
        # 1. Carrega a matriz de distâncias (arquivo .upper.txt)
        # parseArquivoTsplib retorna o dicionário de distâncias e a quantidade de pontos
    distancias, qtdPontos = parseArquivoTsplib(caminho)
        
        # 2. Carrega o arquivo de mapeamento de nomes (.map.txt)
        # Tenta adivinhar o nome do arquivo de mapa trocando a extensão
    caminhoMapa = caminho.lower().replace(".upper.txt", ".map.txt")
    if ".upper.txt" not in caminho.lower():
             # Fallback caso o arquivo não tenha a extensão padrão
             caminhoMapa = os.path.splitext(caminho)[0] + ".map.txt"
             
    mapaNomes = lerArquivoMapa(caminhoMapa)
        
    if mapaNomes is None:
            print("Não foi possível carregar os nomes dos pontos. O programa será encerrado.")
            return

    print(f"Matriz carregada com sucesso. Otimizando rota para {qtdPontos} pontos de entrega (+ Ponto R)...")

        # --- ETAPA 3: Execução do Algoritmo Genético ---
    duracaoAlgoritmo = 0
        
    if cronometro:
            tempoInicial = time.perf_counter()

        # Chamada única ao otimizador (Força Bruta foi removida)
    melhorIndices, melhorCusto = otimizarRotaGa(
            distancias, 
            qtdPontos,
            tamPopulacao=100,   # Pode ajustar aqui
            numGeracoes=500,    # Pode ajustar aqui
            taxaCrossover=0.8,
            taxaMutacao=0.2
        )

    if cronometro:
            tempoFinal = time.perf_counter()
            duracaoAlgoritmo = tempoFinal - tempoInicial

        # --- ETAPA 4: Tradução e Exibição dos Resultados ---
    print("\nCálculo finalizado. Apresentando resultados...")

        # CORREÇÃO AQUI: Somamos +1 no índice 'i' para pegar o nome correto no mapa
        # O mapa tem: 0=R, 1=A, 2=B...
        # O AG retorna: 0, 1... (que significam 1º ponto de entrega, 2º ponto...)
        # Então AG(0) -> Mapa(1)='A'
    nomesRota = [mapaNomes.get(i + 1, f"?{i}?") for i in melhorIndices]
        
    rotaFormatada = " -> ".join(nomesRota)

    print("\n-------------------------------------")
    print(f"Melhor rota encontrada: R -> {rotaFormatada} -> R")
    print(f"Custo total: {melhorCusto} dronômetros")
        
    if cronometro:
        print(f"\nTempo de execução do algoritmo: {duracaoAlgoritmo:.4f} segundos")
    print("-------------------------------------")

''' except FileNotFoundError:
        print(f"\n[Erro] O arquivo '{caminho}' não foi encontrado.")
        print("Dica: Verifique se você digitou o caminho correto para o arquivo .upper.txt")
    except Exception as e:
        print(f"\n[Erro Crítico] Ocorreu um erro durante a otimização: {e}")'''
        # É útil imprimir o erro completo para debug, se necessário:
        # import traceback
        # traceback.print_exc()


# Ponto de entrada para execução como módulo (python -m ...)
if __name__ == "__main__":
    main(cronometro=True)