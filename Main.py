# Proyecto 0 - View
# Karen Fuentes (202122467)
# Paula Estupiñan (202212331)

from Lexer import Lexer
from Parser import Parser

def cargar_programa_txt(nombre_archivo) -> list:
    "retorna lista de strings"
    try:
        with open(nombre_archivo, 'r') as archivo:
            programa = archivo.readlines()
            return programa
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no fue encontrado.")
        return []

def limpiador_elemento(elemento) -> str:
    elem_limpio = elemento.replace('\n', '').replace('\t', '')
    elem_limpio = elem_limpio.lower()
    delimitadores = ['(', ')', ',', ';', '{', '}', '=']
    for punct in delimitadores:
        elem_limpio = elem_limpio.replace(punct, f' {punct} ')
    elem_limpio = ' '.join(elem_limpio.split())
    return elem_limpio

def iterador_limpiar_lista(lista) -> list:
    lista_limpia = []
    for item in lista:
        item_limpio = limpiador_elemento(item)
        if item_limpio:
            lista_limpia.append(item_limpio)
    return lista_limpia

def mostrar_menu():
    print("1. Cargar archivo txt")
    print("2. Salir")


# ... Código anterior ...

def verificar_gramatica(tokens):
    stack = []
    for token, value in tokens:
        if token == "PUNCTUATOR":
            if value == "{":
                stack.append(value)
                print(f"Pushed '{{' onto stack. Current stack: {stack}")
            elif value == "}":
                if not stack or stack[-1] != "{":
                    print(f"Error: Se encontró un '}}' sin un '{{' correspondiente. Token: {value}")
                    return False, "Error: Se encontró un '{' sin un '}' correspondiente."
                stack.pop()
                print(f"Popped '{{' from stack. Current stack: {stack}")
    if stack:
        return False, f"Error: Se encontró un '{{' sin un '}}' correspondiente. Token: {stack[-1]}"
    return True, "La gramática es correcta y la correspondencia de llaves es válida."

# ... Resto del código ...



def iniciar_aplicacion():
    print("¡Bienvenido!")

    continuar = True
    lexer_instance = Lexer()
    parser = Parser([])  # Inicializamos con una lista vacía

    while continuar:
        mostrar_menu()
        opcion_seleccionada = (input("Por favor seleccione una opción: "))
        
        if not opcion_seleccionada.isdigit():
            print("Por favor, ingrese un número válido.")
            continue

        opcion_seleccionada = int(opcion_seleccionada)
        
        if opcion_seleccionada == 1:
            print(" ")
            print(f"¡Asegurese que el programa este en la carpeta de P0!")
            nombre_archivo = input("Ingresa el nombre del archivo del programa: ")
            programa_list = cargar_programa_txt(nombre_archivo)
            print(" ")
            print(programa_list)
            print(" ")
            programa_list = iterador_limpiar_lista(programa_list)
            print(" ")
            print(programa_list)
            print(" ")
            tokens = []
            for item in programa_list:
                ans = lexer_instance.lexer(item)
                tokens.extend(ans)  # Usamos extend en lugar de append para agregar todos los tokens a la lista
            
            print(" ")
            print(tokens)
            print(" ")

            es_correcto, mensaje = verificar_gramatica(tokens)
            if es_correcto:
                print("La gramática es correcta.")
            else:
                print(mensaje,flush=True)

        elif opcion_seleccionada == 2:
            continuar = False
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

iniciar_aplicacion()
