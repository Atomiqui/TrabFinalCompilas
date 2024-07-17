# Trabalho Final de Compiladores

#### Grupo: Alisson Costa Schmidt e Bianca Sabrina Bublitz.

## Estrutura do Projeto
  * **main.py**: É onde a comunicação com o usuário é feita e onde é mantido o loop principal do programa.
  * **func.py**: Contém funções auxiliares para leitura, análise e validação da gramática e das palavras.
  * **GLD.txt**: arquivo que está sendo usado para guardar a definição das gramáticas de teste (outro arquivo pode ser indicado).

## Definição formal da gramática:
```
G -> V = {(Non-terminal' ')+}\nT = {(Terminals' ')+}\nP = {\n(Productions\n)+}\nS = Non-terminal
Non-terminal -> A-Z | 1-9
Terminals -> a-z | * | / | - | + 
Productions -> Non-terminal '->' prod( | prod)*
Prod -> Terminals | Non-terminal | TerminalsNon-terminal | &
```
_OBS:_ ' ' indicando que é necessário o espaço após os terminais/não terminais pois é o que estamos usando para fazer o split.

## Como executar:
  1. Clonar o repositório:
      ```
      git clone https://github.com/Atomiqui/TrabFinalCompilas
      ```
      Para abrir com o VS Code:
      ```
      cd TrabFinalCompilas
      code .
      ```

      Ou abra a pasta do código com uma IDE da sua preferência!


  2. Verificar dependências necessárias:
      ```
      pip install matplotlib
      pip install networkx 
      ```
  3. Defina uma gramática a ser testada no arquivo ```GLD.txt``` ou crie outro arquivo com a definição.
    
      **Obs:** Deve estar no mesmo diretório.

  4. Rodar o programa:
      ```
      python main.py
      ```
  5. Caso sua gramática for uma GLD, será solicitada uma palavra a ser validada, ao ver a mensagem "Informe uma palavra para ser validada:", digite a palavra.

## Como foi feito:
O trabalho foi feito utilizando Python, visando a facilidade da linguagem para as operações necessárias. Também visando facilitar, após a leitura e validação da GR é montado um grafo com as produções, se assemelhando à um automato, assim, tendo um recurso visual (com a função ```show_grap(graph)```), que temos familiaridade, para poder ver o programa em execução e debug.

O laço principal do programa, situado no arquivo ```main.py```, é responsável pela comunicação com o usuário e a coordenação das ações resultantes dessa interação. Essas ações são executadas por meio das funções auxiliares definidas em ```func.py```.

A leitura da gramática é feita utilizando a função ```read_grammar(file_path)```, que procura pelos quatro elementos de representação de uma GR, que aqui chamamos de V, T, P e S e faz a leitura das linhas separado parte esquerda e direita enquanto remove espaços, chaves, ... A validação da GR é feita usando a função ```validate_GLD(G)``` que utiliza das regras que definem uma GLD para fazer os testes sobre os elementos (V, T, P e S) lidos. Por exemplo, faz a validação se as produções possuem variáveis apenas na parte direita da derivação.

Com a GLD lida e validada, utilizamos a função ````build_graph(G)```` para montar o grafo que representará a gramática na nossa função de validação. Um nó com o símbolo de final de _string_ ($) é adicionado para que as produções que derivam diretamente em terminais, possam ser colocadas no grafo. Segue um exemplo:
```
S -> aA
A -> b | &
```
Gera um grafo assim:

![Grafo_Exemplo](https://github.com/Atomiqui/TrabFinalCompilas/blob/main/src/img_grafo.png)

Com o grafo montado, a função de validação ```validate_word(graph, word, stack, current_node, F)``` utiliza as arestas e os seus rótulos para fazer o deslocamento. Durante a execução da validação, caso a o token que está sendo testado no momento não ache uma aresta em que ele esteja em um dos rótulos, isso indica que há um erro na palavra, ou o caminho escolhido (em caso de ambiguidade) não é o certo, mas, caso ao final da palavra o nó atual seja o $ isso indica que a palavra foi validada.

Em casos de erro, o índice retornado é usado para indicar a posição da palavra que gerou o erro. Como a solução escolhida foi por meio de recursão, existem um vetor que armazena os erros que aconteceram em cada ramificação e ao retornar, indica apenas o que foi mais longe (maior índice alcançado na palavra informada). Após o fim da função de validação, é exibida uma mensagem para o usuário, em caso da palavra pertencer "Palavra pertence!" caso não pertença "Palavra não pertence!" e indica a ocorrência de um erro e a sua posição.
