def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def read_grammar(file_path):
    p = []
    reading_P = False

    lines = read_file(file_path)
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
    print(f"S: {S}")

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