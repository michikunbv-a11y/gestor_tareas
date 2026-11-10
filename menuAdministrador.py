import os
import registro
import connector

def menuAdministrador():
    while True:
        os.system("cls")
        os.system("color 05")

        print("        MENÚ ADMINISTRADOR              ")
        print("  1. Gestión de usuarios                ")
        print("  2. Visualización de usuarios          ")
        print("  3. Inactivar usuario                  ")
        print("  4. Activar usuario                    ")
        print("  5. Salir                              ")

        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registro.registrar_usuario()
        elif opcion == "2":
            visualizar_usuarios()
        elif opcion == "3":
            inactivar_usuario()
        elif opcion == "4":
            activar_usuario()
        elif opcion == "5":
            break
        else:
            print("[!] Opción no válida.")
            os.system("pause")

def visualizar_usuarios():
    os.system("cls")
    try:
        conexion = connector.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT cedula, nombre_usuario, apellido_usuario, rol_usuario, estado_usuario FROM usuarios")
        usuarios = cursor.fetchall()
        
        print("\n--- LISTADO GENERAL DE USUARIOS ---")
        print(f"{'CÉDULA':<12} | {'NOMBRE REAL':<25} | {'ROL':<14} | {'ESTADO':<10}")
        print("-" * 75)
        
        for u in usuarios:
            nom_real = f"{u[1]} {u[2]}"[:25]
            estado_texto = "ACTIVO" if u[4] == "activo" else "INACTIVO"
            print(f"{str(u[0]):<12} | {nom_real:<25} | {str(u[3]):<14} | {estado_texto:<10}")
        
        conexion.close()
    except Exception as e:
        print(f"Error: {e}")
    input("\nPresione Enter para volver...")
def inactivar_usuario():
    os.system("cls")
    try:
        conexion = connector.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT cedula, nombre_usuario, apellido_usuario FROM usuarios WHERE estado_usuario = 'activo'")
        usuarios = cursor.fetchall()
        
        print("\n--- INACTIVAR USUARIO  ---")
        if not usuarios:
            print("No hay usuarios activos para inactivar.")
        else:
            print("="*75)
            print(f"{'CÉDULA':<12} | {'NOMBRE REAL':<25}")
            print("-" * 75)
            
            for u in usuarios:
                nom_real = f"{u[1]} {u[2]}"[:25]
                print(f"{str(u[0]):<12} | {nom_real:<25}")
            print("="*75)
            
            target = input("\nIngrese la CÉDULA del usuario a inactivar (o Enter para cancelar): ")
            if target:
                query_check = "SELECT cedula FROM usuarios WHERE cedula = %s AND estado_usuario = 'activo'"
                cursor.execute(query_check, (target,))
                
                if cursor.fetchone():
                    query = "UPDATE usuarios SET estado_usuario = 'inactivo' WHERE cedula = %s"
                    cursor.execute(query, (target,))
                    conexion.commit()
                    print(f"\n[!] Usuario con cédula '{target}' inactivado con éxito.")
                else:
                    print(f"\n[!] Error: La cédula '{target}' no existe o ya está inactiva.")
        
        conexion.close()
    except Exception as e:
        print(f"Error: {e}")
    input("\nPresione Enter para volver...")

def activar_usuario():
    os.system("cls")
    try:
        conexion = connector.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT cedula, nombre_usuario, apellido_usuario FROM usuarios WHERE estado_usuario = 'inactivo'")
        usuarios = cursor.fetchall()
        
        print("\n--- ACTIVAR USUARIO ---")
        if not usuarios:
            print("No hay usuarios inactivos.")
        else:
            for u in usuarios:
                print(f"Cédula: {u[0]} | Nombre: {u[1]} {u[2]}")
            
            target = input("\nIngrese la CÉDULA del usuario a activar: ")
            if target:
                
                query = "UPDATE usuarios SET estado_usuario = 'activo' WHERE cedula = %s"
                cursor.execute(query, (target,))
                conexion.commit()
                print(f"\n[✔] Usuario con cédula '{target}' activado con éxito.")
        
        conexion.close()
    except Exception as e:
        print(f"Error: {e}")
    input("\nPresione Enter para volver...")