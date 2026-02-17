def cesarCode(texto, desplazamiento):
    resultado = ''
    for e in (texto):
        if (e.isalpha()):
            base = ord('A')if e.isupper() else ord('a')
            resultado += chr((ord(e)-base + desplazamiento) % 26 + base)
        else:
            resultado += e

    return resultado
        
def descifrado(texto, desplazamiento):
    return cesarCode(texto, -desplazamiento)


def main():
    a= cesarCode('aBCd3.,',29)
    print(a)
    print(descifrado(a,29))

main()