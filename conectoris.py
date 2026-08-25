import connector
from hash import hash_password


def inicioSesion(cedula, password):
    try:
        miConexion = connector.conectar()
        cursor = miConexion.cursor()

        password_hashed = hash_password(password)

        query = """SELECT rol_usuario, id_usuario, nombre_usuario, apellido_usuario, estado_usuario
        FROM usuarios WHERE cedula = %s AND password = %s"""
        cursor.execute(query, (cedula, password_hashed))
        resultado = cursor.fetchone()

        miConexion.close()
        return resultado if resultado else None
    except Exception as e:
        print(f"Error: {e}")
        return None