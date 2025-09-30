# Para medição de tempo e desempenho do programa para diferentes entradas
import time

from parser import parseArquivo
from otimizador import otimizarRota

def main(cronometro=False):
    print("::: Otimizador de Rotas FlyFood :::")
    caminho = input("Digite o caminho para o arquivo da matriz: ")

    try:
        if cronometro:
            tempo_inicial = time.perf_counter()

        pontos_mapeados = parseArquivo(caminho)
        print("Pontos encontrados:", pontos_mapeados)

        melhor_rota = otimizarRota(pontos_mapeados)

        if cronometro:
            tempo_final = time.perf_counter()
            print(f"Tempo de execução: {(tempo_final - tempo_inicial):.4f} segundos")

        print("\nCalculando rota...")
        print("\n-------------------------------------")
        print(f"A melhor rota encontrada é: {melhor_rota}")
        print("-------------------------------------")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
