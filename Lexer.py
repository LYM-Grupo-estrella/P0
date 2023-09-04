class Lexer:
    
    def lexer(self,programa):

        """Recibe una lista formateada de cada linea del programa, 
        se separa por espacios y categoriza de acuerdo a su funcionalidad entre: 
        KEYWORD, OPERATOR, CONSTANT, PUNCTUATOR, COMMAND, CONDITION, DIRECTION, 
        y si no cumple con cualquiera de las condiciones establecidas se asigna como IDENTIFIER.
        Retorna una lista de tokens con el formato (TOKEN,cadena)"""

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