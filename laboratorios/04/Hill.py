# Función matemática para encontrar el inverso modular
def mod_inverso(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def cifrado_hill_2x2(texto, matriz_clave, encriptar=True):
    # La matriz clave es 2x2: [[a, b], [c, d]]
    a, b = matriz_clave[0][0], matriz_clave[0][1]
    c, d = matriz_clave[1][0], matriz_clave[1][1]
    
    # 1. Calculamos el determinante: (a*d - b*c) mod 26
    det = (a * d - b * c) % 26
    
    # Verificamos si la matriz es válida para cifrar
    inv_det = mod_inverso(det, 26)
    if inv_det is None:
        return "Error: La matriz clave no tiene inversa modular (su determinante no es coprimo con 26)."

    # 2. Si estamos desencriptando, necesitamos la Matriz Inversa
    if not encriptar:
        # Fórmula de la matriz inversa 2x2 módulo 26:
        # inv_det * [[d, -b], [-c, a]] mod 26
        a_inv = (inv_det * d) % 26
        b_inv = (inv_det * -b) % 26
        c_inv = (inv_det * -c) % 26
        d_inv = (inv_det * a) % 26
        
        # Reemplazamos las variables de la matriz para usar la inversa
        a, b, c, d = a_inv, b_inv, c_inv, d_inv

    # 3. Limpiamos el texto y lo ajustamos para que sea par
    texto = texto.replace(" ", "").upper()
    if len(texto) % 2 != 0:
        texto += "X" # Agregamos una letra de relleno si es impar

    resultado = ""

    # 4. Procesamos el texto de 2 en 2 letras
    for i in range(0, len(texto), 2):
        # Convertimos letras a números (A=0, ..., Z=25)
        p1 = ord(texto[i]) - 65
        p2 = ord(texto[i+1]) - 65
        
        # Multiplicación de la matriz: [C] = [K] * [P]
        c1 = (a * p1 + b * p2) % 26
        c2 = (c * p1 + d * p2) % 26
        
        # Volvemos a convertir a letras
        resultado += chr(c1 + 65)
        resultado += chr(c2 + 65)

    return resultado

# --- Ejemplo de uso ---
# Usaremos la matriz clave:
# [ 3  3 ]
# [ 2  5 ]
clave_2x2 = [[3, 3], [2, 5]]
mensaje = "HOLA MUNDO"

print(f"Mensaje original: {mensaje}")

cifrado = cifrado_hill_2x2(mensaje, clave_2x2)
print(f"Hill Cifrado:     {cifrado}")

descifrado = cifrado_hill_2x2(cifrado, clave_2x2, encriptar=False)
print(f"Hill Descifrado:  {descifrado}")