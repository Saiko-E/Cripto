import sqlite3
import proyecto.backend.seguridad as seguridad  # Importamos las funciones de tu nuevo archivo

def getConexion():
    # conecta al archivo o lo crea si no existe
    conexion = sqlite3.connect("sistema_cripto.db")
    conexion.row_factory = sqlite3.Row 
    return conexion

def startBD():
    conexion = getConexion()
    cursor = conexion.cursor()
    
    # tabla empleados (agregamos firmaDigital tipo blob)
    cursor.execute('''
        create table if not exists empleados (
            empleadoId integer primary key autoincrement,
            nombreEncriptado blob not null,
            firmaDigital blob not null,
            departamento text not null
        )
    ''')
    
    # tabla becarios (agregamos firmaDigital tipo blob)
    cursor.execute('''
        create table if not exists becarios (
            becarioId integer primary key autoincrement,
            nombreEncriptado blob not null,
            firmaDigital blob not null,
            universidad text not null,
            empleadoAsignadoId integer,
            foreign key (empleadoAsignadoId) references empleados(empleadoId)
        )
    ''')
    
    conexion.commit()
    conexion.close()

def insertarEmpleado(nombreReal, departamento):
    # 1. Encriptamos el nombre
    nombreCifrado = seguridad.encriptarDato(nombreReal)
    
    # 2. Firmamos el dato ya encriptado
    firma = seguridad.firmarDato(nombreCifrado)
    
    # 3. Guardamos todo en la base
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        insert into empleados (nombreEncriptado, firmaDigital, departamento)
        values (?, ?, ?)
    ''', (nombreCifrado, firma, departamento))
    
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
        nombreCifrado = emp['nombreEncriptado']
        firma = emp['firmaDigital']
        
        # Verificamos la autenticidad antes de descifrar
        esValida = seguridad.verificarFirma(nombreCifrado, firma)
        
        if esValida:
            nombreDescifrado = seguridad.desencriptarDato(nombreCifrado)
            estadoFirma = "Válida"
        else:
            nombreDescifrado = "¡ALERTA! Dato corrupto o alterado"
            estadoFirma = "Inválida"

        resultado.append({
            "id": emp['empleadoId'],
            "nombre": nombreDescifrado,
            "departamento": emp['departamento'],
            "estadoFirma": estadoFirma
        })
    return resultado