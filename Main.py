# Proyecto 0 - View
# Karen Fuentes (202122467)

import Lexer
import Parser
import Comandos_Robot as Comandos_Rob


def cargar_programa_txt():
    return None

def mostrar_menu():
    print("1. Cargar archivo txt")
    print("2. Salir")

def iniciar_aplicacion():
    print("¡Bienvenido!")

    continuar = True

    lexer = Lexer()
    parser = Parser()

    while continuar:
        mostrar_menu()
        opcion_seleccionada = int(input("Por favor seleccione una opción: "))
        if opcion_seleccionada == 1:
            nombre_archivo = input("Ingresa el nombre del archivo del programa: ")
            programa = cargar_programa_txt




