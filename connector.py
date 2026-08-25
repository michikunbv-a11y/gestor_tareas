import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="3915623",
        database="gestor_tareas", 
        auth_plugin='mysql_native_password' 
    )