import func
import threading

while True:
    #file_path = input('Informe o nome do arquivo: ')
    G = func.read_grammar('GLD4.txt')
    if G:
        break

if func.validate_GLD(G):
    graph = func.build_graph(G)
    #func.show_graph(graph)
    while True:
        word = input('Informe uma palavra para ser validada: ')
        if func.validate_word(graph, word, G):
            print('Palavra válida')
        else:
            print('Palavra inválida')
            if input('Deseja continuar? (s/n) ') == 'n':
                break
else:
    print('Gramática inválida')