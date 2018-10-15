import math
def dct(u, v, arr):
    cu = 1
    cv = 1
    if u == 0:
        cu = 1/(2**(1/2)) 
    if v == 0:
        cv = 1/(2**(1/2))

    sum = 0
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            term1 = math.cos((2*x+1)*u*math.pi/16)
            term2 = math.cos((2*y+1)*v*math.pi/16)
            sum += arr[x][y] * term1 * term2

    result = cu*cv*sum/4

    return result
            
    

arr =  [[188, 180, 155, 149, 179, 116, 86, 96],
        [168, 179, 168, 174, 180, 111, 86, 95],
        [150, 166, 175, 189, 165, 101, 88, 97],
        [163, 165, 179, 184, 135, 90, 91, 96],
        [170, 180, 178, 144, 102, 87, 91, 98],
        [175, 174, 141, 104, 85, 83, 88, 96],
        [153, 134, 105, 82, 83, 87, 92, 96],
        [117, 104, 86, 80, 86, 90, 92, 103]]



coeff = [[None for y in range(len(arr[x]))] for x in range(len(arr))]

print()
print('DCT Coefficient Table')
print('------------------------------------------------')
for u in range(len(coeff)):
    for v in range(len(coeff[u])):
        coeff[u][v] = dct(u,v,arr)
        print('%.1f' % coeff[u][v], end=' ')
    print()
print('\n')

quant_coeff = [[None for y in range(len(arr[x]))] for x in range(len(arr))]
print('Quantized Coefficient Table')
print('------------------------------------------------')
for u in range(len(coeff)):
    for v in range(len(coeff[u])):
        quant_coeff[u][v] = round(coeff[u][v]/100)
        print(quant_coeff[u][v], end=' ')
    print()


