# Copyright 2020 EYST
# Calvin Institute Technology
# SCCE 2041 - Semester Ganjil 2025-2026

# Kode ini untuk melakukan pencarian akar menggunakan metode biseksi

import numpy as np
import matplotlib.pyplot as plt

from numpy import savetxt

# Definisi fungsi
def f	(x):
	# f(x) = x^3 + 4 x^2 - 10
	return (-1/2) + (1/4 * np.power(x, 2)) - (x * np.sin(x)) - (1/2 * np.cos(2 * x))

# Mulai dari a dan b
a_data = np.array([0]) # Ini permulaan a kalian
b_data = np.array([100]) # Ini permulaan b kalian
p_data = np.array([])
fp_data = np.array([])

# Toleransi
toleransi_ = 0.00001

# Maksimum iterasi
max_itr_ = 100

# Iterasi metode biseksi
itr = 0
error = 1
while itr < max_itr_:
	# Dapatkan a, b, dan p
	a = a_data[itr]
	b = b_data[itr]
	p = (a + b) / 2
	
	# Update iterasi
	itr += 1

	# Dapatkan f(x) untuk a, b, dan p
	fx_a = f(a)
	fx_b = f(b)
	fx_p = f(p)
	error = fx_p - 0

	# Cek satu negatif dan satu positif
	# Jika tidak, hentikan kode
	if (fx_a * fx_b) > 0:
		print("ERROR: f(a) dan f(b) dua-duanya positif atau dua-duanya negatif!")
		break

	# Masukkan p ke data array
	p_data = np.append(p_data, [p])
	fp_data = np.append(fp_data, [fx_p])

	# Print hasil
	print("Step " + str(itr) + " telah selesai dengan jawaban p = " + str(p) + " dan hasil f(p) = " + str(fx_p) + ".")

	# Selesai jika error lebih kecil dari toleransi
	if np.abs(error) < toleransi_:
		break

	# Untuk iterasi selanjutnya
	# p menggantikan a atau b
	if (fx_p * fx_a) > 0:
		# p menggantikan a
		a_data = np.append(a_data, [p])
		b_data = np.append(b_data, [b])
	else:
		# p menggantikan b
		a_data = np.append(a_data, [a])	 
		b_data = np.append(b_data, [p])

# Gabungkan semua data array untuk disimpan
'''
a = 1,2,3,4,5
b = 6,7,8,9,10
p = 11,12,13,14,15
fp = 16,17,18,19,20

data_array = [[1,6,11,16],
			  [2,7,12,17],	
			  [3,8,13,18],
			  [4,9,14,19],
			  [5,10,15,20]]


'''
# import numpy as np
# from numpy import savetxt
# a_data = np.array([1,2,3,4,5])
# b_data = np.array([6,7,8,9,10])
# p_data = np.array([11,12,13,14,15])
# fp_data = np.array([16,17,18,19,20])
# data_array = np.column_stack((a_data, b_data, p_data, fp_data))
# savetxt('bisection_hasil.csv', data_array, delimiter=',')

# Selesai
print("Metode Biseksi selesai dengan jumlah iterasi: ", str(itr))
print("Hasil akar yang didapatkan: ", str(p_data[-1]))
print("Error: ", str(error))

