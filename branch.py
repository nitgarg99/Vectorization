from PIL import Image, ImageDraw
from collections import defaultdict
import random
import math
import sys



def openColor(file_name):
    with open(file_name, 'rb') as f:
        r = f.read(352*288)
        g = f.read(352*288)
        b = f.read(352*288)

        rgb_pixels = [[(r[i*288+j], g[i*288+j], b[i*288+j])
                        for j in range(288)] for i in range(352)]
        
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
        grey_pixels = [[im_buffer[i*288+j] for j in range(288)] for i in range(352)]
        
    
    return grey_pixels

    
def split(rectangles, index, dimensions): #Rectangle has structure [[x0, x1], [y0,y1]]
    i = index % dimensions
    newRects = []
    for rect in rectangles:
        s = (rect[i][1] - rect[i][0] + 1) // 2
        
        rect1 = []
        rect2 = []
        for point in rect:
            rect1.append([point[0], point[1]])
            rect2.append([point[0], point[1]])

        rect1[i][1] = rect1[i][0] + s - 1
        rect2[i][0] = rect2[i][0] + s

        newRects.append(rect1)
        newRects.append(rect2)
    return newRects
    
def splitSpace(space, N):

    max_iter = int(math.log(N,2))
    dimensions = len(space)

    rectangles = []
    rectangle = []
    for dim in space:
        rectangle.append([0, 255])

    rectangles = [rectangle]
    i = 0
    while i < max_iter:
        rectangles = split(rectangles, i, dimensions)
        i += 1
    vectors = []
    for rect in rectangles:
        vector = []
        for point in rect:
            vector.append((point[0] + point[1]) / 2)
        vectors.append(vector)
    print (vectors)
    print (rectangles)
    return vectors

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
            while j < len(pixels[i])-3:
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

    #print(len(vectors))
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
        for j,code in enumerate(codes):
            dist = distance(code,v)
            if dist < min_d:
                cluster_index = j
                min_d = dist
        clusters[cluster_index].append(i)

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
        
    return new_codes
        
            
def quantize(pixels, codes, mode):
    new_pixels = [[0] * len(pixels[i]) for i in range(len(pixels))]
    print(len(new_pixels), len(new_pixels[0]))
    print(len(pixels), len(pixels[0]))
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
            while j < len(pixels[i])-3:
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

    #print(len(vectors))
    return new_pixels


#Get user input        
#file_name = int(sys.argv[1])
file_name = 'image2.raw'
#N = int(sys.argv[2])
#mode = int(sys.argv[3])
N = 32
mode = 1
if mode == 1:
    dimensions = 2
elif mode == 2:
    dimensions = 4
elif mode == 3:
    dimensions = 16

if file_name[-3:] == 'rgb':
    pixels = openColor(file_name)
    raw_data = [pixel for row in pixels for pixel in row]
    im = Image.new('RGB', (352,288))
    im.putdata(raw_data)
    im.show()

elif file_name[-3:] == 'raw':
    pixels = openGrey(file_name)
    vectors = vectorize(pixels, mode)
    codes = init_codes(vectors, N)
    converged = False
    while not converged:
        new_codes = cluster(codes, vectors)
        converged = True
        for i in range(len(codes)):
            d = distance(new_codes[i],codes[i])
            ### Error value for k-means
            if d > 5:
                converged = False
        codes = new_codes
        for code in codes:
            print('(', end='')
            for val in code:
                s = "{:.3f},".format(val)
                print(s,end=' ')
            print(')', end=' ')
        print()
    qpixels = quantize(pixels, codes, mode)


    raw_data = [pixel for row in pixels for pixel in row]
    quant_data = [pixel for row in qpixels for pixel in row]
    im = Image.new('L', (352,288))
    im.putdata(raw_data)
    im.show()
    im2 = Image.new('L', (352,288))
    im2.putdata(quant_data)
    im2.show()
