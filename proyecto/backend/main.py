from fastapi import FastAPI
from pydantic import BaseModel
import database

# Inicializamos FastAPI
app = FastAPI(title="API Proyecto Criptografía")

# Modelo de Pydantic para recibir los datos del Frontend
# (Mantenemos los atributos en minúsculas para facilitar el mapeo del JSON)
class EmpleadoNuevo(BaseModel):
    nombre: str
    departamento: str

# Evento que se ejecuta al arrancar el servidor de FastAPI
@app.on_event("startup")
def arrancarSistema():
    print("Inicializando base de datos con firmas digitales...")
    database.startBD()

# --- Endpoints ---

@app.post("/empleados/")
def crearEmpleado(empleado: EmpleadoNuevo):
    # Llama a la función que encripta, firma y guarda en SQLite
    database.insertarEmpleado(empleado.nombre, empleado.departamento)
    return {"mensaje": "Empleado registrado, encriptado y firmado con éxito"}

@app.get("/empleados/")
def listarEmpleados():
    # Devuelve la lista descifrada incluyendo el estado de la firma digital
    listaEmpleados = database.getEmpleadosDescifrados()
    return {"empleados": listaEmpleados}