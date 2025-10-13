# Para medição de tempo de execução do programa
import time

from parser import parseArquivo
from otimizador import otimizarRota, otimizarRotaPlus

def main(cronometro=False):  
    """
    Função principal do programa FlyFood.
    Controla o fluxo geral: leitura do arquivo de entrada,
    execução do algoritmo de otimização e exibição dos resultados.
    """
    
    print("\n::: Otimizador de Rotas FlyFood :::")
    caminho = input("Digite o caminho para o arquivo da matriz: ")
    modo = input("Escolha o modo (fast/plus): ").strip().lower()
    
    try:
        # Se cronômetro ativado, inicia a contagem de tempo
        if cronometro:
            tempo_inicial = time.perf_counter() # inicia contador

        # Lê e interpreta o arquivo com o mapa e os pontos
        pontos_mapeados = parseArquivo(caminho)
        print("\nInformações do arquivo:")
        print(f"  Número de linhas: {pontos_mapeados['num_linhas']}")
        print(f"  Número de colunas: {pontos_mapeados['num_colunas']}")

        # Exibe a matriz carregada
        print("\nMatriz:")
        for linha in pontos_mapeados['matriz']:
            print("  " + " ".join(linha))

        # Exibe os pontos encontrados (origem e entregas)
        print("\nPontos mapeados:")
        for ponto, coord in pontos_mapeados['pontos'].items():
            print(f"  - {ponto}: {coord}")
        print()

        # Seleciona o modo
        if modo == "plus":
            # Modo detalhado: imprime todas as rotas (ordenadas por custo)
            melhor_rota, melhor_custo, pior_rota, pior_custo = otimizarRotaPlus(
                pontos_mapeados["pontos"], mostrar_todas=True)
        else:
            # Modo rápido: só atualizações da melhor rota 
            melhor_rota, melhor_custo = otimizarRota(
                                        pontos_mapeados["pontos"], mostrar_atualizacoes=False)        

            pior_rota = None
            pior_custo = None
            
        if cronometro:
            tempo_final = time.perf_counter()
            duracao = tempo_final - tempo_inicial
        else:
            duracao = 0

        # Exibe os resultados finais
        print("\n-------------------------------------")
        print(f"Melhor rota encontrada: R -> {melhor_rota} -> R")
        print(f"Custo total: {melhor_custo} dronômetros")
        
        if pior_rota is not None:
            print(f"\nPior rota encontrada:   R -> {pior_rota} -> R")
            print(f"Custo total: {pior_custo} dronômetros")

        if cronometro:
            print(f"\nTempo total de execução: {duracao:.4f} segundos")
        print("-------------------------------------")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


# Executa o programa com cronômetro e exibição de todas as rotas
if __name__ == "__main__":
    main(cronometro=True)
