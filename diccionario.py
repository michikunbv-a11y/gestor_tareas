import json

def guardar_diccionario(diccionario, nombre_archivo):
    """Guarda un diccionario en un archivo JSON."""
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(diccionario, archivo, indent=4, ensure_ascii=False)


def cargar_diccionario(nombre_archivo):
    """Abre un archivo JSON y lo convierte de vuelta a diccionario."""
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)


def crear_diccionario():
    nombreAlumno = []
    edadAlumno = []
    cedulaAlumno = []

    alumnos = {
        "nombre": nombreAlumno,
        "edad": edadAlumno,
        "cedula": cedulaAlumno
    }

    while True:
        alumnos["nombre"].append(input("Ingrese el nombre del alumno: "))
        alumnos["edad"].append(input("Ingrese la edad del alumno: "))
        alumnos["cedula"].append(input("Ingrese la cédula del alumno: "))

        opcion = input("¿Desea agregar otro alumno? (s/n): ")

        if opcion.lower() != 's':
            break

    guardar_diccionario(alumnos, 'alumnos.json')


crear_diccionario()
print(cargar_diccionario('alumnos.json'))
