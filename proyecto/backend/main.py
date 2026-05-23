from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import database

app = FastAPI(title="API Proyecto Criptografía Bancaria")

# --- Modelos de Pydantic ---

class TutorNuevo(BaseModel):
    usuario: str
    contrasena: str
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str] = None
    edad: int
    foto: Optional[str] = None
    puesto: str
    area: str

class BecarioNuevo(BaseModel):
    usuario: str
    contrasena: str
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str] = None
    edad: int
    foto: Optional[str] = None
    carrera: str
    institucion: str
    semestre: int
    areaAsignada: str
    tutorId: Optional[int] = None

class CredencialesLogin(BaseModel):
    usuario: str
    contrasena: str

# --- Endpoint de Autenticación ---
@app.post("/login/")
def iniciarSesion(credenciales: CredencialesLogin):
    resultado = database.verificarLogin(credenciales.usuario, credenciales.contrasena)
    
    # Si la contraseña es incorrecta o el usuario no existe, lanzamos un error 401
    if not resultado["valido"]:
        raise HTTPException(status_code=401, detail=resultado["mensaje"])
        
    # Si todo sale bien, devolvemos el rol para que el frontend sepa a qué pantalla redirigir
    return {
        "mensaje": "Inicio de sesión exitoso",
        "rol": resultado["rol"],
        "id": resultado["id"]
    }

# --- Evento de Arranque ---

@app.on_event("startup")
def arrancarSistema():
    print("Inicializando base de datos estructurada...")
    database.startBD()

# --- Endpoints para Tutores ---

@app.post("/tutores/")
def crearTutor(tutor: TutorNuevo):
    database.insertarTutor(
        tutor.usuario, tutor.contrasena, tutor.nombre, tutor.apellidoPaterno,
        tutor.apellidoMaterno, tutor.edad, tutor.foto, tutor.puesto, tutor.area
    )
    return {"mensaje": "Tutor registrado exitosamente con credenciales protegidas"}

@app.get("/tutores/")
def listarTutores():
    return {"tutores": database.getTutoresDescifrados()}

# --- Endpoints para Becarios ---

@app.post("/becarios/")
def crearBecario(becario: BecarioNuevo):
    database.insertarBecario(
        becario.usuario, becario.contrasena, becario.nombre, becario.apellidoPaterno,
        becario.apellidoMaterno, becario.edad, becario.foto, becario.carrera,
        becario.institucion, becario.semestre, becario.areaAsignada, becario.tutorId
    )
    return {"mensaje": "Becario registrado y asignado exitosamente"}

@app.get("/becarios/")
def listarBecarios():
    return {"becarios": database.getBecariosDescifrados()}