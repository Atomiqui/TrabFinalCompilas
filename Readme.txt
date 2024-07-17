TRABALHO FINAL DE COMPILADORES
Grupo: Alisson Costa Schmidt e Bianca Sabrina Bublitz

INTERPRETADOR DE GRAMÁTICAS REGULARES LINEARES À DIREITA
O projeto desenvolvido representa um interpretador para Gramáticas Regulares Lineares à Direita. O interpretador é capaz de ler uma gramática a partir de um arquivo, validar palavras fornecidas pelo usuário de acordo com a gramática, e informar se a palavra é válida ou não.


ESTRUTURA DO PROJETO
  - GLD.txt: arquivo contendo a definição da gramática regular.
  - func.py: contém funções auxiliares para análise e validação da gramática.
  - main.py: script principal que executa o interpretador.


DEFINIÇÃO FORMAL DA GRAMÁTICA:
G -> V = {(Non-terminal' ')+}\nT = {(Terminals' ')+}\nP = {\n(Productions\n)+}\nS = Non-terminal
Non-terminal -> A-Z | 1-9
Terminals -> a-z | * | / | - | + 
Productions -> Non-terminal '->' prod( | prod)*
Prod -> Terminals | Non-terminal | TerminalsNon-terminal | &

*OBS: ' ' indicando que é necessário o espaço após os terminais/não terminais pois é o que estamos usando para fazer o split.


COMO EXECUTAR:
  1. Pré-requisitos
  Certifique-se de ter o Python instalado em sua máquina.

  2. Instalação das Dependências
  Instale as dependências necessárias:
  Abra o terminal (ou prompt de comando) e execute os seguintes comandos:
    pip install networkx matplotlib

  3. Clone o repositório:
    git clone <url-do-repositorio>
    cd <nome-do-repositorio>

  4. Execute o script principal:
    python main.py

  5. Digite a palavra a ser validada quando solicitado:
  Enter a word to validate: 101


ERROS COMUNS:
  * Formatação da Gramática: verifique se a gramática está corretamente formatada no arquivo GLD.txt.
  * Símbolos Inválidos: certifique-se de que a palavra contenha apenas símbolos terminais definidos na gramática.
