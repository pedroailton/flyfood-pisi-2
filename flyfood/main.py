# Para medição de tempo de execução do programa
import time

from parser import parseArquivo
from otimizador import otimizarRota

def main(cronometro=False):
    """
    Executa o Otimizador de Rotas FlyFood.

    Lê um arquivo de entrada (TXT ou CSV) com dimensões e matriz do mapa,
    exibe as informações formatadas e calcula a melhor rota para visitar
    todos os pontos e retornar ao ponto 'R'.

    Args:
        cronometro (bool, opcional): Se True, mede e mostra o tempo de execução.
    """
    
    print("::: Otimizador de Rotas FlyFood :::")
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

        melhor_rota = otimizarRota(pontos_mapeados["pontos"])

        if cronometro:
            tempo_final = time.perf_counter() # finaliza o contador
            print(f"\nTempo de execução: {(tempo_final - tempo_inicial):.4f} segundos")

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
