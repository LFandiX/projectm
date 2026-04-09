# Copyright 2020 EYST
# Calvin Institute Technology
# SCCE 2041 - Semester Ganjil 2025-2026

# Kode ini untuk melakukan pencarian akar menggunakan metode newton-raphson

import numpy as np
import matplotlib.pyplot as plt

from numpy import savetxt

# Definisi fungsi
def fx(x):
	# f(x) = x^3 + 4 x^2 - 10
	return (-1/2) + (1/4 * np.power(x, 2)) - (x * np.sin(x)) - (1/2 * np.cos(2 * x))

# Definisi turunan fungsi f(x)
def dfx(x):
	# f(x) = 3 x^2 + 8 x
	return np.sin(2 * x) - np.sin(x) - (x*np.cos(x)) + (1/2) * np.power(x, 1)

# Mulai dari a dan b
p_data = np.array([20*np.pi])
fp_data = np.array([fx(20*np.pi)])

# Toleransi
toleransi_ = 0.00001

# Maksimum iterasi
max_itr_ = 100

# Iterasi metode biseksi
itr = 0
error = 1
while itr < max_itr_:
	# Dapatkan f(x) dan df(x) untuk p = p(i)
	p = p_data[itr]
	fx_p = fx(p)
	dfx_p = dfx(p)

	# Output data inisial
	if itr == 0:
		print("Step " + str(itr) + " dimulai dengan jawaban p = " + str(p) + " dan hasil f(p) = " + str(fx_p) + ".")

	# Cek df(x) bukan nol
	if np.abs(dfx_p) < 1.E-15:
		print("ERROR: df(x) mendekati nol!")
		break

	# Hitung p_baru = p(i+1)
	p_baru = p_data[itr] - fx_p / dfx_p

	# Hitung f(p_baru)
	fx_p_baru = fx(p_baru)
	error = fx_p_baru

	# Masukkan p ke data array
	p_data = np.append(p_data, [p_baru])
	fp_data = np.append(fp_data, [fx_p_baru])

	# Update iterasi
	itr += 1

	# Print hasil
	print("Step " + str(itr) + " telah selesai dengan jawaban p = " + str(p_baru) + " dan hasil f(p) = " + str(fx_p_baru) + ".")

	# Selesai jika error lebih kecil dari toleransi
	if np.abs(error) < toleransi_:
		break


# Gabungkan semua data array untuk disimpan
data_array = np.column_stack((p_data, fp_data))
savetxt('newton_hasil.csv', data_array, delimiter=',')

# Selesai
print("Metode Newton selesai dengan jumlah iterasi setelah angka pertama: ", str(itr))
print("Hasil akar yang didapatkan: ", str(p_data[-1]))
print("Error: ", str(error))


x = np.linspace(-20*np.pi, 20*np.pi, 100)
y = fx(x)
plt.plot(x, y, label='f(x)')
plt.axhline(0, color='black', lw=0.5, ls='--')

plt.scatter(p_data, fp_data, color='red',  label='Iterasi Newton-Raphson')
plt.title('Metode Newton-Raphson')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid()
plt.show()
