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
    
    # 1. Tabla Administradores (Universidad)
    cursor.execute('''
        create table if not exists administradores (
            adminId integer primary key autoincrement,
            usuario text unique not null,
            contrasenaHash text not null,
            nombreEncriptado blob not null,
            puesto text not null,
            firmaDigital blob not null
        )
    ''')

    # 2. Tabla Empresas (Catálogo de S.S.)
    cursor.execute('''
        create table if not exists empresas (
            empresaId integer primary key autoincrement,
            nombre blob not null,
            direccion blob not null,
            telefono blob not null,
            correo blob not null,
            folioRegistro text unique not null,
            firmaDigital blob not null
        )
    ''')
    
    # 3. Tabla Alumnos (Servicio Social)
    # 3. Tabla Alumnos (Servicio Social)
    # 3. Tabla Alumnos (Servicio Social)
    cursor.execute('''
        create table if not exists alumnos (
            alumnoId integer primary key autoincrement,
            matricula text unique not null,
            usuario text unique not null,
            contrasenaHash text not null,
            nombreEncriptado blob not null,
            apellidoPaternoEncriptado blob not null,
            apellidoMaternoEncriptado blob,
            carrera text not null,
            semestre integer not null,
            empresaId integer,
            qrCode text not null,
            firmaDigital blob not null,
            foreign key (empresaId) references empresas(empresaId)
        )
    ''')
    # 4. Tabla de Contratos de Servicio Social
    cursor.execute('''
        create table if not exists contratos (
            contratoId integer primary key autoincrement,
            alumnoId integer unique not null,
            empresaId integer not null,
            contenido text not null,
            firmaDigital blob not null,
            foreign key (alumnoId) references alumnos(alumnoId),
            foreign key (empresaId) references empresas(empresaId)
        )
    ''')
    
    conexion.commit()
    conexion.close()

# --- Funciones Administradores ---
def insertarAdministrador(usuario, contrasenaTextoPlano, nombre, puesto):
    sal = bcrypt.gensalt()
    contrasenaHash = bcrypt.hashpw(contrasenaTextoPlano.encode('utf-8'), sal).decode('utf-8')
    
    nombreCifrado = seguridad.encriptarDato(nombre)
    firma = seguridad.firmarDato(nombreCifrado)
    
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        insert into administradores (usuario, contrasenaHash, nombreEncriptado, puesto, firmaDigital)
        values (?, ?, ?, ?, ?)
    ''', (usuario, contrasenaHash, nombreCifrado, puesto, firma))
    conexion.commit()
    conexion.close()

# --- Funciones Empresas ---
def insertarEmpresa(nombre, direccion, telefono, correo, folioRegistro):
    nombreCifrado = seguridad.encriptarDato(nombre)
    direccionCifrado = seguridad.encriptarDato(direccion)
    telefonoCifrado = seguridad.encriptarDato(telefono)
    correoCifrado = seguridad.encriptarDato(correo)
    
    bloqueIntegridad = nombreCifrado + telefonoCifrado + correoCifrado
    firma = seguridad.firmarDato(bloqueIntegridad)
    
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        insert into empresas (nombre, direccion, telefono, correo, folioRegistro, firmaDigital)
        values (?, ?, ?, ?, ?, ?)
    ''', (nombreCifrado, direccionCifrado, telefonoCifrado, correoCifrado, folioRegistro, firma))
    conexion.commit()
    conexion.close()

# --- Funciones Alumnos ---
def insertarAlumno(matricula, usuario, contrasenaTextoPlano, nombre, apellidoPaterno, apellidoMaterno, carrera, semestre, empresaId):
    sal = bcrypt.gensalt()
    contrasenaHash = bcrypt.hashpw(contrasenaTextoPlano.encode('utf-8'), sal).decode('utf-8')
    
    nombreCifrado = seguridad.encriptarDato(nombre)
    paternoCifrado = seguridad.encriptarDato(apellidoPaterno)
    maternoCifrado = seguridad.encriptarDato(apellidoMaterno) if apellidoMaterno else b''
    
    # ¡Aquí generamos el QR Cifrado!
    qrCodeBase64 = seguridad.generarQrCifrado(matricula)
    
    bloqueIdentidad = nombreCifrado + paternoCifrado + maternoCifrado
    firma = seguridad.firmarDato(bloqueIdentidad)
    
    conexion = getConexion()
    cursor = conexion.cursor()
    
    # Actualizamos el INSERT para incluir qrCode
    cursor.execute('''
        insert into alumnos (matricula, usuario, contrasenaHash, nombreEncriptado, apellidoPaternoEncriptado, apellidoMaternoEncriptado, carrera, semestre, empresaId, qrCode, firmaDigital)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (matricula, usuario, contrasenaHash, nombreCifrado, paternoCifrado, maternoCifrado if apellidoMaterno else None, carrera, semestre, empresaId, qrCodeBase64, firma))
    
    conexion.commit()
    conexion.close()

# --- Lógica de Login Adaptada ---
def verificarLogin(usuario, contrasenaTextoPlano):
    conexion = getConexion()
    cursor = conexion.cursor()
    
    # Buscar Administrador
    cursor.execute("select adminId, contrasenaHash from administradores where usuario = ?", (usuario,))
    admin = cursor.fetchone()
    if admin and bcrypt.checkpw(contrasenaTextoPlano.encode('utf-8'), admin['contrasenaHash'].encode('utf-8')):
        conexion.close()
        return {"valido": True, "rol": "Administrador", "id": admin['adminId']}
            
    # Buscar Alumno
    cursor.execute("select alumnoId, contrasenaHash from alumnos where usuario = ?", (usuario,))
    alumno = cursor.fetchone()
    if alumno and bcrypt.checkpw(contrasenaTextoPlano.encode('utf-8'), alumno['contrasenaHash'].encode('utf-8')):
        conexion.close()
        return {"valido": True, "rol": "Alumno", "id": alumno['alumnoId']}
            
    conexion.close()
    return {"valido": False, "mensaje": "Credenciales inválidas"}


def obtenerDatosParaContrato(alumnoId):
    """Une las tablas de alumnos y empresas para extraer la información necesaria."""
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        select a.nombreEncriptado as alNombre, a.apellidoPaternoEncriptado as alPaterno, a.apellidoMaternoEncriptado as alMaterno, a.matricula, a.carrera,
               e.empresaId, e.nombre as empNombre, e.folioRegistro
        from alumnos a
        join empresas e on a.empresaId = e.empresaId
        where a.alumnoId = ?
    ''', (alumnoId,))
    datos = cursor.fetchone()
    conexion.close()
    return datos

def generarYGuardarContrato(alumnoId):
    datos = obtenerDatosParaContrato(alumnoId)
    if not datos:
        return None
    
    # Desciframos temporalmente los datos sensibles para el cuerpo del texto
    nombreAl = seguridad.desencriptarDato(datos['alNombre'])
    paternoAl = seguridad.desencriptarDato(datos['alPaterno'])
    maternoAl = seguridad.desencriptarDato(datos['alMaterno']) if datos['alMaterno'] else ""
    nombreEmp = seguridad.desencriptarDato(datos['empNombre'])
    
    nombreCompleto = f"{nombreAl} {paternoAl} {maternoAl}".strip()
    
    # Estructuramos el cuerpo formal del contrato de Servicio Social
    contenidoContrato = (
        f"CONTRATO DE FORMALIZACIÓN DE SERVICIO SOCIAL\n\n"
        f"Por medio del presente documento, se hace constar que el alumno(a) {nombreCompleto} "
        f"con matrícula {datos['matricula']}, perteneciente a la carrera de {datos['carrera']}, "
        f"ha sido asignado(a) formalmente para realizar sus actividades de Servicio Social en la "
        f"institución/empresa {nombreEmp}, bajo el número de folio de registro oficial {datos['folioRegistro']}.\n\n"
        f"Ambas partes se comprometen a respetar los lineamientos institucionales establecidos."
    )
    
    # Blindamos el texto completo usando la Firma Post-Cuántica (Dilithium)
    firmaPQC = seguridad.firmarDato(contenidoContrato.encode('utf-8'))
    
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        insert or replace into contratos (alumnoId, empresaId, contenido, firmaDigital)
        values (?, ?, ?, ?)
    ''', (alumnoId, datos['empresaId'], contenidoContrato, firmaPQC))
    conexion.commit()
    conexion.close()
    
    return {
        "contenido": contenidoContrato,
        "firma": firmaPQC.hex()  # Lo pasamos a hexadecimal para que sea legible en el JSON de la API
    }

def consultarContratoPorAlumno(alumnoId):
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute("select * from contratos where alumnoId = ?", (alumnoId,))
    contrato = cursor.fetchone()
    conexion.close()
    
    if not contrato:
        return None
        
    # Verificamos la integridad matemática del contrato usando la llave pública cuántica
    esValido = seguridad.verificarFirma(contrato['contenido'].encode('utf-8'), contrato['firmaDigital'])
    
    return {
        "contratoId": contrato['contratoId'],
        "contenido": contrato['contenido'],
        "estadoFirma": "Válida (Protección Post-Cuántica)" if esValido else "¡ALERTA! El contrato ha sido manipulado",
        "firmaDigital": contrato['firmaDigital'].hex()
    }


# --- Funciones GET ---

def listarEmpresas():
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute("select empresaId, nombre, direccion, telefono, correo, folioRegistro from empresas")
    filas = cursor.fetchall()
    conexion.close()
    resultado = []
    for f in filas:
        resultado.append({
            "empresaId": f["empresaId"],
            "nombre": seguridad.desencriptarDato(f["nombre"]),
            "direccion": seguridad.desencriptarDato(f["direccion"]),
            "telefono": seguridad.desencriptarDato(f["telefono"]),
            "correo": seguridad.desencriptarDato(f["correo"]),
            "folioRegistro": f["folioRegistro"]
        })
    return resultado


def listarAlumnos():
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        select a.alumnoId, a.matricula, a.nombreEncriptado, a.apellidoPaternoEncriptado,
               a.apellidoMaternoEncriptado, a.carrera, a.semestre, a.qrCode,
               e.nombre as empNombre
        from alumnos a
        left join empresas e on a.empresaId = e.empresaId
    ''')
    filas = cursor.fetchall()
    conexion.close()
    resultado = []
    for f in filas:
        resultado.append({
            "alumnoId": f["alumnoId"],
            "matricula": f["matricula"],
            "nombre": seguridad.desencriptarDato(f["nombreEncriptado"]),
            "apellidoPaterno": seguridad.desencriptarDato(f["apellidoPaternoEncriptado"]),
            "apellidoMaterno": seguridad.desencriptarDato(f["apellidoMaternoEncriptado"]) if f["apellidoMaternoEncriptado"] else "",
            "carrera": f["carrera"],
            "semestre": f["semestre"],
            "qrCode": f["qrCode"],
            "empresa": seguridad.desencriptarDato(f["empNombre"]) if f["empNombre"] else None
        })
    return resultado


def obtenerAlumno(alumnoId):
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute('''
        select a.alumnoId, a.matricula, a.usuario, a.nombreEncriptado, a.apellidoPaternoEncriptado,
               a.apellidoMaternoEncriptado, a.carrera, a.semestre, a.qrCode,
               e.empresaId, e.nombre as empNombre, e.folioRegistro
        from alumnos a
        left join empresas e on a.empresaId = e.empresaId
        where a.alumnoId = ?
    ''', (alumnoId,))
    f = cursor.fetchone()
    conexion.close()
    if not f:
        return None
    return {
        "alumnoId": f["alumnoId"],
        "matricula": f["matricula"],
        "usuario": f["usuario"],
        "nombre": seguridad.desencriptarDato(f["nombreEncriptado"]),
        "apellidoPaterno": seguridad.desencriptarDato(f["apellidoPaternoEncriptado"]),
        "apellidoMaterno": seguridad.desencriptarDato(f["apellidoMaternoEncriptado"]) if f["apellidoMaternoEncriptado"] else "",
        "carrera": f["carrera"],
        "semestre": f["semestre"],
        "qrCode": f["qrCode"],
        "empresaId": f["empresaId"],
        "empresa": seguridad.desencriptarDato(f["empNombre"]) if f["empNombre"] else None,
        "folioRegistro": f["folioRegistro"]
    }


def darDeBajaAlumno(alumnoId):
    conexion = getConexion()
    cursor = conexion.cursor()
    cursor.execute("delete from contratos where alumnoId = ?", (alumnoId,))
    cursor.execute("delete from alumnos where alumnoId = ?", (alumnoId,))
    eliminados = cursor.rowcount
    conexion.commit()
    conexion.close()
    return eliminados > 0