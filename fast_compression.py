from PIL import Image, ImageDraw
from collections import defaultdict
import random
import math
import sys
import numpy as np



def openColor(file_name):
    with open(file_name, 'rb') as f:
        r = f.read(352*288)
        g = f.read(352*288)
        b = f.read(352*288)

        rgb_pixels = [[(r[i*352+j], g[i*352+j], b[i*352+j])
                        for j in range(352)] for i in range(288)]
        
        '''
        r_band = Image.frombytes('L', (352,288), r)
        b_band = Image.frombytes('L', (352,288), b)
        g_band = Image.frombytes('L', (352,288), g)

        im = Image.merge('RGB', (r_band, g_band, b_band))
        im.show()
        '''
        

    return rgb_pixels

def openGrey(file_name):
    with open(file_name, 'rb') as f:
        im_buffer = f.read()
        grey_pixels = [[im_buffer[i*352+j] for j in range(352)] for i in range(288)]
        
    
    return grey_pixels


def init_codes(vectors, N):
    codes = []
    while len(codes) != N:
        index = random.randrange(len(vectors))
        if vectors[index] not in codes:
            codes.append(vectors[index])
    return codes



def vectorize(pixels, mode):
    vectors = []
    if mode == 1:
        i = 0
        j = 0
        while i < len(pixels):
            while j < len(pixels[i])-1:
                vectors.append((pixels[i][j], pixels[i][j+1]))
                j += 2
            i += 1
            j = 0

    elif mode == 2:
        i = 0
        j = 0
        while i < len(pixels)-1:
            while j < len(pixels[i])-1:
                vectors.append((pixels[i][j], pixels[i][j+1], pixels[i+1][j], pixels[i+1][j+1]))
                j += 2
            i += 2
            j = 0

    elif mode == 3:
        i = 0
        j = 0
        while i < len(pixels)-3:
            while j < len(pixels[i])- 3:
                vectors.append((pixels[i][j], pixels[i][j+1], pixels[i][j+2], pixels[i][j+3],
                                pixels[i+1][j], pixels[i+1][j+1], pixels[i+1][j+2], pixels[i+1][j+3],
                                pixels[i+2][j], pixels[i+2][j+1], pixels[i+2][j+2], pixels[i+2][j+3],
                                pixels[i+3][j], pixels[i+3][j+1], pixels[i+3][j+2], pixels[i+3][j+3]
                                ))
                j += 4
            i += 4
            j = 0

    return vectors

def distance(point1, point2):

    sum = 0
    for i in range(len(point1)):
        sum += (point1[i] - point2[i]) ** 2

    return (sum ** (1/2))

def cluster(codes, vectors):

    #step 3
    clusters = [[] for code in codes]
    for i,v in enumerate(vectors):
        min_d = float('inf')
        test = codes - vectors[i]
        test = np.linalg.norm(test, axis=1)
        test_index = np.argmin(test)
        clusters[test_index].append(i)

    #step 4
    new_codes = []
    for indices in clusters:
        sum = [0] * len(vectors[0])
        count = 0
        for i in indices:
            count += 1
            for j in range(len(vectors[i])):
                sum[j] += vectors[i][j]
        for i in range(len(sum)):
            sum[i] = sum[i]/count

        new_codes.append(tuple(sum))
        
    new_codes = np.array(new_codes)
    return new_codes

def color_distance(color_v1, color_v2):

    sum = 0
    for i in range(len(color_v1)):
        for j in range(len(color_v1[i])):
            sum += (color_v1[i][j] - color_v2[i][j]) ** 2
    return (sum ** (1/2))

def distance(m1, m2):
    return np.linalg.norm(m1 - m2)
def color_cluster(codes, vectors):

    #step 3
    clusters = [[] for code in codes]
    for i in range(vectors.shape[0]):
        min_d = float('inf')
        test = codes - vectors[i]
        test = np.linalg.norm(test, axis=(1,2))
        test_index = np.argmin(test)
        clusters[test_index].append(i)

    #step 4
    new_codes = []
    for indices in clusters:
        sum = [[0,0,0] for i in range(len(vectors[0]))]
        count = 0
        for i in indices:
            count += 1
            for j in range(len(vectors[i])):
                for k in range(len(vectors[i][j])):
                    sum[j][k] += vectors[i][j][k]
        for i in range(len(sum)):
            for j in range(len(sum[i])):
                sum[i][j] = sum[i][j] / count
            sum[i] = tuple(sum[i])

        new_codes.append(tuple(sum))
    new_codes = np.array(new_codes)
        
    return new_codes
        
            
def quantize(pixels, codes, mode):
    new_pixels = [[0] * len(pixels[i]) for i in range(len(pixels))]
    if mode == 1:
        i = 0
        j = 0
        while i < len(pixels):
            while j < len(pixels[i])-1:
                v = (pixels[i][j], pixels[i][j+1])
                min_d = float('inf')
                for code in codes:
                    dist = distance(code,v)
                    if dist < min_d:
                        match = code
                        min_d = dist

                new_pixels[i][j] = match[0]
                new_pixels[i][j+1] = match[1]
                j += 2

            i += 1
            j = 0

    elif mode == 2:
        i = 0
        j = 0
        while i < len(pixels)-1:
            while j < len(pixels[i])-1:
                v = (pixels[i][j], pixels[i][j+1], pixels[i+1][j], pixels[i+1][j+1])
                min_d = float('inf')
                for code in codes:
                    dist = distance(code,v)
                    if dist < min_d:
                        match = code
                        min_d = dist

                new_pixels[i][j] = match[0]
                new_pixels[i][j+1] = match[1]
                new_pixels[i+1][j] = match[2]
                new_pixels[i+1][j+1] = match[3]
                j += 2
            i += 2
            j = 0

    elif mode == 3:
        i = 0
        j = 0
        while i < len(pixels)-3:
            while j < len(pixels[i])- 3:
                v=(pixels[i][j], pixels[i][j+1], pixels[i][j+2], pixels[i][j+3],
                                pixels[i+1][j], pixels[i+1][j+1], pixels[i+1][j+2], pixels[i+1][j+3],
                                pixels[i+2][j], pixels[i+2][j+1], pixels[i+2][j+2], pixels[i+2][j+3],
                                pixels[i+3][j], pixels[i+3][j+1], pixels[i+3][j+2], pixels[i+3][j+3]
                                )
                min_d = float('inf')
                for code in codes:
                    dist = distance(code,v)
                    if dist < min_d:
                        match = code
                        min_d = dist

                new_pixels[i][j] = match[0]
                new_pixels[i][j+1] = match[1]
                new_pixels[i][j+2] = match[2]
                new_pixels[i][j+3] = match[3]
                new_pixels[i+1][j] = match[4]
                new_pixels[i+1][j+1] = match[5]
                new_pixels[i+1][j+2] = match[6]
                new_pixels[i+1][j+3] = match[7]
                new_pixels[i+2][j] = match[8]
                new_pixels[i+2][j+1] = match[9]
                new_pixels[i+2][j+2] = match[10]
                new_pixels[i+2][j+3] = match[11]
                new_pixels[i+3][j] = match[12]
                new_pixels[i+3][j+1] = match[13]
                new_pixels[i+3][j+2] = match[14]
                new_pixels[i+3][j+3] = match[15]
                j += 4
            i += 4
            j = 0

    return new_pixels

def color_quantize(pixels, codes, mode):
    new_pixels = [[0] * len(pixels[i]) for i in range(len(pixels))]
    if mode == 1:
        i = 0
        j = 0
        while i < len(pixels):
            while j < len(pixels[i])-1:
                v = (pixels[i][j], pixels[i][j+1])
                min_d = float('inf')

                for code in codes:
                    dist = color_distance(code,v)
                    if dist < min_d:
                        match = code
                        min_d = dist

                new_pixels[i][j] = match[0]
                new_pixels[i][j+1] = match[1]
                j += 2

            i += 1
            j = 0

    elif mode == 2:
        i = 0
        j = 0
        while i < len(pixels)-1:
            while j < len(pixels[i])-1:
                v = (pixels[i][j], pixels[i][j+1], pixels[i+1][j], pixels[i+1][j+1])
                min_d = float('inf')
                for code in codes:
                    dist = color_distance(code,v)
                    if dist < min_d:
                        match = code
                        min_d = dist

                new_pixels[i][j] = match[0]
                new_pixels[i][j+1] = match[1]
                new_pixels[i+1][j] = match[2]
                new_pixels[i+1][j+1] = match[3]
                j += 2
            i += 2
            j = 0

    elif mode == 3:
        i = 0
        j = 0
        while i < len(pixels)-3:
            while j < len(pixels[i])- 3:
                v=(pixels[i][j], pixels[i][j+1], pixels[i][j+2], pixels[i][j+3],
                                pixels[i+1][j], pixels[i+1][j+1], pixels[i+1][j+2], pixels[i+1][j+3],
                                pixels[i+2][j], pixels[i+2][j+1], pixels[i+2][j+2], pixels[i+2][j+3],
                                pixels[i+3][j], pixels[i+3][j+1], pixels[i+3][j+2], pixels[i+3][j+3]
                                )
                min_d = float('inf')
                for code in codes:
                    dist = color_distance(code,v)
                    if dist < min_d:
                        match = code
                        min_d = dist

                new_pixels[i][j] = match[0]
                new_pixels[i][j+1] = match[1]
                new_pixels[i][j+2] = match[2]
                new_pixels[i][j+3] = match[3]
                new_pixels[i+1][j] = match[4]
                new_pixels[i+1][j+1] = match[5]
                new_pixels[i+1][j+2] = match[6]
                new_pixels[i+1][j+3] = match[7]
                new_pixels[i+2][j] = match[8]
                new_pixels[i+2][j+1] = match[9]
                new_pixels[i+2][j+2] = match[10]
                new_pixels[i+2][j+3] = match[11]
                new_pixels[i+3][j] = match[12]
                new_pixels[i+3][j+1] = match[13]
                new_pixels[i+3][j+2] = match[14]
                new_pixels[i+3][j+3] = match[15]
                j += 4
            i += 4
            j = 0

    return new_pixels

#Get user input        
file_name = sys.argv[1]
N = int(sys.argv[2])
mode = int(sys.argv[3])
if mode == 1:
    dimensions = 2
elif mode == 2:
    dimensions = 4
elif mode == 3:
    dimensions = 16

if file_name[-3:] == 'rgb':
    pixels = openColor(file_name)
    vectors = vectorize(pixels, mode)
    codes = init_codes(vectors,N)
    converged = False
    iteration = 0
    vectors = np.array(vectors)
    codes = np.array(codes)
    print('Performing k-means iterations...')
    while not converged:
        iteration += 1
        print(iteration)
        new_codes = color_cluster(codes, vectors)
        converged = True
        dist_arr = codes - new_codes
        dist_arr = np.linalg.norm(dist_arr, axis=(1,2))
        max_d = np.amax(dist_arr)
        if max_d > .3:
            converged = False
        codes = new_codes
    final_codes = [[[] for j in range(len(codes[i]))] for i in range(len(codes))]
    for i in range(len(codes)):
        for j in range(len(codes[i])):
            for k in range(len(codes[i][j])):
                final_codes[i][j].append(int(round(codes[i][j][k])))
            final_codes[i][j] = tuple(final_codes[i][j])
        final_codes[i] = tuple(final_codes[i])

    print('Quantizing (may take a minute)...')
    qpixels = color_quantize(pixels, final_codes, mode)

    raw_data = [pixel for row in pixels for pixel in row]
    quant_data = [pixel for row in qpixels for pixel in row]
    im = Image.new('RGB', (352,288))
    im.putdata(raw_data)
    im.show()
    im2 = Image.new('RGB', (352,288))
    im2.putdata(quant_data)
    im2.show()

elif file_name[-3:] == 'raw':
    pixels = openGrey(file_name)
    vectors = vectorize(pixels, mode)
    codes = init_codes(vectors, N)
    converged = False
    iteration = 0
    vectors = np.array(vectors)
    codes = np.array(codes)
    print('Performing k-means iterations...')
    while not converged:
        iteration += 1
        print (iteration)
        new_codes = cluster(codes, vectors)
        converged = True
        dist_arr = codes - new_codes
        dist_arr = np.linalg.norm(dist_arr, axis=1)
        max_d = np.amax(dist_arr)
        if max_d > .1:
            converged = False
        codes = new_codes

    print('Quantizing (may take a minute)...')
    qpixels = quantize(pixels, codes, mode)


    raw_data = [pixel for row in pixels for pixel in row]
    quant_data = [pixel for row in qpixels for pixel in row]
    im = Image.new('L', (352,288))
    im.putdata(raw_data)
    im.show()
    im2 = Image.new('L', (352,288))
    im2.putdata(quant_data)
    im2.show()
