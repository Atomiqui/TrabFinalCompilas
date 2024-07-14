import networkx as nx
import threading
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

def show_graph(graph, pos, colors, font_color='black'):
    nx.draw(
        graph,
        pos, 
        with_labels=True,
        node_size=2000,
        node_color=colors,
        edgecolors='black',
        arrowstyle="<|-",
        font_size=16
    )
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color=font_color)
    plt.show()
    return pos

def update_graph_view(graph, pos, colors, font_color='black'):
    nx.draw(
        graph,
        pos, 
        with_labels=True,
        node_size=2000,
        node_color=colors,
        edgecolors='black',
        arrowstyle="<|-",
        font_size=16
    )
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color=font_color)
    plt.show()

def validate_word(graph, word, G):
    current_node = G['S']
    T = G['T']
    isLoop = False
    isAmbiguous = False
    previous_variable = current_node
    visitedNodes = []
    stack = list(word)

    pos = nx.spring_layout(graph)
    graph_nodes = graph.nodes()
    index = list(graph_nodes).index(current_node)
    colors = ['blue' if i == index else 'white' for i in range(len(graph_nodes))]
    pos = show_graph(graph, pos, colors)

    print(f"Validando {word}:")
    while stack:
        w = stack[0]

        previous_node = current_node
        previous_len_stack = len(stack)

        #print('\033[31m' + stack[0] + '\033[0m' + ''.join(stack[1:]))
        for origin, destiny, data in graph.out_edges(current_node, data=True):
            if w not in T:
                print(f"{current_node}--{w}-->?")
                index = list(graph_nodes).index(current_node)
                colors = ['red' if i == index else 'white' for i in range(len(graph_nodes))]
                show_graph(graph, pos, colors, 'red')
                return False
            elif w in data['label']:
                if current_node == destiny:
                    isLoop = True
                else:
                    isLoop = False
                
                stack.pop(0)
                isAmbiguous = False
                visitedNodes = []

                print(f"{current_node}--{w}-->{destiny}")
                current_node = destiny
                index = list(graph_nodes).index(current_node)
                colors = ['blue' if i == index else 'white' for i in range(len(graph_nodes))]
                show_graph(graph, pos, colors)
                
                break
            elif data['label'] == '' and destiny not in visitedNodes:
                isAmbiguous = True
                previous_variable = current_node
                visitedNodes.append(destiny)
                
                print(f"{current_node}----->{destiny}")
                current_node = destiny
                index = list(graph_nodes).index(current_node)
                colors = ['blue' if i == index else 'white' for i in range(len(graph_nodes))]
                show_graph(graph, pos, colors)
                
                break
        
        if previous_node == current_node and not isLoop and not isAmbiguous:
            print(f"{current_node}--{w}-->?")
            index = list(graph_nodes).index(current_node)
            colors = ['red' if i == index else 'white' for i in range(len(graph_nodes))]
            show_graph(graph, pos, colors, 'red')

            return False
        elif previous_node == current_node and not isLoop and isAmbiguous:
            print(f"{current_node}----->{previous_variable}")
            current_node = previous_variable
            index = list(graph_nodes).index(current_node)
            colors = ['blue' if i == index else 'white' for i in range(len(graph_nodes))]
            show_graph(graph, pos, colors, 'red')
            
        elif previous_len_stack == len(stack) and not isAmbiguous:
            print(f"{current_node}--{w}-->?")
            index = list(graph_nodes).index(current_node)
            colors = ['red' if i == index else 'white' for i in range(len(graph_nodes))]
            show_graph(graph, pos, colors, 'red')

            return False
    return current_node == '$'