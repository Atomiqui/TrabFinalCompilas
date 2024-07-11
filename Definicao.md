# Trabalho de Compiladores
_Um Interpretador para Gramáticas Regulares_

### Especificação do trabalho:
#### Tarefas impotantes para iniciar o trabalho:
* Entender o que deve ser feito. **V**
* Entender o que são Gramáticas Lineares à Direita e como identificar.
    * Isso pode ser uma GLD:
      ```
      S -> B
      B -> a
      ```
* Escolher a linguagem de programação (levar em consideração os geradores de parser). **Python ♥**
* Qual analisador sintático vamos fazer?
* Lembrar de construir o **README** conforme avançamos.

#### Especificações do [PDF](https://classroom.google.com/u/0/c/NjU1ODgzOTMyMDMw/a/Njg0Njk4NTU3MDY5/details):
* Criar uma gramática para representar Gramáticas Regulares (GR).
* Implementar um interpretador para essas gramáticas.
* O interpretador deve reconhecer (ou não) palavras de acordo com a especificação da gramática.
* Tratar erros da especificação da GR, se existirem.
* A gramática deve permitir representar os 4 elementos da representação formal de uma GR.
* A gramática deve estar armazenada em um arquivo para sua leitura.
* A GR deve ser do tipo Gramática Linear à Direita (GLD).
* O parser deve validar se a gramática recebida é uma GLD.
* Validar a Gramática Regular fornecida pelo usuário.
* Solicitar (em tempo de execução) ao usuário uma palavra para ser validada.
* Emitir uma mensagem de validação se a palavra pertence à linguagem da GR, exibindo os movimentos entre símbolos não-terminais conforme o programa percorre as produções da gramática e reconhece os símbolos terminais.
* Emitir uma mensagem de erro, mostrando a posição da palavra a ser testada em que houve o problema, se a palavra não pertence à linguagem da GR.
* Trabalhos podem ser feitos individualmente ou em dupla, com correta identificação dos responsáveis.
* Pode ser implementado em qualquer linguagem, com o auxílio de gerador de parsers (ou não).
* O trabalho, após entregue, será apresentado pessoalmente ao professor, em horário de aula a ser combinado.
* Entrega via Classroom:
  * Todo o código desenvolvido;
  * Documentação;
  * Um arquivo readme.txt contendo todas as instruções para a compilação e execução do código, indicando dependências, plataforma escolhida e passos detalhados.
* Valerá o último envio recebido.
