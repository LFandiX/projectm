block = ["A7", "62", "3C", "FB", "70", "03", "EE", "36", "F2", "3A", "7D", "E2", "45", "07", "0B", "1C"]

shifted_block = [0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11]

result = [block[i] for i in shifted_block]  
print("Hasil ShiftRow:", result)


def gf_mul(a, b):
    """Perkalian di GF(2^8) dengan reduksi modulo 0x11B"""
    MOD = 0x11B
    res = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0x100:  # jika bit ke-9 muncul
            a ^= MOD
        b >>= 1
    return res


def mixcolumn(column):
    mix_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]
    
    result = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            result[i] ^= gf_mul(mix_matrix[i][j], column[j])
    return result


# ['A7', '03', '7D', '1C', '70', '3A', '0B', 'FB', 'F2', '07', '3C', '36', '45', '62', 'EE', 'E2']
column1 = [0xA7, 0x03, 0x7D, 0x1C]
column2 = [0x70, 0x3A, 0x0B, 0xFB]
column3 = [0xF2, 0x07, 0x3C, 0x36]
column4 = [0x45, 0x62, 0xEE, 0xE2]
mixed_column1 = mixcolumn(column1)
mixed_column2 = mixcolumn(column2)
mixed_column3 = mixcolumn(column3)
mixed_column4 = mixcolumn(column4)
print("Hasil MixColumn kolom :", [f"{b:02X}" for b in mixed_column1+ mixed_column2 + mixed_column3 + mixed_column4])


