class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos_actual = 0

    def siguiente_token(self):
        if self.pos_actual < len(self.tokens):
            return self.tokens[self.pos_actual].lower()  # Convertir a minúsculas para manejar insensibilidad de mayúsculas/minúsculas
        return None

    def avanzar(self):
        self.pos_actual += 1

    def error(self, mensaje):
        raise Exception(f"Error de sintaxis en la posición {self.pos_actual}: {mensaje}")

    # ... (resto del código)

    def parse_programa(self):
        definiciones = []
        comandos = []
        while self.siguiente_token() is not None:
            if self.siguiente_token() == "defvar":
                definicion = self.parse_definicion_variable()
                if definicion:
                    definiciones.append(definicion)
            elif self.siguiente_token() == "defproc":
                definicion = self.parse_definicion_procedimiento()
                if definicion:
                    definiciones.append(definicion)
            else:
                comando = self.parse_comando()
                if comando:
                    comandos.append(comando)
            self.avanzar()  # Mover esta línea aquí para avanzar al siguiente token
        return definiciones, comandos

    def parse_definicion_procedimiento(self):
        self.avanzar()
        nombre = self.siguiente_token()
        if not nombre:
            self.error("Se esperaba un nombre de procedimiento después de 'defProc'")
        self.avanzar()
        parametros = self.siguiente_token().strip("()").split(",")  # Asumiendo que los parámetros están entre paréntesis y separados por comas
        # No avanzar aquí
        # self.avanzar()
        bloque_comandos = self.parse_bloque_comandos()
        return ("Procedimiento", nombre, parametros, bloque_comandos)

    def parse_definicion_variable(self):
        self.avanzar()
        nombre = self.siguiente_token()
        if not nombre:
            self.error("Se esperaba un nombre de variable después de 'defVar'")
        self.avanzar()
        valor = self.siguiente_token()
        if not valor:
            self.error(f"Se esperaba un valor inicial para la variable '{nombre}'")
        return ("Variable", nombre, valor)

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


