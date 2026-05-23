import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# cifrado simetrico (Fernet) para proteger los datos

def obtenerLlaveFernet():
    # Si no existe la llave, la crea y la guarda
    if not os.path.exists("secreto.key"):
        llave = Fernet.generate_key()
        with open("secreto.key", "wb") as archivoLlave:
            archivoLlave.write(llave)
    
    with open("secreto.key", "rb") as archivoLlave:
        return archivoLlave.read()

# Inicializacion del cifrado
cifrador = Fernet(obtenerLlaveFernet())

def encriptarDato(texto: str) -> bytes:
    """Recibe un texto normal y devuelve los bytes encriptados."""
    return cifrador.encrypt(texto.encode('utf-8'))

def desencriptarDato(textoCifrado: bytes) -> str:
    """Recibe bytes encriptados y devuelve el texto normal."""
    return cifrador.decrypt(textoCifrado).decode('utf-8')


# Firma digital con RSA

def inicializarLlavesRsa():
    """Genera y guarda el par de llaves RSA si no existen."""
    if not os.path.exists("privada.pem") or not os.path.exists("publica.pem"):
        print("Generando nuevo par de llaves RSA...")
        llavePrivada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        llavePublica = llavePrivada.public_key()
        
        # Guardar Llave Privada
        with open("privada.pem", "wb") as f:
            f.write(llavePrivada.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            
        # Guardar Llave Pública
        with open("publica.pem", "wb") as f:
            f.write(llavePublica.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

def cargarLlavePrivada():
    with open("privada.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def cargarLlavePublica():
    with open("publica.pem", "rb") as f:
        return serialization.load_pem_public_key(f.read())

def firmarDato(datoEncriptado: bytes) -> bytes:
    """Firma el dato usando la Llave Privada del Tutor/Sistema."""
    llavePrivada = cargarLlavePrivada()
    firma = llavePrivada.sign(
        datoEncriptado,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return firma

def verificarFirma(datoEncriptado: bytes, firma: bytes) -> bool:
    """Verifica si la firma coincide con el dato usando la Llave Pública."""
    llavePublica = cargarLlavePublica()
    try:
        llavePublica.verify(
            firma,
            datoEncriptado,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True # La firma es válida
    except Exception:
        return False # La firma no coincide (dato alterado)

# Ejecutamos la verificación de llaves RSA al importar el archivo
inicializarLlavesRsa()