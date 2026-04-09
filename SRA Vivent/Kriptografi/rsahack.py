# n = 31621 
# e = 70235
# # mencari p dan q 
# p = 103
# q = 307

# phi = (p-1) * (q-1)
# d = pow(e, -1, phi)
# print("d =", d)

# y = 14588
# x = pow(y, d, n)
# print("x =", x)



import math

# log 2 (15) mod 19
print(math.log(15,2) % 19)
# Hitunglah log 5 (2) (mod 13)
print(math.log(2,5) % 13)




print((199**182) % 401)

# a, k, n = list(map(int, input().split()))
# result = a
# if k == 0: print(1, 0)
# else:
#     for i in str(str(bin(k))[3:]):
#         result = result ** 2 % n
#         if i == "1":
#             result = result * a % n
#     print(result)




import math



def pow2(base, exponent, mod):
    result = 1
    base = base % mod
    while exponent > 0:
        if (exponent % 2) == 1: # Jika eksponen ganjil
            result = (result * base) % mod
        exponent = exponent >> 1 # Eksponen dibagi 2
        base = (base * base) % mod # Basis dikuadratkan
    return result
def baby_step_giant_step(g, h, p): 
    order_of_group = p - 1
    m = int(math.ceil(math.sqrt(order_of_group))) 
    print(m)
    baby_steps = {}

    for j in range(m):
        value = (h * pow2(g, j, p)) % p
        baby_steps[value] = j
    print(baby_steps)
    g_m = pow2(g, m, p)
    g_m_inverse = pow(g_m, -1, p) # Ini adalah pow(g^(-m), 1, p)
    current_giant_step = 1 # Mulai dengan g^(0*m)

    for i in range(m):
        if current_giant_step in baby_steps:
            j = baby_steps[current_giant_step]
            x = (i * m - j) % order_of_group # Pastikan x berada dalam orde grup
            if pow2(g, x, p) == h:
                print(i, j, h)
                return x
        current_giant_step = (current_giant_step * g_m) % p
    return None

# --- CONTOH PENGGUNAAN ---

# Soal 1: log_2 15 mod 19. (g=2, h=15, p=19)
g1, h1, p1 = 3, 7, 401
x1 = baby_step_giant_step(g1, h1, p1)
print(f"1. log_{g1} {h1} mod {p1} = {x1}")
print(f"   Verifikasi: {g1}^{x1} mod {p1} = {pow2(g1, x1, p1)}")


def generate_until_target(g, p, target=None):
    """
    Mengenerate pangkat g^k mod p sampai:
      - target ditemukan (kalau target diberikan), atau
      - siklus kembali ke 1.
    Mengembalikan (daftar nilai, eksponen_target atau None).
    """
    vals = []
    cur = 1
    target_exp = None
    for k in range(1, p):  # maksimal p-1 kali
        cur = (cur * g) % p
        vals.append(cur)
        if target is not None and cur == target:
            target_exp = k
            break
        if cur == 1:  # balik ke awal siklus
            break
    return vals, target_exp

# Contoh penggunaan
p = 401
g = 3
target = 381

vals, exp = generate_until_target(g, p, target)

print("Semua pangkat yang dihasilkan:")
for i, v in enumerate(vals, start=1):
    print(f"{g}^{i} ≡ {v} (mod {p})")

if exp:
    print(f"Target {target} ditemukan pada eksponen {exp}, yaitu {g}^{exp} ≡ {target} (mod {p})")

else:
    print(f"Target {target} tidak ditemukan dalam siklus.")

print(f"Jumlah pangkat yang dihasilkan: {len(vals)}")





# base = 3
# y = 381
# mod = 401
# pow = 1
# result = 0
# while True:
#     result = math.pow(base, pow) % mod
#     print(f"20^{pow} mod {mod} =", pow)
#     if result == 1:

#         break
#     pow += 1


# base = 5
# y = 2
# mod = 13
# pow = 1
# result = 0
# while True:
#     result = (base**pow) % mod
#     if result == y:
#         print("log", base, "(", y, ") (mod", mod, ") =", pow)
#         break
#     pow += 1
print((199**62) % 401)