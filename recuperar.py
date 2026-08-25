import connector
import os
import getpass
import hash

def recuperar_password():
    os.system("cls")
    print("--- RESTABLECER CONTRASEÑA ---")
    id_usuario = input("Ingrese su ID de usuario: ")

    try:
        conexion = connector.conectar()
        cursor = conexion.cursor()

        query_verificar = "SELECT cedula FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query_verificar, (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            print(f"\n[!] Usuario '{id_usuario}' encontrado.")

            while True:
                nueva_pass = getpass.getpass("Ingrese su nueva contraseña (5 dígitos): ")
                if len(nueva_pass) == 5:
                    confirmacion = getpass.getpass("Confirme su nueva contraseña: ")
                    if nueva_pass == confirmacion:
                        break
                    else:
                        print("\n[!] Las contraseñas no coinciden.")
                else:
                    print(f"\n[!] Error: Debe tener exactamente 5 dígitos.")

            nueva_pass_hashed = hash.hash_password(nueva_pass)

            query_update = "UPDATE usuarios SET password = %s WHERE id_usuario = %s"
            cursor.execute(query_update, (nueva_pass_hashed, id_usuario))
            conexion.commit()

            print(f"\n[!] Contraseña actualizada con éxito.")
        else:
            print(f"\n[!] El usuario '{id_usuario}' no se encuentra registrado.")

        conexion.close()
    except Exception as e:
        print(f"Error: {e}")

    input("\nPresione Enter para volver...")