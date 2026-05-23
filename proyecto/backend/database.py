import sqlite3
import bcrypt
import seguridad

def getConexion():
    conexion = sqlite3.connect("sistema_cripto.db")
    conexion.row_factory = sqlite3.Row 
    return conexion

def startBD():
    conexion = getConexion()
    cursor = conexion.cursor()
    
    # 1. Tabla de Tutores (Encargados)
    cursor.execute('''
        create table if not exists tutores (
            tutorId integer primary key autoincrement,
            usuario text unique not null,
            contrasenaHash text not null,
            nombreEncriptado blob not null,
            apellidoPaternoEncriptado blob not null,
            apellidoMaternoEncriptado blob,
            edad integer,
            foto text,
            puesto text not null,
            area text not null,
            firmaDigital blob not null
        )
    ''')
    
    # 2. Tabla de Becarios
    cursor.execute('''
        create table if not exists becarios (
            becarioId integer primary key autoincrement,
            usuario text unique not null,
            contrasenaHash text not null,
            nombreEncriptado blob not null,
            apellidoPaternoEncriptado blob not null,
            apellidoMaternoEncriptado blob,
            edad integer,
            foto text,
            carrera text not null,
            institucion text not null,
            semestre integer not null,
            areaAsignada text not null,
            tutorId integer,
            firmaDigital blob not null,
            foreign key (tutorId) references tutores(tutorId)
        )
    ''')
    
    conexion.commit()
    conexion.close()

def insertarTutor(usuario, contrasenaTextoPlano, nombre, apellidoPaterno, apellidoMaterno, edad, foto, puesto, area):
    # 1. Hashing de contraseña (irreversible)
    sal = bcrypt.gensalt()
    contrasenaHash = bcrypt.hashpw(contrasenaTextoPlano.encode('utf-8'), sal).decode('utf-8')
    
    # 2. Cifrado de datos sensibles
    nombreCifrado = seguridad.encriptarDato(nombre)
    paternoCifrado = seguridad.encriptarDato(apellidoPaterno)
    maternoCifrado = seguridad.encriptarDato(apellidoMaterno) if apellidoMaterno else b''
    
    # 3. Firma digital del bloque de identidad para asegurar integridad
    bloqueIdentidad = nombreCifrado + paternoCifrado + maternoCifrado
    firma = seguridad.firmarDato(bloqueIdentidad)
    
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        insert into tutores (usuario, contrasenaHash, nombreEncriptado, apellidoPaternoEncriptado, apellidoMaternoEncriptado, edad, foto, puesto, area, firmaDigital)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (usuario, contrasenaHash, nombreCifrado, paternoCifrado, maternoCifrado if apellidoMaterno else None, edad, foto, puesto, area, firma))
    
    conexion.commit()
    conexion.close()

def getTutoresDescifrados():
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute("select * from tutores")
    tutores = cursor.fetchall()
    conexion.close()
    
    resultado = []
    for tut in tutores:
        nombreCifrado = tut['nombreEncriptado']
        paternoCifrado = tut['apellidoPaternoEncriptado']
        maternoCifrado = tut['apellidoMaternoEncriptado'] if tut['apellidoMaternoEncriptado'] else b''
        firma = tut['firmaDigital']
        
        bloqueIdentidad = nombreCifrado + paternoCifrado + maternoCifrado
        esValida = seguridad.verificarFirma(bloqueIdentidad, firma)
        
        if esValida:
            nombreDescifrado = seguridad.desencriptarDato(nombreCifrado)
            paternoDescifrado = seguridad.desencriptarDato(paternoCifrado)
            maternoDescifrado = seguridad.desencriptarDato(maternoCifrado) if tut['apellidoMaternoEncriptado'] else ""
            estadoFirma = "Válida"
        else:
            nombreDescifrado = "¡ALERTA!"
            paternoDescifrado = "Dato Corrupto"
            maternoDescifrado = ""
            estadoFirma = "Inválida"
            
        resultado.append({
            "tutorId": tut['tutorId'],
            "usuario": tut['usuario'],
            "nombre": nombreDescifrado,
            "apellidoPaterno": paternoDescifrado,
            "apellidoMaterno": maternoDescifrado,
            "edad": tut['edad'],
            "foto": tut['foto'],
            "puesto": tut['puesto'],
            "area": tut['area'],
            "estadoFirma": estadoFirma
        })
    return resultado

def insertarBecario(usuario, contrasenaTextoPlano, nombre, apellidoPaterno, apellidoMaterno, edad, foto, carrera, institucion, semestre, areaAsignada, tutorId):
    sal = bcrypt.gensalt()
    contrasenaHash = bcrypt.hashpw(contrasenaTextoPlano.encode('utf-8'), sal).decode('utf-8')
    
    nombreCifrado = seguridad.encriptarDato(nombre)
    paternoCifrado = seguridad.encriptarDato(apellidoPaterno)
    maternoCifrado = seguridad.encriptarDato(apellidoMaterno) if apellidoMaterno else b''
    
    bloqueIdentidad = nombreCifrado + paternoCifrado + maternoCifrado
    firma = seguridad.firmarDato(bloqueIdentidad)
    
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        insert into becarios (usuario, contrasenaHash, nombreEncriptado, apellidoPaternoEncriptado, apellidoMaternoEncriptado, edad, foto, carrera, institucion, semestre, areaAsignada, tutorId, firmaDigital)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (usuario, contrasenaHash, nombreCifrado, paternoCifrado, maternoCifrado if apellidoMaterno else None, edad, foto, carrera, institucion, semestre, areaAsignada, tutorId, firma))
    
    conexion.commit()
    conexion.close()

def getBecariosDescifrados():
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute("select * from becarios")
    becarios = cursor.fetchall()
    conexion.close()
    
    resultado = []
    for bec in becarios:
        nombreCifrado = bec['nombreEncriptado']
        paternoCifrado = bec['apellidoPaternoEncriptado']
        maternoCifrado = bec['apellidoMaternoEncriptado'] if bec['apellidoMaternoEncriptado'] else b''
        firma = bec['firmaDigital']
        
        bloqueIdentidad = nombreCifrado + paternoCifrado + maternoCifrado
        esValida = seguridad.verificarFirma(bloqueIdentidad, firma)
        
        if esValida:
            nombreDescifrado = seguridad.desencriptarDato(nombreCifrado)
            paternoDescifrado = seguridad.desencriptarDato(paternoCifrado)
            maternoDescifrado = seguridad.desencriptarDato(maternoCifrado) if bec['apellidoMaternoEncriptado'] else ""
            estadoFirma = "Válida"
        else:
            nombreDescifrado = "¡ALERTA!"
            paternoDescifrado = "Dato Corrupto"
            maternoDescifrado = ""
            estadoFirma = "Inválida"
            
        resultado.append({
            "becarioId": bec['becarioId'],
            "usuario": bec['usuario'],
            "nombre": nombreDescifrado,
            "apellidoPaterno": paternoDescifrado,
            "apellidoMaterno": maternoDescifrado,
            "edad": bec['edad'],
            "foto": bec['foto'],
            "carrera": bec['carrera'],
            "institucion": bec['institucion'],
            "semestre": bec['semestre'],
            "areaAsignada": bec['areaAsignada'],
            "tutorId": bec['tutorId'],
            "estadoFirma": estadoFirma
        })
    return resultado

def verificarLogin(usuario, contrasenaTextoPlano):
    conexion = getConexion()
    cursor = conexion.cursor()
    
    # 1. Buscar en la tabla de Tutores
    cursor.execute("select tutorId, contrasenaHash from tutores where usuario = ?", (usuario,))
    tutor = cursor.fetchone()
    
    if tutor:
        # Si existe el tutor, verificamos el hash de su contraseña
        esValida = bcrypt.checkpw(contrasenaTextoPlano.encode('utf-8'), tutor['contrasenaHash'].encode('utf-8'))
        conexion.close()
        if esValida:
            return {"valido": True, "rol": "Tutor", "id": tutor['tutorId']}
        else:
            return {"valido": False, "mensaje": "Contraseña incorrecta"}
            
    # 2. Si no es tutor, buscar en la tabla de Becarios
    cursor.execute("select becarioId, contrasenaHash from becarios where usuario = ?", (usuario,))
    becario = cursor.fetchone()
    
    if becario:
        esValida = bcrypt.checkpw(contrasenaTextoPlano.encode('utf-8'), becario['contrasenaHash'].encode('utf-8'))
        conexion.close()
        if esValida:
            return {"valido": True, "rol": "Becario", "id": becario['becarioId']}
        else:
            return {"valido": False, "mensaje": "Contraseña incorrecta"}
            
    conexion.close()
    return {"valido": False, "mensaje": "El usuario no existe"}