import sys

# untuk memasukan input berupa string
input_data = sys.argv[1]

left,right = input_data.split(".")
#ex: 101.110
# Manual
def binary_to_decimal(binary_string):
    decimal_value = 0
    for i, bit in enumerate(reversed(binary_string)):
        decimal_value += int(bit) * (2 ** i)
    return decimal_value

integer_part = binary_to_decimal(left)
decimal_part = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(right))

output_data = integer_part + decimal_part
print(output_data)