# Para medição de tempo de execução do programa
import time

from .parser import parseArquivo
from .otimizador import otimizarRota, otimizarRotaPlus

def main(cronometro=False):  
    """
    Função principal do programa FlyFood.
    Controla o fluxo geral: leitura do arquivo de entrada,
    execução do algoritmo de otimização e exibição dos resultados.
    """
    print("\n::: Otimizador de Rotas FlyFood :::")
    caminho = input("Digite o caminho para o arquivo da matriz: ")

    modo = ""
    # Loop para evitar quebra se o usuário digitar errado
    while modo not in ["fast", "plus"]:
        modo = input("Escolha o modo (fast/plus): ").strip().lower()
        if modo not in ["fast", "plus"]:
            print("Opção inválida. Por favor, digite 'fast' ou 'plus'.")

    try:
        # --- ETAPA 1: Leitura e Exibição ---
        pontos_mapeados = parseArquivo(caminho)

        print("\nAnalisando o arquivo e mapeando os pontos...")
        print("\nInformações do arquivo:")
        print(f"  Número de linhas: {pontos_mapeados['num_linhas']}")
        print(f"  Número de colunas: {pontos_mapeados['num_colunas']}")

        print("\nMatriz:")
        for linha in pontos_mapeados["matriz"]:
            print("  " + " ".join(linha))

        print("\nPontos mapeados:")
        for ponto, coord in pontos_mapeados["pontos"].items():
            print(f"  - {ponto}: {coord}")
        print()

        print("Iniciando o cálculo da rota ótima...")

        # --- ETAPA 2: Execução do Algoritmo (Dentro do Cronômetro) ---
        duracao_algoritmo = 0
        if cronometro:
            # AQUI: Iniciamos o cronômetro APENAS para o bloco do algoritmo
            tempo_inicial_algoritmo = time.perf_counter()

        if modo == "plus":
            print("\nBuscando a melhor rota (modo completo)...")
            melhor_rota, melhor_custo, pior_rota, pior_custo = otimizarRotaPlus(
                pontos_mapeados["pontos"], mostrar_todas=True
            )
        else:
            print("\nBuscando a melhor rota (modo rápido)...")
            melhor_rota, melhor_custo = otimizarRota(
                pontos_mapeados["pontos"], mostrar_atualizacoes=True
            )
            pior_rota = None
            pior_custo = None

        if cronometro:
            # AQUI: Paramos o cronômetro LOGO APÓS o algoritmo terminar
            tempo_final_algoritmo = time.perf_counter()
            duracao_algoritmo = tempo_final_algoritmo - tempo_inicial_algoritmo

        # --- ETAPA 3: Exibição dos Resultados ---
        print("\nCálculo finalizado. Apresentando resultados...")

        print("\n-------------------------------------")
        print(f"Melhor rota encontrada: R -> {melhor_rota} -> R")
        print(f"Custo total: {melhor_custo} dronômetros")

        if pior_rota is not None:
            print()
            print(f"Pior rota encontrada:   R -> {pior_rota} -> R")
            print(f"Custo total: {pior_custo} dronômetros")

        if cronometro:
            print()
            # AQUI: Exibimos a duração correta, que agora mede apenas o algoritmo
            print(f"Tempo de execução do ALGORITMO: {duracao_algoritmo:.4f} segundos")
        print("-------------------------------------")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


# Executa o programa
if __name__ == "__main__":
    main(cronometro=True)