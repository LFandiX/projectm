def caesar_brute_force(ciphertext):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    results = []
    
    for shift in range(1, 26):
        decrypted_text = ''
        for char in ciphertext:
            if char.upper() in alphabet:
                index = (alphabet.index(char.upper()) - shift) % 26
                if char.islower():
                    decrypted_text += alphabet[index].lower()
                else:
                    decrypted_text += alphabet[index]
            else:
                decrypted_text += char
        results.append((shift, decrypted_text))
    
    return results


