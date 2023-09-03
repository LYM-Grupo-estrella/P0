# Proyecto 0 - View
# Karen Fuentes (202122467)

import Lexer
import Parser
import Comandos_Robot as Comandos_Rob


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
    elem_limpio = elemento.lower()
    delimitadores = ['(', ')', ',', ';', '{', '}', '=']
    for punct in delimitadores:
        elem_limpio = elem_limpio.replace(punct, f' {punct} ')
    elem_limpio = ' '.join(elem_limpio.split())
    
    return elem_limpio

def iterador_limpiar_lista(lista) -> list:
    lista_limpia = []
    for item in lista:
        item_limpio = limpiador_elemento(item)
        lista_limpia.append(item_limpio)
    return lista_limpia

def mostrar_menu():
    print("1. Cargar archivo txt")
    print("2. Salir")

def iniciar_aplicacion():
    print("¡Bienvenido!")

    continuar = True

    #lexer = Lexer()
    #parser = Parser()

    while continuar:
        mostrar_menu()
        opcion_seleccionada = int(input("Por favor seleccione una opción: "))
        if opcion_seleccionada == 1:
            print(" ")
            print(f"¡Asegurese que el programa este en la carpeta de P0!")
            nombre_archivo = input("Ingresa el nombre del archivo del programa: ")
            programa_list = cargar_programa_txt(nombre_archivo)
            print(" ")
            print(programa_list) #quitar
            print(" ")
            programa_list = iterador_limpiar_lista(programa_list)
            print(" ")
            print(programa_list) #quitar
            print(" ")
            tokens = []
            for item in programa_list:
                ans = Lexer.lexer(item)
                tokens.append(ans)
            print(" ")
            print(tokens)
            print(" ")
        

iniciar_aplicacion()




