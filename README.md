# Trabalho Final de Compiladores

#### Grupo: Alisson Costa Schmidt e Bianca Sabrina Bublitz.

### Interpretador de Gramáticas Regulares Lineares à Direita
O projeto desenvolvido representa um interpretador para Gramáticas Regulares Lineares à Direita. O interpretador é capaz de ler uma gramática a partir de um arquivo, validar palavras fornecidas pelo usuário de acordo com a gramática, e informar se a palavra é válida ou não.

## Estrutura do Projeto
  * GLD.txt: arquivo contendo a definição da gramática regular.
  * func.py: contém funções auxiliares para análise e validação da gramática.
  * main.py: script principal que executa o interpretador.

## Defiição formal da gramática:
```
G -> V = {(Non-terminal' ')+}\nT = {(Terminals' ')+}\nP = {\n(Productions\n)+}\nS = Non-terminal
Non-terminal -> A-Z | 1-9
Terminals -> a-z | * | / | - | + 
Productions -> Non-terminal '->' prod( | prod)*
Prod -> Terminals | Non-terminal | TerminalsNon-terminal | &
```
_OBS:_ ' ' indicando que é necessário o espaço após os terminais/não terminais pois é o que estamos usando para fazer o split.

## Como executar:
  1. Clone o repositório:
  ```
  git clone <url-do-repositorio>
  cd <nome-do-repositorio>
  ```

  2. Execute o script principal:
  ```
  python main.py
  ```

  3. Digite a palavra a ser validada quando solicitado:
  ```
  Enter a word to validate: '101'
  ```

## Erros Comuns:
  * Símbolos Inválidos: Certifique-se de que a palavra contenha apenas símbolos terminais definidos na gramática.
  * Formatação da Gramática: Verifique se a gramática está corretamente formatada no arquivo GLD2.txt.