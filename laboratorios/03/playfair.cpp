#include <iostream>
#include <vector>
#include <string>
#include <functional>
#include <algorithm>

using namespace std;
using CipherFunc = function<string(const string&, bool)>;

CipherFunc createPlayfairCipher(const string& key) {
    
    vector<char> matrix;
    vector<bool> used(26, false);

    used['J' - 'A'] = true;
    for(char c: key){
        c = toupper(c);
        c = c=='J'?'I':c;
        //usados
        if(isalpha(c) && !used[c-'A']){
            matrix.push_back(c);
            used[c-'A'] = true;
        }
    }

    for(char c = 'A'; c <= 'Z'; c++){
        if(!used[c-'A']){
            matrix.push_back(c);
            used[c-'A'] = true;
        }
    }

    return [matrix](string text, bool cipher) -> string {
        string result = "", processedText = "";
        int shift = cipher ? 1 : 4; 

        if(cipher){
            string clean = "";
            for (char c : text) if (isalpha(c)) clean += c;

            for (int i = 0; i < clean.length(); ++i) {
                processedText += clean[i];
                if (i + 1 < clean.length()) {
                    if(clean[i] == clean[i+1]){
                        processedText += 'X';
                        i++ ; 
                    }  
                    else processedText += clean[++i];
                }
            }
            if (processedText.length() % 2 != 0) processedText += 'X';
        }else{
            for (char c : text) if (isalpha(c)) processedText += c;
        }
        text = processedText;

        for (size_t i = 0; i < text.length(); i += 2) {

            bool a_mayus = isupper(text[i]);
            bool b_mayus = isupper(text[i+1]);

            char a = toupper(text[i]);
            char b = toupper(text[i+1]);

            a = a == 'J' ? 'I' : a;
            b = b == 'J' ? 'I' : b;

            int idx1 = distance(matrix.begin(), find(matrix.begin(), matrix.end(), a));
            int idx2 = distance(matrix.begin(), find(matrix.begin(), matrix.end(), b));

            int r1 = idx1 / 5, c1 = idx1 % 5;
            int r2 = idx2 / 5, c2 = idx2 % 5;

            if (r1 == r2) {
                // Misma fila: desplazar columnas circularmente
                a = matrix[r1 * 5 + (c1 + shift) % 5];
                b = matrix[r2 * 5 + (c2 + shift) % 5];
            } 
            else if (c1 == c2) {
                // Misma columna: desplazar filas circularmente
                a = matrix[((r1 + shift) % 5) * 5 + c1];
                b = matrix[((r2 + shift) % 5) * 5 + c2];
            } 
            else {
                // Rectángulo: intercambiar columnas
                a = matrix[r1 * 5 + c2];
                b = matrix[r2 * 5 + c1];
            }

            result += a_mayus ? a : tolower(a);
            result += b_mayus ? b : tolower(b);
        }

        return result;
    };
    
}


int main() {
    // Test
    auto playfair = createPlayfairCipher("silla");

    string original = "Alfonso";
    string cifrado = playfair(original, true);
    string descifrado = playfair(cifrado, false);

    cout << "Original:  " << original << endl;
    cout << "Cifrado:   " << cifrado << endl;
    cout << "Descifrado: " << descifrado << endl;

    return 0;
}