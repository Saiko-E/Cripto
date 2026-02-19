#include <iostream>
#include <string>
#include <vector>

using namespace std;

string cifradoVigenere(string text, string key) {

    if(key.empty()) return text;

    string result = "";
    int keyIndex = 0;
    
    for(char c : text) {
        if(isalpha(c)) {
            char base = isupper(c) ? 'A' : 'a';
            char keyChar = toupper(key[keyIndex % key.length()]);
            int shift = keyChar - 'A';
            result += (c - base + shift) % 26 + base;
            keyIndex++;
        } else {
            result += c;
        }
    }
    
    return result;
}

string descifradoVigenere(string text, string key) {

    if(key.empty()) return text;

    string result = "";
    int keyIndex = 0;
    
    for(char c : text) {
        if(isalpha(c)) {
            char base = isupper(c) ? 'A' : 'a';
            char keyChar = toupper(key[keyIndex % key.length()]);
            int shift = keyChar - 'A';
            result += (c - base - shift + 26) % 26 + base;
            keyIndex++;
        } else {
            result += c;
        }
    }
    
    return result;
}

void verificar(string nombrePrueba, string original, string procesado, string esperado) {
    cout << "[" << nombrePrueba << "]" << endl;
    cout << "  Original:  " << original << endl;
    cout << "  Resultado: " << procesado << endl;
    cout << "  Esperado:  " << esperado << endl;
    if (procesado == esperado) {
        cout << "  STATUS:     EXITO" << endl;
    } else {
        cout << "  STATUS:     FALLIDO" << endl;
    }
}



int main (){
    string resultado = cifradoVigenere("abcdef", "bcd");
    string reversa = descifradoVigenere(resultado,"bcd");
    
    cout << resultado << endl;
    cout << reversa << endl;


    cout << "=== PRUEBAS DE CIFRADO ===" << endl << endl;


    string textoCesar = "Hola Mundo 2026!";
    int shift = 3;
  
    string textoVigenere = "ATAQUE AL ALBA";
    string clave = "SOL";
    string cifradoV = cifradoVigenere(textoVigenere, clave);
    string descifradoV = descifradoVigenere(cifradoV, clave);

    verificar("Vigenere Cifrado (SOL)", textoVigenere, cifradoV, "SHLIIP SZ LDPL");
    verificar("Vigenere Descifrado", cifradoV, descifradoV, textoVigenere);
    verificar("Vigenere (Minúsculas)", "secreto", cifradoVigenere("secreto", "abc"), "sferfvo");


    return 0;
}