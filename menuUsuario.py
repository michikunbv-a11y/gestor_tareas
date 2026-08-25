import os
import connector
from datetime import datetime
import re

def menuUsuario(id_usuario, nombre_real):
    verificar_recordatorios_auto(id_usuario)

    while True:
        os.system("cls") 
        os.system("color 01")
        print(f"BIENVENIDO: {nombre_real.upper():<26}   ")
        print("           MENÚ DE USUARIO               ")
        print("   1. visualizar mis tareas              ")
        print("   2. Crear nueva tarea completa         ")
        print("   3. Modificar tarea                    ")
        print("   4. Eliminar mi tarea                  ")
        print("   5. Salir                              ")

        
        opcion = input("Seleccione una opción: ")
        conexion = connector.conectar()
        cursor = conexion.cursor()

        if opcion == "1":
            os.system("cls")
            print("\n--- MIS TAREAS REGISTRADAS ---")
            actualizar_estados_automatico(cursor, conexion, id_usuario)
            mostrar_tabla_actualizada(cursor, id_usuario)
            os.system("pause")

        elif opcion == "2":
            os.system("cls")
            print("\n--- CREAR NUEVA TAREA ---")

            while True:
                nombre_tarea = input("1. Nombre de la tarea: ")
                if nombre_tarea.strip():
                    break
                else:
                    print("[!] Error: El nombre de la tarea es obligatorio.")

            desc = input("2. Descripción: ")
            
            while True:
                fecha = input("3. Fecha (AAAA-MM-DD) o Enter para N/A: ")
                if not fecha:
                    fecha_val = None
                    break
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')
                    fecha_val = fecha
                    break
                except ValueError:
                    print("[!] Error: Formato de fecha inválido o contiene letras. Use AAAA-MM-DD.")

            while True:
                print("4. Prioridad: 1. Alta | 2. Media | 3. Baja")
                op_prio = input("Seleccione una opción (1-3): ")
                if op_prio == "1":
                    prio = "Alta"
                    break
                elif op_prio == "2":
                    prio = "Media"
                    break
                elif op_prio == "3":
                    prio = "Baja"
                    break
                else:
                    print("[!] Error: Ingrese solo el número de la opción (1, 2 o 3).")

            tiempo_val = "00:00:00"
            if fecha_val:
                while True:
                    tiempo = input("5. Tiempo límite (HH:MM:SS) o Enter para 00:00:00: ")
                    if not tiempo:
                        break
                    if re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$', tiempo):
                        tiempo_val = tiempo
                        break
                    else:
                        print("[!] Error: Formato de tiempo inválido. Use HH:MM:SS (ejemplo: 12:30:00).")

            tiempo_lim_tarea = f"{fecha_val} {tiempo_val}" if fecha_val else None

            query = "INSERT INTO tareas (nombre_tarea, descripcion_tarea, prioridad_tarea, tiempo_lim_tarea, estado_tarea, id_usuario) VALUES (%s, %s, %s, %s, 'Pendiente', %s)"
            cursor.execute(query, (nombre_tarea, desc, prio, tiempo_lim_tarea, id_usuario))
            conexion.commit()
            validar_y_mostrar(cursor, id_usuario)

        elif opcion == "3":
            while True:
                os.system("cls")
                print("\n--- MODIFICAR TAREA COMPLETA ---")
                mostrar_tabla_actualizada(cursor, id_usuario)
                id_t = input("\nIngrese el ID de la tarea a modificar (o 'S' para salir): ")
                
                if id_t.upper() == 'S':
                    break

                cursor.execute("SELECT id_tareas FROM tareas WHERE id_tareas = %s AND id_usuario = %s", (id_t, id_usuario))
                
                if cursor.fetchone():
                    print("\n--- Ingrese los nuevos datos ---")

                    while True:
                        nombre_tarea = input("1. Nuevo Nombre de la tarea: ")
                        if nombre_tarea.strip():
                            break
                        else:
                            print("[!] Error: El nombre de la tarea es obligatorio.")

                    desc = input("2. Nueva Descripción: ")
                    
                    while True:
                        fecha = input("3. Nueva Fecha (AAAA-MM-DD) o Enter para N/A: ")
                        if not fecha:
                            fecha_val = None
                            break
                        try:
                            datetime.strptime(fecha, '%Y-%m-%d')
                            fecha_val = fecha
                            break
                        except ValueError:
                            print("[!] Error: Formato de fecha inválido.")

                    while True:
                        print("4. Nueva Prioridad: 1. Alta | 2. Media | 3. Baja")
                        op_prio = input("Seleccione una opción (1-3): ")
                        if op_prio == "1": prio = "Alta"; break
                        elif op_prio == "2": prio = "Media"; break
                        elif op_prio == "3": prio = "Baja"; break
                        else: print("[!] Error: Seleccione una opción ")

                    tiempo_val = "00:00:00"
                    if fecha_val:
                        while True:
                            tiempo = input("5. Nuevo Tiempo límite (HH:MM:SS) o Enter para 00:00:00: ")
                            if not tiempo:
                                break
                            if re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$', tiempo):
                                tiempo_val = tiempo
                                break
                            else:
                                print("[!] Error: Use el formato HH:MM:SS.")

                    tiempo_lim_tarea = f"{fecha_val} {tiempo_val}" if fecha_val else None
                    
                    query_update = """
                        UPDATE tareas 
                        SET nombre_tarea = %s, descripcion_tarea = %s, prioridad_tarea = %s, tiempo_lim_tarea = %s 
                        WHERE id_tareas = %s AND id_usuario = %s
                    """
                    cursor.execute(query_update, (nombre_tarea, desc, prio, tiempo_lim_tarea, id_t, id_usuario))
                    conexion.commit()
                    
                    print(f"\n[✔] Tarea {id_t} modificada con éxito.")
                    os.system("pause")
                    break
                else:
                    print(f"\n[!] Error: La tarea {id_t} no existe o no tiene permiso.")
                    os.system("pause")

        elif opcion == "4":
            while True:
                os.system("cls")
                print("\n--- ELIMINAR TAREA ---")
                mostrar_tabla_actualizada(cursor, id_usuario)
                id_t = input("\nIngrese el ID de la tarea a eliminar (o 'S' para salir): ")
                
                if id_t.upper() == 'S':
                    break

                cursor.execute("SELECT id_tareas FROM tareas WHERE id_tareas = %s AND id_usuario = %s", (id_t, id_usuario))
                
                if cursor.fetchone():
                    cursor.execute("DELETE FROM tareas WHERE id_tareas = %s", (id_t,))
                    conexion.commit()
                    print(f"\n[✔] Tarea {id_t} eliminada correctamente.")
                    os.system("pause")
                    break
                else:
                    print(f"\n[!] Error: No se encontró la tarea {id_t} o no tiene permiso.")
                    os.system("pause")

        elif opcion == "5":
            conexion.close()
            break


def actualizar_estados_automatico(cursor, conexion, id_usuario):
    ahora = datetime.now()
    query = "UPDATE tareas SET estado_tarea = 'Finalizada' WHERE id_usuario = %s AND tiempo_lim_tarea < %s AND estado_tarea = 'Pendiente'"
    cursor.execute(query, (id_usuario, ahora))
    conexion.commit()

def mostrar_tabla_actualizada(cursor, id_usuario):
    query = "SELECT id_tareas, nombre_tarea, descripcion_tarea, prioridad_tarea, tiempo_lim_tarea, estado_tarea FROM tareas WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    tareas = cursor.fetchall()
    
    print("="*115)
    print("| ID |      NOMBRE      |       DESCRIPCIÓN        | PRIORIDAD |   LÍMITE (fecha y hora)   |   ESTADO   |")
    print("="*115)                  
    for tarea in tareas:
        id_tarea, nombre, desc, prio, limite, estado = tarea
        nombre_str = (nombre or "")[:16]
        desc_str = (desc or "")[:22]
        limite_str = limite.strftime('%Y-%m-%d %H:%M') if limite else "N/A"
        prio_str = prio if prio else "N/A"
        estado_str = estado or "N/A"
        print(f"| {str(id_tarea).ljust(2)} | {nombre_str.ljust(16)} | {desc_str.ljust(22)} | {prio_str.ljust(9)} | {limite_str.ljust(24)} | {estado_str.ljust(10)} |")
    print("="*115)

def validar_y_mostrar(cursor, id_usuario):
    print("\n[✔] Operación exitosa.")
    mostrar_tabla_actualizada(cursor, id_usuario) 
    os.system("pause")

def verificar_recordatorios_auto(id_usuario):
    conexion = connector.conectar() 
    cursor = conexion.cursor() 
    fecha_hoy = datetime.now().date() 
    query = "SELECT id_tareas, nombre_tarea, tiempo_lim_tarea FROM tareas WHERE id_usuario = %s AND DATE(tiempo_lim_tarea) = %s AND estado_tarea = 'Pendiente'"
    cursor.execute(query, (id_usuario, fecha_hoy)) 
    recordatorios = cursor.fetchall()
    
    if recordatorios:
        print("\n RECORDATORIOS PARA HOY ")
        for r in recordatorios:
            print(f"- {r[1]} (Límite: {r[2]})")
        os.system("pause")
    conexion.close()