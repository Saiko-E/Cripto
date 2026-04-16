# Programa para encontrar los primeros n inversos de un número a módulo m

def euclides_extendido(a, b):
    """
    Retorna (mcd, x, y) tal que a*x + b*y = mcd
    """
    if a == 0:
        return b, 0, 1
    else:
        mcd, x1, y1 = euclides_extendido(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return mcd, x, y

def encontrar_n_inversos(a, m, n):
    mcd, x, y = euclides_extendido(a, m)
    
    if mcd != 1:
        return f"No existe inverso para {a} mod {m} porque no son coprimos."
    
    # El inverso base (el menor positivo)
    inverso_base = x % m
    
    # Generar n términos de la clase de congruencia
    inversos = []
    for i in range(n):
        inversos.append(inverso_base + (i * m))
        
    return inversos

# --- Ejemplo de uso ---
numero = 3
modulo = 7
cantidad = 5

resultado = encontrar_n_inversos(numero, modulo, cantidad)

if isinstance(resultado, list):
    print(f"Los primeros {cantidad} inversos de {numero} mod {modulo} son:")
    print(resultado)
else:
    print(resultado)