from hash import hash_password
import connector

def inicioSesion(cedula, password):
    conexion = connector.conectar()
    cursor = conexion.cursor()

    password_hashed = hash_password(password)

    sql = "SELECT rol_usuario, id_usuario, nombre_usuario, apellido_usuario, estado_usuario FROM usuarios WHERE cedula = %s AND password = %s"
    cursor.execute(sql, (cedula, password_hashed))
    resultado = cursor.fetchone()

    conexion.close()
    return resultado if resultado else None