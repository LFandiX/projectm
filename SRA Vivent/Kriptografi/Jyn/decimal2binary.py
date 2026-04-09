
input = "12.75"

integer, decimal = input.split(".")
integer = int(integer)
decimal = float("0." + decimal)

def integer_to_binary(n):
    if n == 0:
        return "0"
    bits = []
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    bits.reverse()
    return ''.join(bits)

def decimal_to_binary_fraction(fraction, precision=10):
    bits = []
    count = 0
    while fraction > 0 and count < precision:
        fraction *= 2
        bit = int(fraction)
        bits.append(str(bit))
        print(f"Bit {count}: {bit}")
        fraction -= bit
        print(f"Remaining fraction: {fraction}")
        count += 1
    return ''.join(bits)

binary_integer = integer_to_binary(integer)
binary_decimal = decimal_to_binary_fraction(decimal, precision=10)
output = f"{binary_integer}.{binary_decimal}"
print(output)
