# Polinomial irreducible AES (x^8 + x^4 + x^3 + x + 1)
MOD = 0x11B

def gf_mul(a, b):
    """Perkalian di GF(2^8) dengan reduksi modulo 0x11B"""
    res = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0x100:  # jika bit ke-9 muncul
            a ^= MOD
        b >>= 1
    return res

def gf_pow(a, n):
    """Pangkat di GF(2^8)"""
    res = 1
    for _ in range(n):
        res = gf_mul(res, a)
    return res

def gf_inverse(a):
    """Invers multiplikatif di GF(2^8) dengan Fermat's little theorem:
       a^(254) = a^(-1) karena order grup = 255"""
    return gf_pow(a, 254)

def affine_transform(byte):
    """Transformasi affine untuk S-box AES"""
    # Ubah byte ke array bit (LSB -> MSB)
    bits = [(byte >> i) & 1 for i in range(8)]

    # Konstanta 0x63 = 01100011 (LSB -> MSB: [1,1,0,0,0,1,1,0])
    c = [(0x63 >> i) & 1 for i in range(8)]

    result_bits = []
    for i in range(8):
        # b_i ⊕ b_{i+4} ⊕ b_{i+5} ⊕ b_{i+6} ⊕ b_{i+7} ⊕ c_i
        val = bits[i] ^ bits[(i+4) % 8] ^ bits[(i+5) % 8] ^ bits[(i+6) % 8] ^ bits[(i+7) % 8] ^ c[i]
        result_bits.append(val)

    # Ubah array bit kembali ke byte
    result = sum(b << i for i, b in enumerate(result_bits))
    return result


# Contoh: invers dari 0x59
x = 0x59
inv = gf_inverse(x)
print(f"Invers dari {x:02X} di GF(2^8) adalah {inv:02X}")

# Verifikasi: x * inv ≡ 1
print(f"Verifikasi: {x:02X} * {inv:02X} = {gf_mul(x, inv):02X}")
s = affine_transform(inv)
print(f"S-box({x:02X}) = {s:02X}")

multi = gf_mul(0xBB, 0xF0)
print(f'multi = {multi:02X}')