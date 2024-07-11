# Trabalho Final de Compiladores

### Grupo:
**Alisson Costa Schmidt** e **Bianca Sabrina Bu(alguma coisa).**

## Como definir a gramática:
Exemplos de definição onde:
* **V**: Conjunto finito de **V**ariáveis (não-terminais).
* **T**: Conjunto finito de símbolos **T**erminais.
* **P**: Conjunto finito de regras de **P**rodução.
* **S**: **S**ímbolo inicial.
* **&**: Símbolo de vazio.

```
V = {S, A, B}
T = {a, b, c}
P = {
  S -> aA,
  A -> bB | cA | &,
  B -> a
}
S = S
```
_OBS:_ Atente-se às chaves ({}), elas devem estar na mesma configuração dos exemplos!
## Como rodar o trabalho:
## Como foi feito: