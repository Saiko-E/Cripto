from fastapi import FastAPI
from pydantic import BaseModel
import database

# Inicializamos FastAPI
app = FastAPI(title="API Proyecto Criptografía")

# Modelo
class EmpleadoNuevo(BaseModel):
    nombre: str
    departamento: str

# Evento que se ejecuta al arrancar el servidor
@app.on_event("startup")
def arrancar_sistema():
    print("Inicializando base de datos...")
    database.startBD()

# ---Enspoints ) ---

@app.post("/empleados/")
def crear_empleado(empleado: EmpleadoNuevo):
    database.insertarEmpleado(empleado.nombre, empleado.departamento)
    return {"mensaje": "Empleado registrado y encriptado con éxito"}

@app.get("/empleados/")
def listar_empleados():
    # Devuelve la lista ya descifrada para que el frontend la muestre
    lista = database.getEmpleadosDescifrados()
    return {"empleados": lista}