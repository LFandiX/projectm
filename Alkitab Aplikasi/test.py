n = int(input("Masukkan nomor: "))
numbers = []
for i in range(n):
    number = int(input("Masukkan angka: "))
    numbers.append(number)


print(f"Angka terkecil adalah {min(numbers)}, angka terbesar adalah {max(numbers)}")

import random

print (random.randint(1, 100))


while False:
    print("Hello, World!")