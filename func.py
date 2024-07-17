import networkx as nx
import matplotlib.pyplot as plt

def read_file(file_path):
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
            v = line.split('=')[1].strip()[1:-1].split(' ')
            v.remove('')
        elif line.startswith('T'):
            t = line.split('=')[1].strip()[1:-1].split(' ')
            t.remove('')
        elif line.startswith('P'):
            reading_P = True
            continue
        elif reading_P:
            if line == '}':
                reading_P = False
                continue
            if '->' in line:
                left_part, right_part = line.split('->')
                if '|' in line:
                    right_part = right_part.strip().split('|')
                    for production in right_part:
                        p.append((left_part.strip(), production.strip()))
                else:
                    right_part = right_part.strip()
                    p.append((left_part.strip(), right_part))
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

def validate_word(graph, word, stack, current_node, F):
    i = len(word) - len(stack)
    index_errors = [i] if len(stack) > 0 else [i-1]
    print(''.join(word[:i]) + '\033[31m' + word[i] + '\033[0m' + ''.join(word[i+1:])) if stack else ...
    while stack:
        token = stack[0]
        expected_tokens = []
        visited_nodes = []
        out_edges = graph.out_edges(current_node, data=True)
        for origin, destiny, data in out_edges:
            if token in data['label'] or data['label'] == '':
                expected_tokens.append(data['label'])

        if len(expected_tokens) == 0:
            return False, max(index_errors)

        for origin, destiny, data in out_edges:
            if token in data['label']:
                print(f"{origin}--{token}-->{destiny}")
                newStack = stack[1:]
            elif data['label'] == '':
                print(f"{origin}----->{destiny}")
                newStack = stack
            else:
                continue
            
            visited_nodes.append(destiny)
            isValid, index_error = validate_word(graph, word, newStack, destiny, F)
            index_errors.append(index_error)

            if isValid:
                return True, len(word)-1
            elif len(visited_nodes) == len(expected_tokens):
                print(f"{origin}<-----{destiny}")
                return False, max(index_errors)
            else:
                print(f"{destiny}----->{origin}")
                print(''.join(word[:i]) + '\033[31m' + word[i] + '\033[0m' + ''.join(word[i+1:])) if stack else ... 

    if current_node != F:
        prod = graph.get_edge_data(current_node, F)
        if prod:
            if prod['label'] == '&':
                print(f"{current_node}--&-->{F}")
                current_node = F

    return current_node == F, max(index_errors)

def show_graph(graph):
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', font_color='black')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_size=10)
    plt.show()