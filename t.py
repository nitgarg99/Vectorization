import numpy as np

arr= np.array(
[[[2,6,3], [3,5,4]],
 [[7,8,3], [4,2,1]],
 [[2,2,2], [2,2,2]],
 [[3,4,5], [2,5,6]]])

print(arr.shape)

arr2 = np.linalg.norm(arr, axis=(1,2))

print(arr2)

sum = 0
for i in arr[0]:
    for j in i:
        print(j)
        sum += j**2

print (sum ** (1/2))
