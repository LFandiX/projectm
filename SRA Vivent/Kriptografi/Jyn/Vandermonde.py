
import numpy as np

# x = np.array([0.9, 1.3, 1.9, 2.1, 2.6, 3.0, 3.9, 4.4, 4.7, 5.0,
#               6.0, 7.0, 8.0, 9.2, 10.5, 11.3, 11.6, 12.0, 12.6, 13.0, 13.3])
# y = np.array([1.3, 1.5, 1.85, 2.1, 2.6, 2.7, 2.4, 2.15, 2.05, 2.1,
#               2.25, 2.3, 2.25, 1.95, 1.4, 0.9, 0.7, 0.6, 0.5, 0.4, 0.25])

x = np.array([1,3,5])
y = np.array([0,-2,2])

def vandermonde_matrix_A(x, n):
    hasil = np.array([])
    for xi in x:
        row = np.array([])
        for j in range(n):
            row = np.append(row, xi ** j)
        hasil = np.append(hasil, row)
    return hasil.reshape((len(x), n))

def vandermonde_mat_A(x, n):
    hasil = []
    for xi in x:
        row = []
        for j in range(n):
            row.append(xi ** j)
        hasil.append(row)
    return np.array(hasil)


def vandermonde_matrix_B(y, n):
    return np.array([[yi] for yi in y])

# ini klo mau langsung A dan B
def vandermonde_matrix_A_B(x, n):
    return np.array([[xi ** j for j in range(n)] for xi in x]), np.array([[yi] for yi in y])

print ("Matrix A: \n",vandermonde_matrix_A(x, 3),'\nMatrix B: \n', vandermonde_matrix_B(y, 3))
print ("Matrix A: \n",vandermonde_mat_A(x, 3))




import numpy as np

# Data dari tabel (21 poin)
x_data = np.array([0.9, 1.3, 1.9, 2.1, 2.6, 3.0, 3.9, 4.4, 4.7, 5.0, 6.0, 7.0, 8.0, 9.2, 10.5, 11.3, 11.6, 12.0, 12.6, 13.0, 13.3])
y_data = np.array([1.3, 1.5, 1.85, 2.1, 2.6, 2.7, 2.4, 2.15, 2.05, 2.1, 2.25, 2.3, 2.25, 1.95, 1.4, 0.9, 0.7, 0.6, 0.5, 0.4, 0.25])

# Membuat matriks Vandermonde A
# Dengan N=21, kita mencari polinomial derajat 20 (N-1)
# np.vander(x, N) akan membuat matriks dengan N kolom
A = np.vander(x_data, len(x_data), increasing=True)

# Vektor b adalah nilai f(x) atau y
b = y_data

# Menampilkan hasil (opsional, untuk verifikasi)
print("Bentuk Matriks Vandermonde A:", A.shape)
print("Bentuk Vektor b:", b.shape)
print("\nMatriks Vandermonde A (2 angka di blakang koma):")
print(np.round(A, 3))
print("\nVektor b (5 elemen pertama):")
print(b)

# def vandermonde_matrix(x, n):
#     """Generate a Vandermonde matrix.

#     Args:
#         x (list): A list of values to generate the matrix from.
#         n (int): The number of columns in the matrix.

#     Returns:
#         list: A 2D list representing the Vandermonde matrix.
#     """
#     return [[xi ** j for j in range(n)] for xi in x]


def vandermonde_mat_A(x, n):
    hasil = []
    for xi in x:
        row = []
        for j in range(n):
            row.append(xi ** j)
        hasil.append(row)
    return np.array(hasil)


def vandermonde_matrix_B(y, n):
    return np.array([[yi] for yi in y])

# ini klo mau langsung A dan B
def vandermonde_matrix_A_B(x, n):
    return np.array([[xi ** j for j in range(n)] for xi in x]), np.array([[yi] for yi in y])

print ("Matrix A: \n",vandermonde_matrix_A(x_data, 5),'\nMatrix B: \n', vandermonde_matrix_B(y_data, 5))