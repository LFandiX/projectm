import sys

# untuk memasukan input berupa string
input_data = sys.argv[1]

#mendefine sebuah variable yang akan ditambahkan pada looping
total =0
#menghitung panjang dari masukan dalam hal ini jumlah angka binary, hal ini dapat dilakukan karena data masukan berbentuk string
length = len(input_data)


input_data = input_data[::-1]
for i in range (len(input_data)):
    # hitung = int(input_data[i])*(2**(length-i-1))
    hitung = int(input_data[i])*(2**i)
    total = total + hitung

#Mengeluarkan hasil terakhir berupa hasil penjumlahan dari tiap loop setelah loop selesai di eksekusi
print(total)




