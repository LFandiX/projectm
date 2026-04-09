import sys

# untuk memasukan input berupa string
input_data = sys.argv[1]
binary_string = bin(int(input_data))[2:]
print(binary_string)

# Manual
num = int(input_data)
if num == 0:
    print("0")
else:
    bits = []
    while num > 0:
        bits.append(str(num % 2))
        num //= 2
    bits.reverse()
    print(''.join(bits))