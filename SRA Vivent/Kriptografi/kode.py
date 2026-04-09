# DES operations for the three tasks in the image (03A, 03B, 03C)
# This code computes:
# - 03A: initial permutation (IP) on the given 64-bit plaintext and prints the first 5 bits with steps.
# - 03B: key scheduling: computes round-1 key (K1) from the given 64-bit key, showing PC-1, shifts, PC-2 results.
# - 03C: Feistel round 7: with the given 64-bit input at start of round 7 (i.e., input = (L6,R6)),
#         compute f(R6, K7) using DES E, S-boxes, P and then compute output of round 7 (L7,R7).
#         Print the 5 leftmost bits of the 64-bit output (L7||R7).
#
# The bitstrings are taken from the image (OCR), with leading zeros added when OCR missed them.

# Input bitstrings (from the image, cleaned)
plaintext = "1000100000011101011100011000100110100100000101111111100000000001"  # 03A, 64 bits
key64     = "0" + "110111000101101111101111010100000011111010110000110011110100000"  # 03B, prepend missing leading 0 to make 64 bits
input_r7  = "0" + "111001000010011111101011001010111111010100010011111010110011000"  # 03C, prepend 0
R5 = "10011111111110101001001001111111"  # input 32-bit untuk f-function (soal 03D)
K5 = "01011000011101111111101000001111001001000101100"  # round key 48-bit (soal 03D)

# XOR-result untuk soal 03E (hasil setelah expansion XOR subkey)
xor_given_03E = "010110101110110100000101111111000000110010101110"  # 48-bit

# Verifikasi panjang
print("len(R5) =", len(R5), "len(K5) =", len(K5), "len(xor_given_03E) =", len(xor_given_03E))



# verify lengths
assert len(plaintext) == 64
assert len(key64) == 64
assert len(input_r7) == 64

# DES tables (standard)
IP = [
58,50,42,34,26,18,10,2,
60,52,44,36,28,20,12,4,
62,54,46,38,30,22,14,6,
64,56,48,40,32,24,16,8,
57,49,41,33,25,17,9,1,
59,51,43,35,27,19,11,3,
61,53,45,37,29,21,13,5,
63,55,47,39,31,23,15,7
]

PC1 = [
57,49,41,33,25,17,9,
1,58,50,42,34,26,18,
10,2,59,51,43,35,27,
19,11,3,60,52,44,36,
63,55,47,39,31,23,15,
7,62,54,46,38,30,22,
14,6,61,53,45,37,29,
21,13,5,28,20,12,4
]

PC2 = [
14,17,11,24,1,5,
3,28,15,6,21,10,
23,19,12,4,26,8,
16,7,27,20,13,2,
41,52,31,37,47,55,
30,40,51,45,33,48,
44,49,39,56,34,53,
46,42,50,36,29,32
]

# Expansion E (32 -> 48)
E = [
32,1,2,3,4,5,
4,5,6,7,8,9,
8,9,10,11,12,13,
12,13,14,15,16,17,
16,17,18,19,20,21,
20,21,22,23,24,25,
24,25,26,27,28,29,
28,29,30,31,32,1
]

# S-boxes (8 boxes). Each is 4x16 table; we store flattened as list of 64 entries and index by row*16+col.
S_boxes = [
# S1
[
14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13
],
# S2
[
15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9
],
# S3
[
10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12
],
# S4
[
7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14
],
# S5
[
2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3
],
# S6
[
12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13
],
# S7
[
4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12
],
# S8
[
13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11
]
]

# P permutation (32-bit)
P = [
16,7,20,21,
29,12,28,17,
1,15,23,26,
5,18,31,10,
2,8,24,14,
32,27,3,9,
19,13,30,6,
22,11,4,25
]

# Left-rotation schedule for each round (1..16)
shifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

# helper functions
def permute(bitstr, table):
    return ''.join(bitstr[i-1] for i in table)

def left_rotate(bitstr, n):
    return bitstr[n:]+bitstr[:n]

def xor_bits(a,b):
    return ''.join('1' if x!=y else '0' for x,y in zip(a,b))

def sbox_substitution(bits48):
    out=""
    for i in range(8):
        block = bits48[i*6:(i+1)*6]
        row = int(block[0]+block[5],2)
        col = int(block[1:5],2)
        val = S_boxes[i][row*16+col]
        out += format(val,'04b')
    return out

# ---- 03A: Initial Permutation ----
ip_result = permute(plaintext, IP)
first5_03A = ip_result[:5]

# ---- 03B: Key schedule round 1 (K1) ----
# 1) PC-1 to get 56-bit key (C0||D0)
key56 = permute(key64, PC1)  # 56 bits
C0, D0 = key56[:28], key56[28:]
# 2) left shift by shifts[0] (round 1 = 1)
C1 = left_rotate(C0, shifts[0])
D1 = left_rotate(D0, shifts[0])
# 3) PC-2 to produce K1 (48 bits)
K1 = permute(C1 + D1, PC2)

# ---- Compute K7 for use in 03C ----
C, D = C0, D0
for r in range(7):  # apply shifts for rounds 1..7 (r=0..6)
    C = left_rotate(C, shifts[r])
    D = left_rotate(D, shifts[r])
K7 = permute(C + D, PC2)

# ---- 03C: Feistel round 7 ----
# Interpret input_r7 as (L6 || R6) entering round 7
L6 = input_r7[:32]
R6 = input_r7[32:]
# 1) Expansion E on R6 -> 48 bits
R6_expanded = permute(R6, E)
# 2) XOR with K7
xored = xor_bits(R6_expanded, K7)
# 3) S-box substitution -> 32 bits
s_out = sbox_substitution(xored)
# 4) P permutation -> 32 bits = f(R6,K7)
f_r6 = permute(s_out, P)
# 5) Compute round output: L7 = R6, R7 = L6 XOR f_r6
L7 = R6
R7 = xor_bits(L6, f_r6)
round7_output = L7 + R7
first5_03C = round7_output[:5]

# Print step-by-step results
print("=== 03A Initial Permutation ===")
print("Plaintext (64):", plaintext)
print("IP(plaintext):  ", ip_result)
print("First 5 bits after IP:", first5_03A)
print()
print("=== 03B Key Scheduling (Round 1) ===")
print("Original 64-bit Key:", key64)
print("After PC-1 (56 bits) -> C0||D0:")
print("C0:", C0)
print("D0:", D0)
print("Left-rotate by", shifts[0], "for round 1 -> C1/D1:")
print("C1:", C1)
print("D1:", D1)
print("K1 (48 bits after PC-2):", K1)
print()
print("=== K7 (for use in 03C) ===")
print("K7 (48 bits):", K7)
print()
print("=== 03C Feistel Round 7 ===")
print("Input (L6||R6):", input_r7)
print("L6:", L6)
print("R6:", R6)
print("Expanded R6 (48):", R6_expanded)
print("R6_expanded XOR K7 ->", xored)
print("After S-boxes (32):", s_out)
print("After P permutation f(R6,K7) (32):", f_r6)
print("L7 (should be R6):", L7)
print("R7 (L6 XOR f):", R7)
print("Output of round 7 (L7||R7):", round7_output)
print("First 5 bits of round-7 output:", first5_03C)



# ---- 03D: Expansion of R5 and XOR with K5 ----
R5_expanded = permute(R5, E)
xor_03D = xor_bits(R5_expanded, K5)

print("\n--- 03D Expansion & XOR (sebelum S-box) ---")
print("R5 (32):", R5)
print("Expanded R5 (48):", R5_expanded)
print("K5 (48):", K5)
print("XOR result (48):", xor_03D)

# ---- 03E: Given XOR result -> S-box -> P -> last 8 bits of final f-output ----
s_out_03E = sbox_substitution(xor_given_03E)
f_out_03E = permute(s_out_03E, P)

print("\n--- 03E S-box & P ---")
print("Given XOR (48):", xor_given_03E)
print("After S-boxes (32):", s_out_03E)
print("After P permutation f(R,K) (32):", f_out_03E)
print("Last 8 bits of f-output:", f_out_03E[-8:])
