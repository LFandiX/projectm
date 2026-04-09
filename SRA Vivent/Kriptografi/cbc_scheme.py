

plotplainToCipher = {"0":"4",
                     "1":"f",
                     '2':'1',
                     '3':'b',
                     '4':'7',
                     '5':'0',
                     '6':'d',
                     '7':'5',
                     '8':'a',
                     '9':'6',
                     'a':'9',
                     'b':'2',
                     'c':'e',
                     'd':'8',
                     'e':'c',
                     'f':'3'}

cipherToPlain = {v:k for k,v in plotplainToCipher.items()}

# Untuk setiap transaksi pemindahan dana, terdapat 12 bit (berarti membutuhkan 3 blok) informasi terenkripsi yang ditransmisikan melalui kanal yang tidak aman: id pengirim (4 bit), id penerima (4 bit), dan nominal jumlah transfer (4 bit). Anda mengetahui bahwa salah seorang nasabah Bank Calvin, yaitu Oscar yang selalu membuat transaksi aneh setiap harinya secara berulang-ulang, yaitu membuat 4 transaksi berikut yang sama setiap harinya (dalam notasi hexadecimal)
# misal plain text = 60A
# iv = 5
def encrypt(plainText, iv):
    # Bagi plain text menjadi blok-blok 4 bit
    blocks = [plainText[i:i+1] for i in range(len(plainText))]
    cipherText = ""
    previousCipher = iv

    for block in blocks:
        # XOR blok dengan previous cipher (atau IV untuk blok pertama)
        xor_result = int(block, 16) ^ int(previousCipher, 16)
        xor_hex = hex(xor_result)[2:]  
        # Enkripsi hasil XOR
        encrypted_block = plotplainToCipher[xor_hex]

        cipherText += encrypted_block
        previousCipher = encrypted_block

    return cipherText,previousCipher

plainText = "60A"
plainText2 = "60A"
plainText3 = "61A"
plainText4 = "61A"
iv = "5"

cipherText,key = encrypt(plainText, iv)
cipherText2,key2 = encrypt(plainText2, key)
cipherText3,key3 = encrypt(plainText3, key2)
cipherText4,key4 = encrypt(plainText4, key3)
print("Cipher Text:", cipherText,cipherText2,cipherText3,cipherText4)
# cipherText = "F3B"

def ofb_encrypt(plainText, iv):
    blocks = [plainText[i:i+1] for i in range(len(plainText))]
    cipherText = ""
    previousOutput = iv

    for block in blocks:
        # Enkripsi previous output
        encrypted_output = plotplainToCipher[previousOutput]

        # XOR hasil enkripsi dengan blok plaintext
        xor_result = int(block, 16) ^ int(encrypted_output, 16)
        xor_hex = hex(xor_result)[2:]  # Hasil XOR dalam hex

        # Tambahkan ke cipher text
        cipherText += xor_hex

        # Update previous output
        previousOutput = encrypted_output

    return cipherText,previousOutput

def cfb_encrypt(plainText, iv):
    blocks = [plainText[i:i+1] for i in range(len(plainText))]
    cipherText = ""
    previousCipher = iv

    for block in blocks:
        # Enkripsi previous cipher
        encrypted_output = plotplainToCipher[previousCipher]

        # XOR hasil enkripsi dengan blok plaintext
        xor_result = int(block, 16) ^ int(encrypted_output, 16)
        xor_hex = hex(xor_result)[2:]  # Hasil XOR dalam hex

        # Tambahkan ke cipher text
        cipherText += xor_hex

        # Update previous cipher
        previousCipher = xor_hex

    return cipherText,previousCipher

plainText = "60A"
plainText2 = "60A"
plainText3 = "61A"
plainText4 = "61A"
iv = "5"

cipherText,key = ofb_encrypt(plainText, iv)
cipherText2,key2 = ofb_encrypt(plainText2, key)
cipherText3,key3 = ofb_encrypt(plainText3, key2)
cipherText4,key4 = ofb_encrypt(plainText4, key3)
print("ofb Text:", cipherText,cipherText2,cipherText3,cipherText4)

cipherText,key = cfb_encrypt(plainText, iv)
cipherText2,key2 = cfb_encrypt(plainText2, key)
cipherText3,key3 = cfb_encrypt(plainText3, key2)
cipherText4,key4 = cfb_encrypt(plainText4, key3)
print("cfb Text:", cipherText,cipherText2,cipherText3,cipherText4)