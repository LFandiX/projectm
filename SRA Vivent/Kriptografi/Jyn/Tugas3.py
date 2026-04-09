import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange, CubicSpline 

# Data dari tabel
x_data = np.array([0.9, 1.3, 1.9, 2.1, 2.6, 3.0, 3.9, 4.4, 4.7, 5.0, 6.0, 7.0, 8.0, 9.2, 10.5, 11.3, 11.6, 12.0, 12.6, 13.0, 13.3])
y_data = np.array([1.3, 1.5, 1.85, 2.1, 2.6, 2.7, 2.4, 2.15, 2.05, 2.1, 2.25, 2.3, 2.25, 1.95, 1.4, 0.9, 0.7, 0.6, 0.5, 0.4, 0.25])

# (a) Piecewise-Linear (cukup dengan plot biasa)

# (b) Polinomial Lagrange
poly_lagrange = lagrange(x_data, y_data)
x_new = np.linspace(x_data.min(), x_data.max(), 100)
# x_new = x_data
y_lagrange = poly_lagrange(x_new)

# (e) Cubic Spline
cs = CubicSpline(x_data, y_data)
y_spline = cs(x_new)

# Plotting semua dalam satu gambar
plt.figure(figsize=(14, 8))

# Data asli dan Piecewise-Linear
plt.plot(x_data, y_data, 'o--', label='Piecewise-Linear & Poin Data', color='blue')

# # Lagrange
# plt.plot(x_new, y_lagrange, label='Polinomial Lagrange', color='red', alpha=0.7)


# # Cubic Spline
# plt.plot(x_new, y_spline, label='Cubic Spline', color='green', linewidth=2.5)

plt.title('Perbandingan Metode Interpolasi')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.axis("equal")
plt.show()