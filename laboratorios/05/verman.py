import random
import string

def generarString(n):
    caracteres = string.ascii_letters + string.digits
    resultado = ''.join(random.choice(caracteres) for _ in range(n))
    return resultado

def vernam(texto, clave):
    if len(clave) < len(texto):
        raise ValueError("ERROR: Clave mas corta que el texto")
    resultado =""
    for letraTexto, letraClave in zip(texto, clave):
        resultado += chr(ord(letraTexto)^ord(letraClave))
    return resultado


if __name__ == "__main__":
    mensaje = "Hola"
    clave   = generarString(len(mensaje))
    
    textoCifrado = vernam (mensaje, clave)
    textoDescifrado = vernam(textoCifrado, clave)

    clave = ""
    print(f"Mensaje original: {mensaje}")
    print(f"Texto cifrado: {repr(textoCifrado)}")
    print(f"Texto descifrado: {textoDescifrado}")
    print(clave)
