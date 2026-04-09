import numpy as np
from numpy import savetxt

# f(x) sesuai soal
def fx(x):
    return (-1/2) + (1/4 * np.power(x, 2)) - (x * np.sin(x)) - (1/2 * np.cos(2 * x))

# Nilai awal
a = 2.0
b = 3.0
p_data = []
fp_data = []

# Parameter
toleransi_ = 1e-5
max_itr_ = 100
itr = 0

while itr < max_itr_:
    # Hitung rumus secant
    fa, fb = fx(a), fx(b)
    if np.abs(fb - fa) < 1e-15:
        print("ERROR: f(b) - f(a) terlalu kecil!")
        break

    p = b - fb * (a - b) / (fa - fb)
    fp = fx(p)

    # Simpan data
    itr += 1
    p_data.append(p)
    fp_data.append(fp)
    print(f"Step {itr}: p = {p}, f(p) = {fp}")

    # Cek konvergensi
    if np.abs(fp) < toleransi_:
        break
    # Update
    a, b = b, p

# Simpan ke CSV
data_array = np.array(list(zip(range(1, len(p_data)+1), p_data, fp_data)), dtype=float)
savetxt('secant_hasil.csv', data_array, delimiter=',', header='iter,p,f(p)', comments='')

# Ringkasan
if len(data_array) > 0:
    p_akhir, f_akhir = data_array[-1][1], data_array[-1][2]
else:
    p_akhir, f_akhir = np.nan, np.nan


print("Jumlah iterasi:", itr)
print("Akar yang ditemukan:", p_akhir)
print("f(akar):", f_akhir)



# # Parameter awal
# p0 = 2.0   # a
# p1 = 3.0   # b
# toleransi_ = 1e-5
# max_itr_   = 100

# iterasi = 0
# data = [] 


# status = "ok"
# while iterasi < max_itr_:
#     f0 = fx(p0)
#     f1 = fx(p1)
#     denom = (f1 - f0)
#     if iterasi == 0:
#         print(f"Step {iterasi} dimulai dengan p0 = {p0}, f(p0) = {f0}, p1 = {p1}, f(p1) = {f1}.")

#     # Cek pembagi tidak nol (hindari divide-by-zero)
#     if np.abs(denom) < 1e-15:
#         status = "division_by_zero"
#         print("ERROR: f(p1) - f(p0) ≈ 0, metode tidak bisa dilanjutkan.")
#         break

#     # Rumus Secant
#     p2 = p1 - f1 * (p1 - p0) / denom
#     f2 = fx(p2)

#     iterasi += 1
#     data.append([iterasi, p2, f2])
#     print(f"Step {iterasi} selesai dengan jawaban p = {p2}, f(p) = {f2}.")

#     # Kriteria berhenti berdasarkan |f(p)|
#     if np.abs(f2) < toleransi_:
#         break

#     # Geser dua tebakan terakhir
#     p0, p1 = p1, p2

# # Simpan CSV
# data_array = np.array(data, dtype=float)
# savetxt('secant_hasil.csv', data_array, delimiter=',', header='iter,p,f(p)', comments='')

# # Ringkasan
# if len(data) > 0:
#     p_akhir, f_akhir = data[-1][1], data[-1][2]
# else:
#     p_akhir, f_akhir = np.nan, np.nan

# print("\nMetode Secant selesai.")
# print("Status:", status)
# print("Jumlah iterasi:", iterasi)
# print("Akar yang ditemukan:", p_akhir)
# print("f(akar):", f_akhir)
