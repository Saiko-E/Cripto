from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import database

app = FastAPI(title="API Sistema de Servicio Social")

# --- Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ideal para desarrollo local)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Pydantic ---
class AdministradorNuevo(BaseModel):
    usuario: str
    contrasena: str
    nombre: str
    puesto: str

class EmpresaNueva(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    correo: str
    folioRegistro: str

class AlumnoNuevo(BaseModel):
    matricula: str
    usuario: str
    contrasena: str
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str] = None
    carrera: str
    semestre: int
    empresaId: Optional[int] = None

class CredencialesLogin(BaseModel):
    usuario: str
    contrasena: str

# --- Evento de Arranque ---
@app.on_event("startup")
def arrancarSistema():
    print("Inicializando base de datos del Servicio Social...")
    database.startBD()

# --- Endpoints ---
@app.post("/administradores/")
def crearAdministrador(admin: AdministradorNuevo):
    database.insertarAdministrador(admin.usuario, admin.contrasena, admin.nombre, admin.puesto)
    return {"mensaje": "Administrador registrado exitosamente"}

@app.post("/empresas/")
def crearEmpresa(empresa: EmpresaNueva):
    database.insertarEmpresa(empresa.nombre, empresa.direccion, empresa.telefono, empresa.correo, empresa.folioRegistro)
    return {"mensaje": "Empresa registrada exitosamente en el catálogo"}

@app.post("/alumnos/")
def crearAlumno(alumno: AlumnoNuevo):
    database.insertarAlumno(
        alumno.matricula, alumno.usuario, alumno.contrasena, alumno.nombre, 
        alumno.apellidoPaterno, alumno.apellidoMaterno, alumno.carrera, 
        alumno.semestre, alumno.empresaId
    )
    return {"mensaje": "Alumno registrado exitosamente para Servicio Social"}

@app.post("/login/")
def iniciarSesion(credenciales: CredencialesLogin):
    resultado = database.verificarLogin(credenciales.usuario, credenciales.contrasena)
    if not resultado["valido"]:
        raise HTTPException(status_code=401, detail=resultado["mensaje"])
    return {
        "mensaje": "Inicio de sesión exitoso",
        "rol": resultado["rol"],
        "id": resultado["id"]
    }


# --- Endpoints para Contratos ---

@app.post("/contratos/generar/{alumnoId}")
def generarContrato(alumnoId: int):
    contrato = database.generarYGuardarContrato(alumnoId)
    if not contrato:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron datos del alumno o no tiene una empresa asignada todavía."
        )
    return {
        "mensaje": "Contrato generado y firmado con criptografía post-cuántica exitosamente",
        "contrato": contrato
    }

@app.get("/contratos/alumno/{alumnoId}")
def obtenerContratoAlumno(alumnoId: int):
    contrato = database.consultarContratoPorAlumno(alumnoId)
    if not contrato:
        raise HTTPException(status_code=404, detail="No se encontró ningún contrato para este alumno.")
    return {"contrato": contrato}


# --- Endpoints GET ---

@app.get("/empresas/")
def listarEmpresas():
    return {"empresas": database.listarEmpresas()}


@app.get("/alumnos/")
def listarAlumnos():
    return {"alumnos": database.listarAlumnos()}


@app.get("/alumnos/{alumnoId}")
def obtenerAlumno(alumnoId: int):
    alumno = database.obtenerAlumno(alumnoId)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    return {"alumno": alumno}


@app.delete("/alumnos/{alumnoId}")
def darDeBajaAlumno(alumnoId: int):
    eliminado = database.darDeBajaAlumno(alumnoId)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    return {"mensaje": "Alumno dado de baja exitosamente"}