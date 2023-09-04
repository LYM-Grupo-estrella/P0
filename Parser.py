class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos_actual = 0
        self.variables_definidas = set()
        self.procedimientos_definidos = set()
        print("Tokens recibidos por el Parser:", self.tokens)
        

    def siguiente_token(self):
        if self.pos_actual < len(self.tokens):
            return self.tokens[self.pos_actual]
        return None

    def avanzar(self):
        self.pos_actual += 1

    def error(self, mensaje):
        raise Exception(f"Error de sintaxis en la posición {self.pos_actual}: {mensaje}, ")


    # ... (resto del código)

    def parse_programa(self):
        try:
            while self.siguiente_token() is not None:
                token_actual = self.siguiente_token()
                
                if token_actual[0] == 'KEYWORD':
                    if token_actual[1] == "defvar":
                        self.parse_definicion_variable()
                    elif token_actual[1] == "defproc":
                        self.parse_definicion_procedimiento()
                    else:
                        self.error(f"Token no reconocido: {token_actual[1]}")
                else:
                    self.parse_comando()
                
                self.avanzar()  # Avanzar al siguiente token

            return True  # Si todo es correcto    

        except Exception as e:
            print(f"Error: {e}")  # Imprime el error
            return False  # Indica que hubo un error

#KEYWORDS

    def parse_definicion_variable(self):
        self.avanzar()

        if self.siguiente_token()[0] != 'IDENTIFIER':
            self.error("Se esperaba un nombre de variable después de 'defVar'")

        nombre = self.siguiente_token()[1]

         # Verificar si la variable ya ha sido definida
        if nombre in self.variables_definidas:
            self.error(f"Variable '{nombre}' ya ha sido definida anteriormente")

        self.avanzar()

        if self.siguiente_token()[0] != 'CONSTANT':
            self.error(f"Se esperaba un valor inicial para la variable '{nombre}'")
        valor = self.siguiente_token()[1]

        self.variables_definidas.add(nombre)

    def parse_definicion_procedimiento(self):
        self.avanzar()
        
        if self.siguiente_token()[0] != 'IDENTIFIER':
            self.error("Se esperaba un nombre de procedimiento después de 'defProc'")
        nombre = self.siguiente_token()[1]
        
        self.avanzar()
        if self.siguiente_token()[1] != "(":
            self.error("Se esperaba un '(' después del nombre del procedimiento")
        
        self.avanzar()
        parametros = []
        esperar_coma = False

        while self.siguiente_token()[1] != ")":
            tipo_token, valor_token = self.siguiente_token()

            if tipo_token in ['IDENTIFIER', 'CONSTANT']:
                if esperar_coma:
                    self.error("Se esperaba una ',' entre los parámetros")
                parametros.append(valor_token)
                esperar_coma = True
            elif valor_token == ",":
                if not esperar_coma:
                    self.error("Coma inesperada o parámetros consecutivos sin comas")
                esperar_coma = False
            else:
                self.error(f"Token no válido en la lista de parámetros: {valor_token}")

            self.avanzar()

        if self.siguiente_token()[1] != ")":
            self.error("Se esperaba un ')' al final de la lista de parámetros")

        self.avanzar()
        bloque_comandos = self.parse_bloque_comandos()


#BLOQUE

    def parse_bloque_comandos(self):
        comandos = []
        
        if self.siguiente_token()[1] != "{":
            self.error("Se esperaba '{' para comenzar un bloque de comandos")
        self.avanzar()
        
        while self.siguiente_token() and self.siguiente_token() != "}":
            comando = self.parse_comando()
            if comando:
                comandos.append(comando)
            else:
                self.error(f"Comando no válido: {self.siguiente_token()}")
            self.avanzar()
        
        if not self.siguiente_token() or self.siguiente_token() != "}":
            self.error("Se esperaba '}' para cerrar el bloque de comandos")
        self.avanzar()  # Salir del bloque
        
        return comandos


    def parse_comando(self):
        token_actual = self.siguiente_token()

        if token_actual[0] == "COMMAND":
            if token_actual[1] == "jump":
                self.avanzar()
                
                # Verificar x
                if self.siguiente_token()[0] != 'CONSTANT':
                    self.error("Se esperaba un valor para x después de 'jump'")
                self.avanzar()
                
                # Verificar y
                if self.siguiente_token()[0] != 'CONSTANT':
                    self.error("Se esperaba un valor para y después de x en 'jump'")
                self.avanzar()

            elif token_actual[1] == "walk":
                self.avanzar()
                
                # Verificar v
                if self.siguiente_token()[0] != 'CONSTANT':
                    self.error("Se esperaba un valor para v después de 'walk'")
                self.avanzar()
                
                # Verificar dirección D u O
                if self.siguiente_token()[0] == "DIRECTION" or self.siguiente_token()[1] in ["front", "right", "left", "back"]:
                    self.avanzar()
                else:
                    self.error(f"Se esperaba una dirección válida después de 'walk', pero se encontró {self.siguiente_token()[1]}")

            elif token_actual[1] == "walk":
                None

        else:
            self.error(f"Comando no reconocido: {token_actual[1]}")



       

#AUXILIARES

def manejar_parentesis(self):
    contador = 0
    parametros = []

    while self.siguiente_token() is not None:
        token_actual = self.siguiente_token()[1]

        if token_actual == "(":
            contador += 1
        elif token_actual == ")":
            contador -= 1
            if contador == 0:  # Si hemos cerrado todos los paréntesis abiertos
                break
        else:
            parametros.append(token_actual)

        self.avanzar()

    if contador != 0:
        self.error("Los paréntesis no están correctamente emparejados")

    return parametros


Tokens = [('KEYWORD', 'defvar'), ('IDENTIFIER', 'nom'), ('CONSTANT', '1'), ('KEYWORD', 'defproc'), ('IDENTIFIER', 'putcb'), ('PUNCTUATOR', '('), ('IDENTIFIER', 'c'), ('PUNCTUATOR', ','), ('IDENTIFIER', 'b'),('PUNCTUATOR', ')')]
parser = Parser(Tokens)
parser.parse_programa()
#print("Variables definidas:", parser.variables_definidas)

