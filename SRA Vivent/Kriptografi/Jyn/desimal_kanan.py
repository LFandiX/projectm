import numpy as np


num = "75"

kanan = int(num)
denum  = 10**len(num)
bit_kanan = []
pecahan_kanan = kanan
for _ in range(10):
    pecahan_kanan = pecahan_kanan * 2
    sisa_bulat, pecahan_kanan = np.divmod(pecahan_kanan, denum)
    bit_kanan.append(int(sisa_bulat))
    pecahan_kanan = int(pecahan_kanan)
    if pecahan_kanan == 0:
        break
bitstr_kanan = ''.join(map(str, bit_kanan))
print(bitstr_kanan)

