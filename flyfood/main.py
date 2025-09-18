from parser import parse_arquivo
from otimizador import otimizar_rota

def main():
    print("::: Otimizador de Rotas FlyFood :::")
    caminho = input("Digite o caminho para o arquivo da matriz: ")

    try:
        pontos_mapeados = parse_arquivo(caminho)
        print("Pontos encontrados:", pontos_mapeados)

        melhor_rota = otimizar_rota(pontos_mapeados)
        print("\n-------------------------------------")
        print(f"A melhor rota encontrada é: {melhor_rota}")
        print("-------------------------------------")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()