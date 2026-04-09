def affine(hex_string):
    """Transformasi affine untuk S-box AES"""
    result = 0
    matrix = [0xF1, 0xE3, 0xC7, 0x8F, 0x1F, 0x3E, 0x7C, 0xF8]  # Matriks transformasi
    c = 0x63  # Konstanta   11010011
    for i in range(8):
        bit = 0
        for j in range(8):
            if (hex_string >> j) & 1:
                bit ^= (matrix[i] >> j) & 1
        bit ^= (c >> i) & 1
        result |= (bit << i)
        
    return result
def matrix_mult(a, b):
    """Perkalian matriks di GF(2)"""
    result = 0
    for i in range(8):
        if (b >> i) & 1:
            result ^= a
        a = (a << 1) ^ (0x1B if (a & 0x80) else 0)  # Reduksi modulo x^8 + x^4 + x^3 + x + 1
    return result
