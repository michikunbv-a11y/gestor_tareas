import getpass
import os
import conectoris
import menuAdministrador
import menuUsuario
import recuperar
import registro
import hash


def mostrar_bienvenida():
    os.system("cls")
    os.system("color 02")
    print("\n" + "="*50)
    print("          BIENVENIDO AL  SISTEMA DE GESTOR DE TAREAS          ")
    print("="*50 + "\n")
    input("       PRESIONE UNA TECLA PARA CONTINUAR...")

def mostrar_menu_principal():
    os.system("cls")
    os.system("color 08")
    print("             GESTOR DE TAREAS            ")
    print("    1) Iniciar Sesión                    ")
    print("    2) Registrarse                       ")
    print("    3) Recuperar Contraseña              ")
    print("    4) Salir                             ")

mostrar_bienvenida()

while True:
    mostrar_menu_principal()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        intentando = True
        while intentando:
            os.system("cls")
            print("--- INICIO DE SESIÓN ---")
            cedula = input("cedula: ")
            Password = getpass.getpass("Contraseña: ")

            datos_login = conectoris.inicioSesion(cedula, Password)

            if datos_login:
                rol, id_usuario, nombre, apellido, estado = datos_login

                if estado == "inactivo":
                    print("\n[!] permiso denegado: usuario inactivo.")
                    os.system("pause")
                    intentando = False
                else:
                    nombre_completo = f"{nombre} {apellido}"
                    if rol == "administrador":
                        menuAdministrador.menuAdministrador()
                    elif rol == "usuario":
                        menuUsuario.menuUsuario(id_usuario, nombre_completo)
                    intentando = False
            else:
                print("\n[!] Error: cedula o contraseña incorrectos.")
                print("1. Reintentar | 2. volver al menú")
                reintento = input("Opción: ")
                if reintento != "1":
                    intentando = False

    elif opcion == "2":
        registro.registrar_usuario(auto_rol_usuario=True)

    elif opcion == "3":
        recuperar.recuperar_password()

    elif opcion == "4":
        print("Saliendo del sistema...")
        break

    else:
        input("Opción no válida. Presione Enter...")
        

