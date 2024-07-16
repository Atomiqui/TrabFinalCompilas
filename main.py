import func
import threading

while True:
    #file_path = input('Informe o nome do arquivo: ')
    G = func.read_grammar('GLD2.txt')
    if G:
        break

if func.validate_GLD(G):
    graph = func.build_graph(G)
    while True:
        word = input('Informe uma palavra para ser validada: ')
        if len(word) == 0:
            print('Palavra vazia!')
            continue
        if func.validate_word(graph, word, list(word), G['S'], '$'):
            print('Palavra pertence!')
        else:
            print('Palavra não pertence!')
        
        if input('Deseja testar outra palavra? (s/n) ') == 'n':
            break
else:
    print('Gramática inválida')