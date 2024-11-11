import re

# Listas de palavras-chave (para Python)
keywords = ['print', 'if', 'else', 'while', 'for', 'def', 'return', 'import', 'class', 'try', 'except']

# Função de análise léxica
def lexical_analysis(code):
    tokens = re.findall(r"[a-zA-Z_]\w*|[0-9]+|'.*?'|[^\w\s]", code)  # Tokeniza o código
    
    # Inicializa as categorias de tokens
    categories = {
        "PALAVRA-CHAVE": 0,
        "IDENTIFICADOR": 0,
        "DELIMITADOR": 0,
        "OPERADOR": 0,
        "STRING": 0,
        "NÚMERO": 0,
        "DESCONHECIDO": 0
    }
    
    # Listas para armazenar os tokens encontrados
    tokens_found = {
        "PALAVRA-CHAVE": [],
        "IDENTIFICADOR": [],
        "DELIMITADOR": [],
        "OPERADOR": [],
        "STRING": [],
        "NÚMERO": [],
        "DESCONHECIDO": []
    }
    
    # Operadores e delimitadores possíveis
    operadores = ['+', '-', '*', '/', '%', '=', '<', '>', '==', '!=', '&&', '||']
    delimitadores = ['(', ')', '{', '}', '[', ']', ',', ';', ':']
    
    # Classificando os tokens
    for token in tokens:
        if token in keywords:
            categories["PALAVRA-CHAVE"] += 1
            tokens_found["PALAVRA-CHAVE"].append(token)
        elif token.isidentifier():
            categories["IDENTIFICADOR"] += 1
            tokens_found["IDENTIFICADOR"].append(token)
        elif token.isdigit():
            categories["NÚMERO"] += 1
            tokens_found["NÚMERO"].append(token)
        elif token.startswith("'") and token.endswith("'"):
            categories["STRING"] += 1
            tokens_found["STRING"].append(token)
        elif token in operadores:
            categories["OPERADOR"] += 1
            tokens_found["OPERADOR"].append(token)
        elif token in delimitadores:
            categories["DELIMITADOR"] += 1
            tokens_found["DELIMITADOR"].append(token)
        else:
            categories["DESCONHECIDO"] += 1
            tokens_found["DESCONHECIDO"].append(token)
    
    # Exibindo a contagem total de tokens e as categorias
    print("\nTotal de tokens: {}".format(len(tokens)))
    
    for category, count in categories.items():
        print(f"{category}: {count}")
    
    print("\nTokens encontrados:")
    for category, tokens in tokens_found.items():
        print(f"{category}:")
        for token in tokens:
            print(f"  {token}")
    
    return tokens, tokens_found

# Função de análise sintática
def syntactic_analysis(tokens):
    index = 0
    while index < len(tokens):
        token = tokens[index]
        
        # Estrutura para 'print'
        if token == 'print':
            if index + 3 < len(tokens) and tokens[index + 1] == '(' and tokens[index + 3] == ')':
                if index + 4 < len(tokens) and tokens[index + 4] == ';':
                    print("Estrutura 'print' válida com ponto e vírgula.")
                else:
                    print("Estrutura 'print' válida, mas falta o ponto e vírgula.")
            else:
                print("Erro sintático: estrutura 'print' incorreta.")
        
        elif token == 'if':
            if tokens[index + 1] == '(' and tokens[index + 3] == ')':
                print("Estrutura 'if' válida.")
            else:
                print("Erro sintático: estrutura 'if' incorreta.")
        
        elif token == 'for':
            if tokens[index + 1] == '(' and tokens[index + 4] == ')':
                print("Estrutura 'for' válida.")
            else:
                print("Erro sintático: estrutura 'for' incorreta.")
        
        index += 1

# Função de análise semântica
def semantic_analysis(tokens_found):
    declared_variables = set()
    errors = []

    # Passa por cada token identificado e faz validações semânticas
    for category, tokens in tokens_found.items():
        for token in tokens:
            if category == "PALAVRA-CHAVE" and token == 'print':
                continue  # Ignora palavras-chave no contexto semântico
            
            elif category == "IDENTIFICADOR":
                if token not in declared_variables:
                    errors.append(f"Erro semântico: variável '{token}' usada antes de ser declarada.")
                else:
                    print(f"Variável '{token}' já foi declarada.")
            
            elif category == "OPERADOR":
                if token == '=':  # Considerando '=' como declaração de variável
                    idx = tokens.index(token)
                    if idx > 0 and tokens[idx - 1] in tokens_found["IDENTIFICADOR"]:
                        declared_variables.add(tokens[idx - 1])
                        print(f"Variável '{tokens[idx - 1]}' declarada.")
                    else:
                        errors.append("Erro semântico: operador '=' sem variável de destino.")
            
            # Verifica compatibilidade de tipo
            elif category == "NÚMERO" or category == "STRING":
                for op in tokens_found["OPERADOR"]:
                    if op in ['+', '-', '*', '/'] and not all(t.isdigit() or t == token for t in tokens_found[category]):
                        errors.append("Erro semântico: operação inválida entre tipos incompatíveis.")

    if errors:
        print("\nErros Semânticos:")
        for error in errors:
            print(error)
    else:
        print("Nenhum erro semântico encontrado.")

# Programa principal
if __name__ == "__main__":
    print("Bem-vindo ao analisador léxico, sintático e semântico! Digite o código para análise (ou 'sair' para encerrar):")
    
    while True:
        code = input("Digite o código para análise: ")
        
        if code.lower() == 'sair':
            break
        else:
            tokens, tokens_found = lexical_analysis(code)
            syntactic_analysis(tokens)
            semantic_analysis(tokens_found)
