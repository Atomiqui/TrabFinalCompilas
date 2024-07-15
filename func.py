import networkx as nx
import threading
import matplotlib.pyplot as plt

def read_file(file_path):
    file_path = 'GLDs/' + file_path
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print('Arquivo não encontrado. Tente novamente.')
        return None
    except Exception as e:
        print(f'Erro: {e}')
        return None

def read_grammar(file_path):
    p = []
    reading_P = False

    lines = read_file(file_path)
    if not lines:
        return None
    
    for line in lines:
        line = line.strip()

        if line.startswith('#') or not line:
            continue

        if line.startswith('V'):
            v = line.split('=')[1].strip()[1:-1].split(', ')
        elif line.startswith('T'):
            t = line.split('=')[1].strip()[1:-1].split(', ')
        elif line.startswith('P'):
            reading_P = True
            continue
        elif reading_P:
            if line == '}':
                reading_P = False
                continue
            if '->' in line and '|' not in line:
                parte_esquerda, parte_direita = line.split('->')
                parte_direita = parte_direita.strip().rstrip(',')
                p.append((parte_esquerda.strip(), parte_direita))
            elif '->' in line and '|' in line:
                parte_esquerda, parte_direita = line.split('->')
                parte_direita = parte_direita.strip().split('|')
                for producao in parte_direita:
                    if ',' in producao:
                        producao = producao.split(',')
                        producao = ''.join(producao)
                    p.append((parte_esquerda.strip(), producao.strip()))
            else:
                raise ValueError(f"Formato de produção inválido: {line}")
        elif line.startswith('S'):
            s = line.split('=')[1].strip()

    return {'V': v, 'T': t, 'P': p, 'S': s}

def validate_GLD(G):
    V = G['V']
    T = G['T']
    P = G['P']
    S = G['S']

    print(f"V: {V}")
    print(f"T: {T}")
    print(f"P: {P}")
    print(f"S: {S}\n")

    if S not in V:
        print(f"Símbolo inicial {S} não está no conjunto de variáveis.")
        return False
    
    vInP = []
    tInP = []
    for v, t in P:
        if v not in V:
            print(f"Variável {v}, da produção {v} -> {t}, não está no conjunto de não terminais.")
            return False
        elif len(t) == 1 and t not in V and t not in T:
            if t == '&':
                continue
            print(f"Terminal {t}, da produção {v} -> {t}, não está no conjunto de terminais.")
            return False
        elif len(t) == 2 and (t[0] not in T):
            print(f"Terminal {t}, da produção {v} -> {t}, não está no conjunto de terminais.")
            return False
        elif len(t) == 2 and (t[1] not in V):
            print(f"Variável {t}, da produção {v} -> {t}, não está no conjunto de não terminais.")
            return False
        elif len(t) > 2:
            print(f"Produção {v} -> {t} é inválida.")
            return False

        if v not in vInP:
            vInP.append(v)

        if len(t) == 1 and t not in V:
            if t not in tInP:
                tInP.append(t)
        elif len(t) == 2:
            if t[0] not in tInP:
                tInP.append(t[0])

    if len(vInP) != len(V):
        print(f"As produções não utilizam todas as variáveis.")
        return False

    if len(tInP) != len(T):
        print(f"As produções não utilizam todos os terminais.")
        return False

    return True

def build_graph(G):
    V = G['V']
    T = G['T']
    P = G['P']
    S = G['S']

    graph = nx.DiGraph()
        
    for v, t in P:
        if len(t) == 1 and t not in V:
            if graph.has_edge(v, '$'):
                label = graph[v]['$']['label']
                label = [label, t]
                graph.add_edge(v, '$', label=', '.join(label))
            else:
                graph.add_edge(v, '$', label=t)
        elif len(t) == 1 and t in V:
            graph.add_edge(v, t, label='')
        elif len(t) == 2:
            if graph.has_edge(v, t[1]):
                label = graph[v][t[1]]['label']
                label = [label, t[0]]
                graph.add_edge(v, t[1], label=', '.join(label))
            else:
                graph.add_edge(v, t[1], label=t[0])
    return graph

def build_reverse_graph(G):
    V = G['V']
    T = G['T']
    P = G['P']
    S = G['S']

    graph = nx.DiGraph()
        
    for v, t in P:
        if len(t) == 1 and t not in V:
            if graph.has_edge('$', v):
                label = graph['$'][v]['label']
                label = [label, t]
                graph.add_edge('$', v, label=', '.join(label))
            else:
                graph.add_edge('$', v, label=t)
        elif len(t) == 1 and t in V:
            graph.add_edge(t, v, label='')
        elif len(t) == 2:
            if graph.has_edge(t[1], v):
                label = graph[t[1]][v]['label']
                label = [label, t[0]]
                graph.add_edge(t[1], v, label=', '.join(label))
            else:
                graph.add_edge(t[1], v, label=t[0])
    return graph

def show_graph(graph):
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', font_color='black')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_size=10)
    plt.show()

def validate_word(graph, word, G):
    current_node = G['S']
    T = G['T']
    T.append('&')
    isLoop = False
    isAmbiguous = False
    visitedNodes = []
    stack = list(word)
    previous_variable = []
    previous_stack = []

    i = 0

    print(f"Validando {word}:")
    print('\033[31m' + stack[0] + '\033[0m' + ''.join(stack[1:])) if stack else ...
    while stack:
        character = stack[0]
        previous_node = current_node
        previous_len_stack = len(stack)

        if i == 30:
            return False
        i += 1

        for origin, destiny, data in graph.out_edges(current_node, data=True):
            print(f'Pv: {previous_variable}')
            print(f'Vn: {visitedNodes}')
            if character not in T:
                print(f"{current_node}--{character}-->?")
                print(f'SyntaxError: Carácter inválido \"{character}\", na posição {len(word) - len(stack)}.')
                return False
            elif character in data['label'] and (destiny not in visitedNodes or isLoop):
                if current_node == destiny:
                    isLoop = True
                else:
                    isLoop = False

                previous_variable.append(current_node)
                previous_stack.append(stack.copy())
                visitedNodes.append(destiny)
                
                stack.pop(0)
                print(f"{current_node}--{character}-->{destiny}")
                current_node = destiny

                print('\033[31m' + stack[0] + '\033[0m' + ''.join(stack[1:])) if stack else ...
                break
            elif data['label'] == '' and destiny not in visitedNodes:
                isAmbiguous = True
                previous_stack.append(stack.copy())
                previous_variable.append(current_node)
                visitedNodes.append(destiny)
                
                print(f"{current_node}----->{destiny}")
                current_node = destiny
                break
        
        if previous_node == current_node and not isLoop and not isAmbiguous:
            print(f"{current_node}--{character}-->?")
            print('o que causa esse erro?')
            return False
        elif previous_node == current_node and not isLoop and isAmbiguous:
            if len(previous_variable) > 0 and graph.has_edge(previous_variable[-1], current_node):
                print(f"{current_node}----->{previous_variable[-1]} aqui")
                stack = previous_stack[-1].copy()
                previous_stack.pop()
                print('\033[31m' + stack[0] + '\033[0m' + ''.join(stack[1:]))
                current_node = previous_variable[-1]
                previous_variable.pop()
            elif len(visitedNodes) > 0:
                visitedNodes.pop()
        elif previous_len_stack == len(stack) and not isAmbiguous:
            print(f"{current_node}--{character}-->?")
            print(f'SyntaxError: Carácter inesperado \"{character}\", na posição {len(word) - len(stack)}.')
            return False
            
    if current_node != '$':
        expected_characters = [data['label'] for origin, destiny, data in graph.out_edges(current_node, data=True)]
        expected_characters.remove(word[-1]) if word[-1] in expected_characters else ...
        expected_characters = ', '.join(expected_characters)
        print(f'SyntaxError: Carácter(es) esperado(s): {expected_characters}, na posição {len(word) - len(stack)}.')
        return False
    
    return True

def new_validate_word(graph, word, G, current_node):
    S = G['S']
    T = G['T']
    stack = list(word)

    print(''.join(stack[:-1]) + '\033[31m' + stack[-1] + '\033[0m') if stack else ...
    while stack:
        token = stack[-1]

        out_edges = graph.out_edges(current_node, data=True)
        labels = [data['label'] for origin, destiny, data in out_edges]
        if token not in labels:
            return False

        for origin, destiny, data in out_edges:
            if token in data['label']:
                print(f"{origin}--{token}-->{destiny}")
                newStack = stack[:-1]
                if new_validate_word(graph, newStack, G, destiny):
                    return True
                else:
                    print(f"{destiny}----->{origin}")
                    print(''.join(stack[:-1]) + '\033[31m' + stack[-1] + '\033[0m') if stack else ...
    if current_node != S:
        prod = graph.get_edge_data(current_node, S)
        if prod['label'] == '':
            print(f"{current_node}----->{S}")
            current_node = S
    
    return current_node == S