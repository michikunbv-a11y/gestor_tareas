import os
import connector
import getpass
import hash

def registrar_usuario(auto_rol_usuario=False):
    os.system("cls")
    print("----- REGISTRO DE NUEVO USUARIO -----")
    while True:
        cedula = input("Ingrese cédula: ")
        if len(cedula) == 10 and cedula.isdigit():
            break
        else:
            print("[!] Error: La cédula debe tener 10 dígitos.")
    while True:
        nombre = input("Ingrese su nombre: ")
        if nombre.replace(" ", "").isalpha():
            break
        else:
            print("[!] Error: El nombre solo debe contener letras.")
    while True:
        apellido = input("Ingrese su apellido: ")
        if apellido.replace(" ", "").isalpha():
            break
        else:
            print("[!] Error: El apellido solo debe contener letras.")
    direccion = input("Ingrese su dirección: ")
    while True:
        password = getpass.getpass("password: ")
        if len(password) == 5:
            confirmar = getpass.getpass("Confirme contraseña: ")
            if password == confirmar:
                contraseña_encriptada = hash.hash_password(password)

                break
            else:
                print("[!] Las contraseñas no coinciden.")
        else:
            print("[!] La contraseña debe tener 5 caracteres.")

    while True:
        print("\nSeleccione rol:")
        print("1. Administrador")
        print("2. Usuario")
        op = input("Opción: ").strip()
        if op == "1":
            rol = "administrador"
            break
        elif op == "2":
            rol = "usuario"
            break
        else:
            print("[!] Opción no válida.")

    try:
        conexion = connector.conectar()
        cursor = conexion.cursor()

        query = """INSERT INTO usuarios(cedula, nombre_usuario, apellido_usuario, direccion_usuario,estado_usuario, rol_usuario, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        datos = (cedula,nombre,apellido,direccion,"activo",rol,contraseña_encriptada)

        cursor.execute(query, datos)
        conexion.commit()

        print(f"\n[✔] Registro exitoso como '{rol}'.")

        cursor.close()
        conexion.close()

    except Exception as e:
        print(f"\n[✘] Error al registrar: {e}")

    os.system("pause")