import sqlite3
from cryptography.fernet import fernet

# generamos una clave de encriptación
clave_secreta = fernet.generate_key()
cifrador = fernet(clave_secreta)

def getConexion():
    # conecta al archivo o lo crea si no existe
    conexion = sqlite3.connect("sistema_cripto.db")
    conexion.row_factory = sqlite3.row 
    return conexion

def startBD():
    conexion = getConexion()
    cursor = conexion.cursor()
    
    # tabla empleados
    cursor.execute('''
        create table if not exists empleados (
            empleadoId integer primary key autoincrement,
            nombreEncriptado text not null,
            departamento text not null
        )
    ''')
    
    # tabla becarios
    cursor.execute('''
        create table if not exists becarios (
            becarioId integer primary key autoincrement,
            nombreEncriptado text not null,
            universidad text not null,
            empleadoAsignadoId integer,
            foreign key (empleadoAsignadoId) references empleados(empleadoId)
        )
    ''')
    
    conexion.commit()
    conexion.close()

def insertarEmpleado(nombre_real, departamento):
    # encriptamos el nombre
    nombreCifrado = cifrador.encrypt(nombre_real.encode('utf-8'))
    
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        insert into empleados (nombreEncriptado, departamento)
        values (?, ?)
    ''', (nombreCifrado, departamento))
    
    conexion.commit()
    conexion.close()

def getEmpleadosDescifrados():
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute("select * from empleados")
    empleados = cursor.fetchall()
    conexion.close()
    
    resultado = []
    for emp in empleados:
        # desciframos el nombre al momento de leerlo
        nombre_descifrado = cifrador.decrypt(emp['nombreEncriptado']).decode('utf-8')
        resultado.append({
            "id": emp['empleadoId'],
            "nombre": nombre_descifrado,
            "departamento": emp['departamento']
        })
    return resultado