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
            if '->' in line:
                parte_esquerda, parte_direita = line.split('->')
                parte_direita = parte_direita.strip().rstrip(',')
                p.append((parte_esquerda.strip(), parte_direita))
            else:
                raise ValueError(f"Formato de produção inválido: {line}")
        elif line.startswith('S'):
            s = line.split('=')[1].strip()

    return {'V': v, 'T': t, 'P': p, 'S': s}

def validar_gld(gramatica):
    v = gramatica['V']
    t = gramatica['T']
    regras = gramatica['P']
    simbolo_inicial = gramatica['S']

    print(f"Variáveis: {v}")
    print(f"t: {t}")
    print(f"Regras: {regras}")
    print(f"Símbolo Inicial: {simbolo_inicial}")

    # Verificar se o símbolo inicial está no conjunto de variáveis
    if simbolo_inicial not in v:
        print(f"Símbolo inicial {simbolo_inicial} não está no conjunto de variáveis.")
        return False

    for variavel, producao in regras:
        # A parte esquerda da produção deve ser uma única variável
        if variavel not in v:
            print(f"Variável {variavel} não está no conjunto de variáveis.")
            return False

        # A parte direita da produção deve ser um terminal seguido de, no máximo, uma variável
        if len(producao) == 1 and producao in t:
            continue
        elif len(producao) == 2 and producao[0] in t and producao[1] in v:
            continue
        else:
            print(f"Produção {producao} é inválida.")
            return False

    return True
