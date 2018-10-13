import math
def H(arr):

    H = 0
    for i in arr:
        H += i * math.log2(i)

    return -H

arr = [.390625, .078125, .078125, .15625, .015625, .03125, .03125, .0625, .15625]

print (H(arr))

bits = [1,4, 4, 3, 6, 6, 5, 4, 3]

avg = 0
for i in range(0,len(bits)):
    avg += bits[i] * arr[i]
    print(bits[i], arr[i])

print(avg)


