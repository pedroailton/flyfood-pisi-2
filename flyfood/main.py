# Para medição de tempo de execução do programa
import time

from parser import parseArquivo
from otimizador import otimizarRota

def main(cronometro=False, melhores_rotas=False):  
    print("\n::: Otimizador de Rotas FlyFood :::")
    caminho = input("Digite o caminho para o arquivo da matriz: ")

    try:
        if cronometro:
            tempo_inicial = time.perf_counter() # inicia contador

        pontos_mapeados = parseArquivo(caminho)
        print("\nInformações do arquivo:")
        print(f"  Número de linhas: {pontos_mapeados['num_linhas']}")
        print(f"  Número de colunas: {pontos_mapeados['num_colunas']}")

        print("\nMatriz:")
        for linha in pontos_mapeados['matriz']:
            print("  " + " ".join(linha))

        print("\nPontos mapeados:")
        for ponto, coord in pontos_mapeados['pontos'].items():
            print(f"  - {ponto}: {coord}")
        print()

        melhor_rota, custo_total = otimizarRota(pontos_mapeados["pontos"], melhores_rotas)
        # pior_rota: parâmetro para a função retornar também a pior rota
        # melhores_rotas: parâmetro para função printar a melhor rota sempre que ela for atualizada

        if cronometro:
            tempo_final = time.perf_counter() # finaliza o contador
            print(f"\nTempo de execução: {(tempo_final - tempo_inicial):.4f} segundos")

        print("\nCalculando rota...")
        print("\n-------------------------------------")
        print(f"A melhor rota encontrada é: {melhor_rota}")
        print(f"Custo total: {custo_total} dronômetros")
        print("-------------------------------------")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main(cronometro=True, melhores_rotas=True)
