num = input('input a number under 256 \n')

if type(int(num)) == int:
    num = int(num)

value = []
remainder = [num]

def detect_value(num, place_value):
    if num >= place_value:
        rem = num - place_value
        value.append(1)
        print(f"{place_value} can be subtracted from {num}, so subtract {place_value} from {num}, and {rem} is the remainder, carry the remainder.")
        print(f"One is appended to our binary value, since we are solving from left to right and the value for the {place_value} bit is present.")
        print('Value thus far, as represented by an array: \n',value)
        input()
        remainder.append(rem)
    else:
        value.append(0)
        print(f"{place_value} cannot be subtracted from {num}.")
        print(f"Zero is appended to binary value, since the {place_value} bit is not present.")
        print('Value thus far, as represented by an array: ',value)
        input()

place_values = [2**x for x in range(8)]

print(f"To convert an integer to a byte in binary, the method is simple.\nFirst start with an array from 0 to 7,\n{[x for x in range(8)]}\nthe values of these places represent the placeholders\nnumbered 0 through 7 for the powers of two, thus we will\nraise two to the power of these places\n{place_values}\n")
print("\n(2 to the power of that position is the value for the bit in that position)\n\n")

place_values = place_values[::-1]

print(f'Reverse the array, the left-most bit will hold the highest value.\n{place_values}\nFor each item in this array, we compare the value of the\ninteger we wish to convert to binary, and subtract out the place value\nfrom that integer if the integer is greater than or equal to that value.\nThis will result in an array that has eight items, with each item having\na value of one or zero, similar to a binary number.\n')

for x in place_values:
    detect_value(remainder[-1], x)

if remainder[-1] == 0:
    print(value,'\n\nor\n')
    value = [str(x) for x in value]
    print('0b' + ''.join(value))
else:
    print('Invalid input')