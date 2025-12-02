<p>
    <strong>Nome da Aplicação:</strong> Fly Food<br>
    <strong>Integrantes:</strong> <a href="https://github.com/Felipecs22">Felipe Cavalcante</a>, <a href="https://github.com/GustavoSantosgcs">Gustavo Santos</a> e <a href="https://github.com/pedroailton">Pedro Ailton</a><br>
    <strong>Professor:</strong> Cícero Garrozi<br>
    <strong>Disciplina:</strong> Projeto Interdisciplinar para Sistemas de Informação 2<br>
    <strong>Curso:</strong> Bacharelado em Sistemas de Informação<br>
    <strong>Unidade de Ensino:</strong> Universidade Federal Rural de Pernambuco (UFRPE)<br>
</p>

<p>O programa Flyfood é uma ferramenta de linha de comando que fornece ao usuário a rota mais rápida para as entregas dos drones da empresa FlyFood dada uma matriz como entrada em arquivo .txt que configura o mapa da região de entrega.</p>

<img src="1VA/assets/imagens/Logo FlyFood.png" width="250" height="250" alt="Demonstração do projeto">

<h2>Ferramentas Utilizadas</h2>
<table>
    <tr>
        <td><img src="1VA/assets/imagens/logo-python.png" alt="Logo do Python" width="25"> Python 3</td>
        <td>Linguagem de programação</td>
    </tr>
    <tr>
        <td><img src="1VA/assets/imagens/logo-vscode.png" alt="Logo do VSCode" width="25"> VSCode</td>
        <td>IDE de desenvolvimento do código-fonte</td>
    </tr>
    <tr>
        <td><img src="1VA/assets/imagens/logo-git.png" alt="Logo do Git" width="25"> Git</td>
        <td>Versionamento de código</td>
    </tr>
    <tr>
        <td><img src="1VA/assets/imagens/logo-github.png" alt="Logo do GitHub" width="25"> GitHub</td>
        <td>Repositório e cooperação no desenvolvimento</td>
    </tr>
</table>

<h1>VERSÃO 1VA</h1>

<h2>Formato da Entrada</h2>

O arquivo de entrada (`.txt`) deve seguir uma estrutura de matriz para representar o mapa de entregas.

O arquivo deve ter o seguinte formato:

```
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```
<ul>
    <li>Uma matriz A de dimensões M×N que representa a área de entrega;</li>
    <li>Cada elemento Aij​ (com i representando a linha e j a coluna) contém um identificador;</li>
    <li>O valor "0" indica uma posição vazia;</li>
    <li>Letras (como 'R', 'A', 'B', etc.) identificam pontos de interesse.</li>
</ul>

<h2>Bibliotecas Utilizadas</h2>
<table>
    <tr>
        <td>time</td>
        <td>Medição do tempo de execução do programa (cronômetro).</td>
    </tr>
    <tr>
        <td>itertools</td>
        <td>Geração de todas as permutações de rotas possíveis para a implementação do algoritmo de força bruta.</td>
    </tr>
    <tr>
        <td>csv</td>
        <td>Leitura e manipulação de arquivos no formato CSV.</td>
    </tr>
    <tr>
        <td>black</td>
        <td>Formatação do programa, para que se encaixe no padrão de formatação PEP 8 da linguagem.</td>
    </tr>
</table>

<h2>Instalações e Execução</h2>
<p>O projeto utiliza apenas bibliotecas padrão do Python, portanto, a única instalação necessária é a do <strong>Python 3</strong>. Nenhum pacote adicional precisa ser instalado via <code>pip</code>.</p>
<p>Para executar o programa, utilize o seguinte comando no terminal, dentro da pasta do projeto:</p>
<pre><code>python main.py</code></pre>
<p>Após a execução, o programa solicitará o caminho para o arquivo de entrada (ex: <code>entrada.txt</code>).</p>

<h1>VERSÃO 2VA</h1>

<h2>Formato da Entrada</h2>

O arquivo de entrada (`.txt`) deve seguir uma estrutura de matriz para representar o mapa de entregas.

O arquivo deve ter o seguinte formato:

```
3 2 5 7
3 4 4
3 5
2
```
<ul>
    <li>Uma matriz A em que cada elemento de coordenadas (i,j) possui a distância dos pontos i para j (que é a mesma de j para i)</li>
    <li>A matriz desconsidera o </li>
    <li>O valor "0" indica uma posição vazia;</li>
    <li>Letras (como 'R', 'A', 'B', etc.) identificam pontos de interesse.</li>
</ul>

<h2>Bibliotecas Utilizadas</h2>
<table> <tr> <td>time</td> <td>Medição do tempo de execução do algoritmo.</td> </tr> <tr> <td>csv</td> <td>Manipulação de arquivos de entrada e saída de dados.</td> </tr> <tr> <td><strong>Deap</strong></td> <td>Framework para Computação Evolutiva (Algoritmos Genéticos) utilizado para a seleção, cruzamento e mutação dos indivíduos.</td> </tr> <tr> <td><strong>NumPy</strong></td> <td>Computação científica de alta performance para cálculos matriciais e estatísticas da população.</td> </tr> <tr> <td><strong>Matplotlib</strong></td> <td>Geração dos gráficos de convergência (fitness x gerações) e plotagem visual das rotas no mapa 2D.</td> </tr> </table>
</table>

<h2>Instalações e Execução</h2>
<h2>Funcionalidades Avançadas (v2.0)</h2>

Além da otimização básica, a versão 2.0 introduz recursos avançados de Engenharia de Software e Ciência de Dados:

### 🧬 Algoritmo Genético com Elitismo
Diferente da força bruta da 1ª VA, utilizamos uma abordagem meta-heurística para encontrar soluções sub-ótimas em tempo hábil para grandes conjuntos de dados.
- **População:** Configurável (padrão: 100+ indivíduos).
- **Operadores:** Cruzamento Ordenado (Ordered Crossover) e Mutação por Inversão.
- **Elitismo:** Garante que a melhor solução de uma geração nunca seja perdida para a próxima.

### 🔄 Conversor de Grid para TSPLIB
O sistema possui um módulo inteligente (`converter.py`) capaz de ler arquivos de matriz simples (Grid) e convertê-los automaticamente para o formato de grafos ponderados (TSPLIB - Upper Row), permitindo o uso de algoritmos de otimização em mapas complexos.

### 📊 Visualização de Dados
O sistema gera automaticamente relatórios visuais na pasta `2VA/flyfood/graficos/`:
1. **Gráfico de Convergência:** Mostra a evolução da aptidão (fitness) média e mínima ao longo das gerações.
2. **Mapa da Rota:** Plota o caminho do drone em um plano 2D, utilizando a métrica Manhattan.

<div align="center">
  <img src="2VA/flyfood/graficos/grafico_convergencia.png" width="400" alt="Gráfico de Convergência">
  <img src="2VA/assets/imagens/Logo FlyFood.png" width="200" alt="Mapa Exemplo">
</div>

<h2>Dataset Brazil58</h2>

O projeto foi validado utilizando o dataset clássico **Brazil58** (58 cidades brasileiras), demonstrando a capacidade do algoritmo de lidar com problemas de escala real onde a força bruta seria computacionalmente impossível.

Para executar com o Brazil58:
1. Certifique-se de que o arquivo `.upper.txt` do Brazil58 esteja na pasta de entradas.
2. Execute o `main.py` e aponte o caminho.
3. O algoritmo genético processará as 58 cidades e gerará a rota otimizada.

<h2>Estrutura do Projeto</h2>

A organização dos arquivos segue o padrão MVC (Model-View-Controller) adaptado para scripts de automação:

```bash
flyfood-pisi-2/
├── 1VA/                  # Solução Força Bruta
│   └── flyfood/
│       ├── entradas/     # Arquivos .txt de teste
│       ├── main.py       # Ponto de entrada
│       ├── otimizador.py # Lógica de permutação
│       └── parser.py     # Leitura de arquivos
├── 2VA/                  # Solução Algoritmo Genético
│   └── flyfood/
│       ├── entrada_brazil58/ # Dataset Brazil58
│       ├── graficos/     # Saída das imagens geradas
│       ├── saida/        # Arquivos convertidos (.map e .upper)
│       ├── converter.py  # Conversor Grid -> Grafo
│       ├── main.py       # Controlador principal
│       ├── otimizador.py # Lógica GA com DEAP
│       └── visualizador.py # Geração de gráficos com Matplotlib
└── README.md
```
<p>
O projeto utiliza duas bibliotecas fora do padrão do Python: a <code>pandas</code> e a <code>matplotlib</code>, portanto, a instalação deles é necessária, além do <strong>Python 3</strong>. Para instalá-los, execute no terminal o seguinte comando:
<pre><code>pip install numpy deap matplotlib </code></pre>
</p>
<p>Para executar o programa, utilize o seguinte comando no terminal, dentro da pasta do projeto:</p>
<pre><code>python main.py</code></pre>
<p>Após a execução, o programa solicitará o caminho para o arquivo de entrada (ex: <code>entrada.txt</code>).</p>
