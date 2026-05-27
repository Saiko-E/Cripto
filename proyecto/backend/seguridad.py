import os
import base64
from io import BytesIO
import qrcode
from cryptography.fernet import Fernet
from dilithium_py.dilithium import Dilithium2

# ==========================================
# 1. LÓGICA DE CIFRADO SIMÉTRICO (FERNET)
# ==========================================

def obtenerLlaveFernet():
    if not os.path.exists("secreto.key"):
        llave = Fernet.generate_key()
        with open("secreto.key", "wb") as archivoLlave:
            archivoLlave.write(llave)
    with open("secreto.key", "rb") as archivoLlave:
        return archivoLlave.read()

cifrador = Fernet(obtenerLlaveFernet())

def encriptarDato(texto: str) -> bytes:
    return cifrador.encrypt(texto.encode('utf-8'))

def desencriptarDato(textoCifrado: bytes) -> str:
    return cifrador.decrypt(textoCifrado).decode('utf-8')

# ==========================================
# 2. LÓGICA DE FIRMA POST-CUÁNTICA (DILITHIUM)
# ==========================================

def inicializarLlavesPQC():
    """Genera y guarda el par de llaves Crystals-Dilithium si no existen."""
    # Guardamos en formato .bin porque Dilithium devuelve arreglos de bytes puros
    if not os.path.exists("privada_pqc.bin") or not os.path.exists("publica_pqc.bin"):
        print("Generando nuevo par de llaves Post-Cuánticas (Dilithium2)...")
        
        # Generación nativa de llaves post-cuánticas
        llavePublica, llavePrivada = Dilithium2.keygen()
        
        with open("privada_pqc.bin", "wb") as f:
            f.write(llavePrivada)
            
        with open("publica_pqc.bin", "wb") as f:
            f.write(llavePublica)

def cargarLlavePrivadaPQC() -> bytes:
    with open("privada_pqc.bin", "rb") as f:
        return f.read()

def cargarLlavePublicaPQC() -> bytes:
    with open("publica_pqc.bin", "rb") as f:
        return f.read()

def firmarDato(datoEncriptado: bytes) -> bytes:
    """Firma el dato usando la Llave Privada Post-Cuántica."""
    llavePrivada = cargarLlavePrivadaPQC()
    firma = Dilithium2.sign(llavePrivada, datoEncriptado)
    return firma

def verificarFirma(datoEncriptado: bytes, firma: bytes) -> bool:
    """Verifica si la firma coincide usando la Llave Pública Post-Cuántica."""
    llavePublica = cargarLlavePublicaPQC()
    try:
        # verify() devuelve True si es auténtico, o False si fue alterado
        esValida = Dilithium2.verify(llavePublica, datoEncriptado, firma)
        return esValida
    except Exception:
        return False

# Ejecutamos la verificación al arrancar
inicializarLlavesPQC()

# ==========================================
# 3. LÓGICA DE CÓDIGOS QR
# ==========================================

def generarQrCifrado(matricula: str) -> str:
    # 1. Encriptamos la matrícula
    matriculaCifradaBytes = encriptarDato(matricula)
    matriculaCifradaTexto = base64.b64encode(matriculaCifradaBytes).decode('utf-8')
    
    # 2. Generamos el QR
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(matriculaCifradaTexto)
    qr.make(fit=True)
    
    imagenQr = qr.make_image(fill_color="black", back_color="white")
    
    # 3. Lo empaquetamos en Base64 para la base de datos
    buffer = BytesIO()
    imagenQr.save(buffer, format="PNG")
    imagenBase64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return f"data:image/png;base64,{imagenBase64}"