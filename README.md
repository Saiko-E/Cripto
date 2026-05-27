# Portal Seguro para la Gestión de Servicio Social (UNAM - FI)

Este proyecto consiste en un prototipo funcional de un portal web enfocado en la gestión y registro de alumnos para una feria de Servicio Social, emulando los sistemas institucionales de la Facultad de Ingeniería. La plataforma implementa un modelo robusto de seguridad criptográfica híbrida para garantizar la confidencialidad de los datos personales, el almacenamiento seguro de credenciales y el no repudio de los documentos oficiales generados mediante tecnologías post-cuánticas.

## Características y Tecnologías

- **Frontend:** React + Vite (Estructura base preparada para maquetación de vistas por roles).
- **Backend:** Python + FastAPI (Servidor asíncrono de alto rendimiento).
- **Base de Datos:** SQLite (`sistema_cripto.db`) con restricciones de integridad y unicidad.
- **Capa Criptográfica:**
  - **Hashing de Contraseñas:** `bcrypt` (Salted Hashing intencionalmente lento contra fuerza bruta).
  - **Confidencialidad:** `Fernet` (Cifrado simétrico AES-128-CBC + HMAC) para datos personales en la base de datos.
  - **Seguridad en QR:** Cifrado simétrico y codificación Base64 de la matrícula universitaria dentro de la matriz del QR.
  - **Resiliencia Post-Cuántica:** **CRYSTALS-Dilithium2** (Estándar FIPS 204) para la firma digital de Contratos de Servicio Social y validación de bloques de identidad.

---

## Prerrequisitos

Antes de iniciar, asegúrate de tener instalado en tu sistema:
- [Python 3.10+](https://www.python.org/)
- [Node.js (LTS)](https://nodejs.org/) (incluye el gestor de paquetes `npm`)

---

## Instrucciones de Despliegue

La aplicación requiere la ejecución simultánea de dos servidores locales (Backend y Frontend). Abre dos terminales independientes en tu sistema y sigue estos pasos:

### 1. Configuración del Backend (Terminal 1)

Navega a la carpeta del backend, inicializa el entorno virtual de Python e instala las dependencias criptográficas y del servidor:

```bash
# 1. Ingresar al directorio del backend
cd backend

# 2. Crear el entorno virtual
python -m venv venv

# 3. Activar el entorno virtual (En Windows)
.\venv\Scripts\activate

# 4. Instalar las dependencias del sistema
pip install -r dependencias.txt

# 5. Levantar el servidor de FastAPI
python main.py
```
*El backend comenzará a correr localmente en la dirección:* `http://127.0.0.1:8000`

### 2. Configuración del Frontend (Terminal 2)

Navega a la carpeta del frontend, descarga los módulos de node e inicia el entorno de desarrollo de Vite:

```bash
# 1. Ingresar al directorio del frontend
cd ../frontend

# 2. Instalar las dependencias de React
npm install

# 3. Levantar el servidor de desarrollo de Vite
npm run dev
```
*El frontend estará disponible en el navegador web a través de la ruta:* `http://localhost:5173`

---

## Guía de Pruebas Criptográficas (API Interactiva)

Dado que el motor criptográfico se encuentra completamente operativo en el backend, la forma más eficiente de validar los flujos de seguridad es utilizando la interfaz interactiva automatizada de FastAPI (**Swagger UI**).

1. Abre tu navegador e ingresa a: `http://127.0.0.1:8000/docs`
2. Para probar cada endpoint, haz clic sobre el bloque, presiona el botón **"Try it out"**, edita el cuerpo del JSON si corresponde y presiona **"Execute"**.

### Flujo de Prueba Recomendado:

#### Paso 1: Registrar una Empresa/Institución Receptora
Busca la ruta `POST /empresas/` y ejecuta la petición con el siguiente JSON. El sistema cifrará simétricamente la dirección y datos de contacto antes de almacenarlos en disco.
```json
{
  "nombre": "Ctrl+Alt+Del Team",
  "direccion": "Ciudad Universitaria, CDMX",
  "telefono": "5512345678",
  "correo": "contacto@ctrlaltdel.com",
  "folioRegistro": "FOLIO-001"
}
```
*Nota: El campo `folioRegistro` cuenta con una restricción de unicidad (`UNIQUE`). Ejecutar la petición con el mismo folio provocará un error de integridad (500), protegiendo el sistema contra registros duplicados.*

#### Paso 2: Registrar un Alumno (Vinculado a la Empresa)
Busca la ruta `POST /alumnos/` y envía los datos del estudiante de prueba. El sistema generará el hash de la contraseña con `bcrypt`, encriptará la matrícula para el código QR y protegerá los datos de identidad.
```json
{
  "matricula": "312345678",
  "usuario": "sebjimort",
  "contrasena": "mi_contrasena_segura",
  "nombre": "Sebastián",
  "apellidoPaterno": "Jiménez",
  "apellidoMaterno": "Ortiz",
  "carrera": "Ingeniería en Computación",
  "semestre": 8,
  "empresaId": 1
}
```

#### Paso 3: Generación de Contrato y Firma Post-Cuántica
Busca la ruta de generación de contratos `POST /contratos/generar/{alumnoId}`. 
- En el parámetro de la URL `alumnoId`, ingresa el identificador numérico del alumno que acabas de registrar (ej. `1` o `2`).
- Presiona **Execute**.

**Resultado Criptográfico:** El servidor extraerá los datos encriptados de la base de datos, los descifrará dinámicamente en memoria RAM para redactar el contrato y utilizará el algoritmo matemático **CRYSTALS-Dilithium2** junto con la clave `privada_pqc.bin` para estampar un sello digital en formato hexadecimal en el campo `"firma"`. Este sello garantiza la autenticidad e integridad inalterable del documento frente a futuros vectores de ataque cuánticos.