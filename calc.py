num = input('input a number under 256 \n')

if type(int(num)) == int:
    num = int(num)

value = []
remainder = [num]

def detect_value(num, place_value):
    if num >= place_value:
        num -= place_value
        value.append(1)
        remainder.append(num)
    else:
        value.append(0)

place_values = [2**x for x in range(8)]

place_values = place_values[::-1]

for x in place_values:
    detect_value(remainder[-1], x)

if remainder[-1] == 0:
    print(value)
else:
    print('Invalid input')