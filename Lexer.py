class Lexer:
    
    def lexer(self,programa):
        tokens = []
        for cadena in programa.split():
            if cadena in ['defvar', 'defproc', 'if', 'else', 'while', 'repeat']:
                tokens.append(('KEYWORD', cadena))
            elif cadena == '=': 
                tokens.append(('OPERATOR', cadena))
            elif cadena.isdigit():
                tokens.append(('CONSTANT', cadena))
            elif cadena in ['(',')',',',';','{','}']:
                tokens.append(('PUNCTUATOR', cadena))
            elif cadena in ['jump','walk','leap','turn', 'turnto','drop','get','grab', 'letgo','nop']:
                tokens.append(('COMMAND',cadena))
            elif cadena in ['facing','can','not']:
                tokens.append(('CONDITION',cadena))
            elif cadena in ['north','south','west','east']:
                tokens.append(('DIRECTION',cadena))
            else: 
                tokens.append(('IDENTIFIER', cadena))
        return tokens