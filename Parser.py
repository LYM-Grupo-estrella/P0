class Parser :

    # Constructor

    def __init__(self,tokens):
        self.tokens = tokens
        self.pos_actual = 0

    def siguiente_token(self):
        if self.pos_actual < len(self.tokens):
            return self.tokens[self.pos_actual]
        return None
    
    def avanzar(self):
        self.pos_actual +=1

    def parse_programa(self):
        definiciones = []
        while self.siguiente_token() is not None:
            definicion = self.parse_definicion()
            if definicion:
                definiciones.append(definicion)
            else:
                self.avanzar()
                

    def parse_definicion(self):
        token = self.siguiente_token()
    
