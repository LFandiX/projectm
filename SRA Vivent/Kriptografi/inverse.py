# Diketahui bahwa gcd(125, 335) = 5. Terapkan algoritma euclid untuk mencari bilangan bulat k dan l sehingga 125k + 225l = 5.

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y



def gcd(a, b):
    while b:
        hasil_bagi = a // b if b != 0 else 0
        a, b = b, a % b
        
        print(f"Current values: a={a}, b={b}, hasil_bagi={hasil_bagi}")
    return a

result = gcd(125, 335)
print(f"GCD is {result}")

# Hitunglah invers dari 276 dalam modulo 401 dengan menggunakan algoritma euclid.
gcd, inv, _ = gcd_extended(276, 401)
print(f"raw inverse = {inv}")
if gcd == 1:
    print(f"Inverse = {inv % 401}")






s0 = 1
s1 = 0
t0 = 0
t1 = 1
r0 = 276
r1 = 401
i = 1
print(f"i={i}, r0={r0}, r1={r1}, s0={s0}, s1={s1}, t0={t0}, t1={t1}")
while r1 != 0:
    ri = r0 // r1
    qi_1 = r0 % r1
    si = s0 - ri * s1
    ti = t0 - ri * t1
    r0, r1 = r1, qi_1
    s0, s1 = s1, si
    t0, t1 = t1, ti
    i += 1
    print(f"i={i}, qi-1={qi_1}, ri={ri}, si={si}, ti={ti}")
if r0 == 1:
    print(f"Inverse = {s0 % 401}")


def extended_gcd(r0, r1):
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    i = 1
    while r1 != 0:
        ri = r0 % r1
        qi_1 = r0 // r1
        si = s0 - qi_1 * s1
        ti = t0 - qi_1 * t1
        r0, r1 = r1, ri
        s0, s1 = s1, si
        t0, t1 = t1, ti
        if r0 == 1:
            print(f"Inverse = {s0 % 401}")
        print(f"i={i}, qi-1={qi_1}, ri={ri}, si={si}, ti={ti}")
        i += 1
    return r0, s0, t0

gcd, k, l = extended_gcd(5,343)
print(f"5 * {k} + 343 * {l} = {gcd}")


# Euler’s Totient Function

def euler_totient(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result




print((1025**2787) % 9223)


