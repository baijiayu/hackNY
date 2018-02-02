# from tkinter import *

# def convert_float_to_list (a):
#     # a should be a float, take 10 effective numbers
#     num = int(a * 100000)
#     temp = list(str(num))
#     result = []
#     for e in temp:
#         result.append(int(e))
#     return result

# def generator (S):
#     # s is a list of floats
#     temp = []
#     for e in S:a
#         temp.append(convert_float_to_list(e))

#     for l in temp:
#         draw
import copy
import tkinter as tk
from PIL import Image,ImageDraw
import string
import random

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def find_first (x1,y1,x2,y2):
        k = (y2-y1)/(x2-x1)
        b = y1 - x1*k
        return (k,b)

def find_second (x1,y1,x2,y2,x3,y3):
        #solve for b
        denominator = (x1-x2)*(x1**2-x3**2)
        denominator = denominator/(x1**2 - x2**2) - (x2 - x3)
        nominator = (y1-y2)*(x2**2-x3**2)
        nominator = nominator/(x1**2 - x2**2) - (y2 - y3)
        b = nominator/denominator
        #solve for a
        a = ((y1-y2)+b*(x2-x1))/(x1**2-x2**2)
        #sovle for b
        c = y1 - a*(x1**2) - b*x1
        return (a,b,c)

def find_third (x1,y1,x2,y2,x3,y3,x4,y4):
        #solve for a and b
        tmp1 = (x2-x4)/(x3-x4)
        A = (y3-y4) * tmp1 - (y2 - y4)
        B = (x3**3 - x4**3) * tmp1 - (x2**3 - x4 ** 3)
        C = (x3**2 - x4**2) * tmp1 - (x2**2 - x4 ** 2)
        tmp2 = (x2-x4)/(x1-x4)
        D = (y1-y4) * tmp2 - (y2 - y4)
        E = (x1**3 - x4**3) * tmp2 - (x2**3 - x4 ** 3)
        F = (x1**2 - x4**2) * tmp2 - (x2**2 - x4 ** 2)
        a = (A*F/C - D) / (B*F/C - E)
        b = (A - B*a)/C
        c = (y3 - y4) - a * (x3**3 - x4**3) - b * (x3**2 - x4**2)
        d = y1 - a*(x1**3) - b*(x1**2) - c*x1
        return (a,b,c,d)

def convert_num_to_rgb (n):
    # n should be a float
    # n should be between -50 and 50
    m = (n+50) * 10**4
    r = int(m // 10**4)
    g = int(m // 10**2 - r * 100)
    b = int(m % 100)
    return (r,g,b)

def convert_initial_list(A):
    # A is a 40*12 2-D list
    k = list()
    for i in range(len(A)):
        l = list()
        for j in range(len(A[i])):
            l.append(convert_num_to_rgb(A[i][j]))
        k.append(l)
    return k

def row_function(A,x,y):
    
    if (x >= 390 or y >= 330):
        return (0,0,0)
    S = convert_initial_list(A)
    start = (y // 10) * 10
    end = start + 10
    (r1,g1,b1) = S[x // 10][y // 30]
    # (30, 56) --> (3,1)
    (r2,g2,b2) = S[x // 10][y//30 + 1]
    # (30, 56) --> (3,2)
    (k_r,c_r) = find_first(start,r1,end,r2)
    (k_g,c_g) = find_first(start,g1,end,g2)
    (k_b,c_b) = find_first(start,b1,end,b2)

    final_r = k_r * x + c_r
    final_g = k_g * x + c_g
    final_b = k_b * x + c_b

    return (int(final_r), int(final_g), int(final_b))

def get_pixel(A,x,y):
    # x: row number
    # y: col number
    # assume the pic is 400 * 360
    if (x >= 390 or y >= 330):
        return (0,0,0)

    if (x % 10 == 0): # x is on the main-row:
        if ( y % 30 == 0): # (x,y) is the main point:
            return convert_num_to_rgb(A[x % 10][y % 30])
        else:
            return row_function(A,x,y)
    else:
        x0 = (x // 10) * 10
        x1 = x0 + 10
        x2 = x0 + 20
        x3 = x0 + 30
        (r0,g0,b0) = row_function(A,x0,y)
        (r1,g1,b1) = row_function(A,x1,y)
        (r2,g2,b2) = row_function(A,x2,y)
        (r3,g3,b3) = row_function(A,x3,y)

        (k_r,b_r) = find_first(x0,r0,x1,r1)
        (a_g,b_g) = find_first(x0,g0,x1,g1)
        (p_b,q_b) = find_first(x0,b0,x1,b1)

        final_r = k_r * x + b_r
        final_g = a_g * x + b_g
        final_b = p_b * x + q_b

        return (int(final_r), int(final_g), int(final_b))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


def findRange(A,height,width,stepRow,stepCol):
    max_R = -100
    min_R = 100
    max_G = -100
    min_G = 100
    max_B = -100
    min_B = 100
    for row in range(0,height,stepRow):
        for col in range(0,width,stepCol):
            (R,G,B) = get_pixel(A,row,col)
            if(R>max_R):
                max_R = R
            if(R<min_R):
                min_R = R
            if(G>max_G):
                max_G = G
            if(G<min_G):
                min_G = G
            if(B>max_B):
                max_B = B
            if(B<min_B):
                min_B = B
    range_R = max_R - min_R
    range_G = max_G - min_G
    range_B = max_B - min_B
    result = [(min_R,range_R),(min_G,range_G),(min_B,range_B)]
    print(result)
    return result


def draw(RGBs):
        height = 400
        width = 360
        rowHeight = 10
        colWidth = 30
        #PILdraw
        [(min_R,range_R),(min_G,range_G),(min_B,range_B)] = findRange(RGBs,height,width,rowHeight,colWidth)
        image1 = Image.new("RGB", (width, height),'white')
        draw = ImageDraw.Draw(image1)
        #draw
        for row in range(0,height,10):
                for col in range(0,height,10):
                        x1 = row
                        y1 = col
                        x2 = row + 10
                        y2 = col + 10
                        (R,G,B) = get_pixel(RGBs,x1,y1)
                        R = int((R - min_R)*255/range_R)
                        G = int((G - min_G)*255/range_G)
                        B = int((B - min_B)*255/range_B)
                        color = (R,G,B)
                        print(color)
                        #PILdraw
                        draw.rectangle([(x1,y1),(x2,y2)],fill=color)
        name = id_generator()+'.jpeg'  #need coordination
        #PIL save
        image1.save(name)

A = [ [30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12]
]

print("testing begin")
draw(A)