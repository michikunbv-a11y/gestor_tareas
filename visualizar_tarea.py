import connector

def visualizar_tareas(id_usuario):
    db = connector.conectar()
    cursor = db.cursor()
    query = "SELECT descripcion_tarea, tiempo_lim_tarea FROM tareas WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    
    for (descripcion, tiempo_lim_tarea) in cursor:
        print(f"Tarea: {descripcion} - Vence: {tiempo_lim_tarea}")
    
    db.close()