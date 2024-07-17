import func
import threading

while True:
    file_path = input('Informe o nome do arquivo: ')
    G = func.read_grammar(file_path)
    if G:
        break

if func.validate_GLD(G):
    graph = func.build_graph(G)
    while True:
        word = input('Informe uma palavra para ser validada: ')
        if len(word) == 0:
            print('Palavra vazia!')
            continue
        isValid, index_error = func.validate_word(graph, word, list(word), G['S'], '$')
        if isValid:
            print('\nPalavra pertence!')
        else:
            print('\nPalavra não pertence!')
            print(index_error)
            print(f'Erro: token inesperado \'{word[index_error]}\' na posição {index_error+1}.')
        if input('\nDeseja testar outra palavra? (s/n) ') == 'n':
            break
else:
    print('Gramática inválida')