class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos_actual = 0
        self.variables_definidas = set()
        self.procedimientos_definidos = {}
        print("Tokens recibidos por el Parser:", self.tokens)
        
    def siguiente_token(self):
        if self.pos_actual < len(self.tokens):
            return self.tokens[self.pos_actual]
        return None

    def avanzar(self):
        self.pos_actual += 1

    def error(self, mensaje):
        raise Exception(f"Error de sintaxis en la posición {self.pos_actual}: {mensaje}, ")

    def verificar_punctuator(self, expected_punctuator, tipo_de:str ):
        if self.siguiente_token()[0] == "PUNCTUATOR" and self.siguiente_token()[1] == tipo_de:
            self.avanzar()
        else:
            self.error(f"Se esperaba un punctuator '{expected_punctuator}'")
        
    def tomar_si_es_punto_y_coma(self):
        # Verifica si el siguiente token es un punto y coma
        if self.siguiente_token()[0] == "PUNCTUATOR" and self.siguiente_token()[1] == ';':
            self.avanzar()
        
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
                self.avanzar() # Avanzar al siguiente token
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
        self.procedimientos_definidos[nombre] = None
        self.avanzar()
        if self.siguiente_token()[1] != "(":
            self.error("Se esperaba un '(' después del nombre del procedimiento")
        self.avanzar()
        parametros = []
        esperar_coma = False

        while self.siguiente_token()[1] != ")":
            tipo_token, valor_token = self.siguiente_token()

            if tipo_token in ['IDENTIFIER']:
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
        self.procedimientos_definidos[nombre] = len(parametros)

        if self.siguiente_token()[1] != ")":
            self.error("Se esperaba un ')' al final de la lista de parámetros")

        self.avanzar()
        self.funct_actual = nombre
        bloque_comandos = self.parse_bloque_comandos(parametros)
        self.funct_actual = ""

#BLOQUE

    def parse_bloque_comandos(self, parametros:list = []):
        comandos = []
        
        if self.siguiente_token()[1] != "{":
            self.error("Se esperaba '{' para comenzar un bloque de comandos")
        self.avanzar()
        
        while self.siguiente_token() and self.siguiente_token() != "}":
            if self.siguiente_token()[1] == "defproc":
                self.parse_programa()
            
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

    def val_var_param(self, funct:str=""):
        res = self.siguiente_token()[1] in self.variables_definidas or self.siguiente_token()[0] == "CONSTANT"
        res *= self.procedimientos_definidos.get(funct, res)
        return res 

    def parse_comando(self):
        token_actual:str = self.siguiente_token()
        brackets = 1
        while token_actual[0] != "x" or self.pos_actual == len(token_actual)-1:

            token_actual = self.siguiente_token()
            if token_actual[0] == "COMMAND":
                
                # Command jump
                if token_actual[1] == "jump":
                    self.avanzar()
                    # Verificar punctuator 'jump'
                    self.verificar_punctuator('jump', "(")
                    self.tokens:list
                    parametros = len(self.tokens[self.pos_actual:self.tokens.index(("PUNCTUATOR", ")"), self.pos_actual)])
                    if parametros == 2:
                        if ( self.val_var_param(self.funct_actual) or self.siguiente_token()[0] != "CONSTANT"):
                            self.error("Se esperaba un valor para x después de 'jump'")
                        self.avanzar()
                        self.verificar_punctuator('jump', ",")
                        if ( self.val_var_param(self.funct_actual) or self.siguiente_token()[0] != "CONSTANT"):
                            self.error("Se esperaba un valor para y después de 'jump'")
                        self.avanzar()
                        self.verificar_punctuator('jump', ")")
                    else:
                        self.error("Se esperaba dos valores para x e y después de 'jump'")
                    self.tomar_si_es_punto_y_coma()

                # Command walk
                elif token_actual[1] == "walk":
                    self.avanzar()
                    # Verificar punctuator 'walk'
                    self.verificar_punctuator('walk', "(")
                    self.tokens:list
                    parametros = len(self.tokens[self.pos_actual:self.tokens.index(("PUNCTUATOR", ")"), self.pos_actual)])
                    if parametros == 1:
                        if  ( self.val_var_param(self.funct_actual) ):
                            self.error("Se esperaba un valor o identificador para v después de 'walk'")
                        self.avanzar()
                        self.verificar_punctuator('walk', ")")
                    elif parametros == 3:
                        if  ( self.val_var_param(self.funct_actual)):
                            self.error("Se esperaba un valor o identificador para v después de 'walk'")
                        self.avanzar()
                        self.verificar_punctuator('walk', ",")
                        if ( self.val_var_param(self.funct_actual) or self.siguiente_token()[0] == "DIRECTION" or self.siguiente_token()[1] in ["front", "right", "left", "back"]):
                            self.error("Se esperaba un valor o identificador para v después de 'walk'")
                        self.avanzar()
                        self.verificar_punctuator('walk', ")")
                    else:
                        self.error("Se esperaba un valor para v después de 'walk'")
                    self.tomar_si_es_punto_y_coma()

               # Command leap
                elif token_actual[1] == "leap":
                    self.avanzar()
                    # Verificar punctuator 'leap'
                    self.verificar_punctuator('leap', "(")
                    self.tokens:list
                    parametros = len(self.tokens[self.pos_actual:self.tokens.index(("PUNCTUATOR", ")"), self.pos_actual)])
                    if parametros == 1:
                        if  ( self.val_var_param(self.funct_actual) ):
                            self.error("Se esperaba un valor o identificador para v después de 'leap'")
                        self.avanzar()
                        self.verificar_punctuator('leap', ")")
                    elif parametros == 3:
                        if  ( self.val_var_param(self.funct_actual)):
                            self.error("Se esperaba un valor o identificador para v después de 'leap'")
                        self.avanzar()
                        self.verificar_punctuator('leap', ",")
                        if ( self.val_var_param(self.funct_actual) or self.siguiente_token()[0] == "DIRECTION" or self.siguiente_token()[1] in ["front", "right", "left", "back"]):
                            self.error("Se esperaba un valor o identificador para v después de 'leap'")
                        self.avanzar()
                        self.verificar_punctuator('leap', ")")
                    else:
                        self.error("Se esperaba un valor para v después de 'leap'")
                    self.tomar_si_es_punto_y_coma()
                    
                # Command turnto
                elif token_actual[1] == "turnto":
                    self.avanzar()
                    # Verificar punctuator 'turnto'
                    self.verificar_punctuator('turnto', "(")
                    # Verificar dirección O
                    if self.siguiente_token()[0] == "DIRECTION" and self.siguiente_token()[1] in ["north", "south", "east", "west"]:
                        self.avanzar()
                    else:
                        self.error("Se esperaba 'north', 'south', 'east' o 'west' después de 'turnto'")
                    # Verificar punctuator ')'
                    self.verificar_punctuator('turnto', ")")
                    self.tomar_si_es_punto_y_coma()

                # Command turn
                elif token_actual[1] == "turn":
                    self.avanzar()
                    # Verificar punctuator '('
                    if self.siguiente_token()[1] != "(":
                        self.error("Se esperaba '(' después de 'turn'")
                    self.avanzar()
                    # Verificar dirección D
                    direccion = self.siguiente_token()[1]
                    # Verificar que D sea un valor válido
                    if direccion not in ["left", "right", "around"]:
                        self.error(f"Valor no válido para D en 'turn': {direccion}")
                    self.avanzar()
                    # Verificar punctuator ')'
                    if self.siguiente_token()[1] != ")":
                        self.error("Se esperaba ')' después de la dirección en 'turn'")
                    self.tomar_si_es_punto_y_coma()

                # Command drop
                elif token_actual[1] == "drop":
                    self.avanzar()
                    # Verificar punctuator 'drop'
                    self.verificar_punctuator('drop', "(")
                    # Verificar valor v
                    if (self.siguiente_token()[0] != "IDENTIFIER") and (self.siguiente_token()[0] != "CONSTANT"):
                        self.error("Se esperaba un valor o identificador para v después de 'drop'")
                    self.avanzar()
                    # Verificar punctuator 'drop'
                    self.verificar_punctuator('drop', ")")
                    self.tomar_si_es_punto_y_coma()

                # Command get
                elif token_actual[1] == "get":
                    self.avanzar()
                    # Verificar punctuator 'get'
                    self.verificar_punctuator('get', "(")
                    # Verificar valor v
                    if (self.siguiente_token()[0] != "IDENTIFIER") and (self.siguiente_token()[0] != "CONSTANT"):
                        self.error("Se esperaba un valor o identificador para v después de 'get'")
                    self.avanzar()
                    # Verificar punctuator 'get'
                    self.verificar_punctuator('get', ")")
                    self.tomar_si_es_punto_y_coma()

                # Command grab
                elif token_actual[1] == "grab":
                    self.avanzar()
                    # Verificar punctuator 'grab'
                    self.verificar_punctuator('grab', "(")
                    # Verificar valor v
                    if (self.siguiente_token()[0] != "IDENTIFIER") and (self.siguiente_token()[0] != "CONSTANT"):
                        self.error("Se esperaba un valor o identificador para v después de 'grab'")
                    self.avanzar()
                    # Verificar punctuator 'grab'
                    self.verificar_punctuator('grab', ")")
                    self.tomar_si_es_punto_y_coma()
                   
                # Command letGo
                elif token_actual[1] == "letgo":
                    self.avanzar()
                    # Verificar punctuator 'letgo'
                    self.verificar_punctuator('letgo', "(")
                    # Verificar valor v
                    if not (not self.val_var_param(self.funct_actual) and (self.siguiente_token()[0] != "CONSTANT")):
                        self.error("Se esperaba un valor o identificador para v después de 'letGo'")
                    self.avanzar()
                    # Verificar punctuator 'letgo'
                    self.verificar_punctuator('letgo', ")")
                    self.tomar_si_es_punto_y_coma()
                   
                # Command nop
                elif token_actual[1] == "nop":
                    self.avanzar()
                    # Verificar punctuator 'nop'
                    self.verificar_punctuator('nop', "(")
                    # No requiere ningún otro token o verificación. No realiza ninguna acción.
                    self.verificar_punctuator('nop', ")")
                    self.tomar_si_es_punto_y_coma()
   
            elif token_actual[0] == "PUNCTUATOR":
                if token_actual[1] == "{":
                    self.avanzar()
                    brackets += 1
                elif token_actual[1] == "}":
                    brackets -= 1
                    if brackets == 0:
                        return True
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
