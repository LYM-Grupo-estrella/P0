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
        raise Exception(f"Error de sintaxis en la posición {self.pos_actual}: {mensaje}")

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
        if not self.siguiente_token()[1].startswith("(") or not self.siguiente_token()[1].endswith(")"):
            self.error("Se esperaban parámetros entre paréntesis después del nombre del procedimiento")
        parametros = self.siguiente_token()[1].strip("()").split(",")  # Extraer parámetros
    
        self.avanzar()
        bloque_comandos = self.parse_bloque_comandos()

#BLOQUE

    def parse_bloque_comandos(self):
        comandos = []
        if self.siguiente_token() != "{":
            self.error("Se esperaba '{' para comenzar un bloque de comandos")
        self.avanzar()
        while self.siguiente_token() != "}":
            comando = self.parse_comando()
            if comando:
                comandos.append(comando)
            else:
                self.error(f"Comando no válido: {self.siguiente_token()}")
            self.avanzar()
        return comandos

    def parse_comando(self):
        # Aquí deberías agregar la lógica para analizar cada tipo de comando
        # Por simplicidad, solo manejaré el comando "walk" como ejemplo
        if self.siguiente_token() == "walk":
            self.avanzar()
            parametros = self.siguiente_token().strip("()").split(",")
            return ("walk", parametros)
        # Agregar otros comandos aquí
        return None

Tokens = [('KEYWORD', 'defvar'), ('IDENTIFIER', 'nom'), ('CONSTANT', '1'), ('KEYWORD', 'defproc'), ('IDENTIFIER', 'putcb'), ('PUNCTUATOR', '('), ('IDENTIFIER', 'c'), ('PUNCTUATOR', ','), ('IDENTIFIER', 'b'),('PUNCTUATOR', ')')]
parser = Parser(Tokens)
parser.parse_programa()
print("Variables definidas:", parser.variables_definidas)

