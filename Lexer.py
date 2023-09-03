def lexer(programa):
    tokens = []
    for cadena in programa.split():
        if cadena in ['defVar', 'defProc', 'if', 'else', 'while', 'repeat']:
            tokens.append(('KEYWORD', cadena))
        elif cadena == '=':
            tokens.append(('OPERATOR', cadena))
        elif cadena.isdigit():
            tokens.append(('CONSTANT', cadena))
        elif cadena == ';':
            tokens.append(('PUNCTUATOR', cadena))
        elif cadena == ';':
            tokens.append(('IDENTIFIER', cadena))
        else:
            tokens.append(('LITERAL', cadena))
    return tokens