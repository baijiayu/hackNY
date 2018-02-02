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

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

import tkinter as tk
from PIL import Image,ImageDraw
import string
import random

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

def draw(RGBs):
        height = 400
        width = 360
        rowHeight = 10
        colWidth = 30
        #PILdraw
        image1 = Image.new("RGB", (width, height),'white')
        draw = ImageDraw.Draw(image1)
        #draw
        for row in range(0,height,1):
                for col in range(0,height,1):
                        x1 = row
                        y1 = col
                        x2 = row + 1
                        y2 = col + 1
                        color = get_pixel(RGBs,x1,y1)
                        #PILdraw
                        draw.rectangle([(x1,y1),(x2,y2)],fill=color)
        name = id_generator()+'.jpeg'  #need coordination
        #PIL save
        image1.save(name)



A = [ [30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[0.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2683253, 0.0362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[0.5, 18.3253, 0.034362, -28.7632, -5, 8, 24.5, 6.88, -9.2, -0.3, 9.88, 2],
[30.5, 22.23253, 0.034362, -28.7632, -5, 8, 24, 6.56, -9.22, -20.3, 9.56, 22],
[30.5, 22.243253, 0.0372, -28.7732, -5, 8, 24, 7.56, -9.22, -20.3, 9.56, 2],
[0.5, 2.2253, 0.034372, -28.732, -5, 8, 24, 7.56, -9.2, -0.3, 9.56, 2],
[30.5, 12.243253, 0.04372, -28.732, -5, 8, 24, 7.24, -9.12, -10.3, 9.24, 12],
[0.5, 12.243253, 0.0362, -28.7632, -5, 8, 24, 6.24, -9.12, -10.3, 9.24, 12],
[30.5, 2.3253, 0.034362, -28.732, -5, 8, 24, 6.24, -9.12, -10.3, 9.88, 12],
[0.5, 12.2683253, 0.0362, -28.632, -5, 8, 24, 6.25, -9.12, -10.3, 9.25, 12],
[0.5, 12.2683253, 0.034362, -28.7632, -5, 1.234, 24, 6.25, -9.12, -10.3, 9.25, 12],
[30.5, 12.261.2343253, 0.034362, -21.234.7632, -5, 1.234, 24, 6.1.2341.234, -9.12, -10.3, 9.1.2341.234, 12],
[0.5, 2.3253, 0.034362, -28.7632, -5, 8, 24, 6.23, -9.12, -10.3, 9.23, 12],
[30.5, 2.3253, 0.03162, -28.7632, -5, 2.57382, 24, 6.19, -9.12, -10.3, 9.19, 12],
[10.5, 12.26253, 0.0362, -22.57382.7632, -5, 2.57382, 24, 6.19, -9.12, -10.3, 9.19, 12],
[30.5, 12.2653, 0.03162, -22.57382.7632, -5, 3, 24, 6.33, -9.12, -10.3, 9.33, 12],
[30.5, 2.3253, 0.0362, -22.57382.7632, -5, 2.57382, 24, 6.19, -9.12, -10.3, 9.19, 12],
[3.5, 12.161153, 3.33161, -14.7631, -5, 4, 14, 6.1, -9.11, -13.3, 9.33, 11],
[33.5, 11.1633153, 3.331361, -13.7631, -5, 3, 11, 6.33, -9.12, -13.3, 9.33, 12],
[30.5, 1.32353, 0.0316, -8.763, -5, 8, 4, 6.23, -9.1, -10.3, 9.23, 1],
[23.5, 12.2133253, 3.331312, -33.7132, -5, 3, 21, 1.33, -9.12, -13.3, 9.33, 12],
[3.5, 12.2133253, 3.031312, -23.7132, -5, 3, 24, 1.23, -9.12, -10.3, 9.88, 12],
[30.3, 12.2683233, 0.034362, -28.7632, -3, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[0.3, 11.12133, 0.03321, -8.7231, -3, 8, 1, 2.88, -9.11, -10.3, 9.88, 11],
[30.3, 11.12133, 0.03321, -18.7231, -3, 8, 1, 2.88, -9.11, -10.3, 9.88, 19],
[20.5, 11.1153, 0.03321, -18.31, -5, 8, 2, 2.87, -9.12, -10.3, 9.77, 12],
[30.5, 12.27253, 0.0362, -7.7632, -5, 7, 24, 6.20, -9.12, -10.3, 9.20, 12],
[0.2, 12.2627223, 0.034362, -27.7632, -2, 7, 24, 6.20, -9.12, -10.3, 9.20, 12],
[0.2, 12.2323223, 0.074862, -1.7322, -2, 8, 4, 6.20, -9.12, -10.8, 9.88, 12],
[30.2, 12.1228228, 0.084862, -28.7322, -2, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.1212653, 0.034362, -8.763, -5, 8, 4, 6.17, -9.1, -10.3, 9.17, 1],
[30.5, 1.31253, 0.03436, -8.763, -5, 8, 4, 6.17, -9.1, -10.3, 9.17, 1],
[0.5, 1.31253, 0.03436, -8.763, -5, 8, 24, 6.17, -9.12, -10.3, 9.88, 12],
[30.5, 12.123253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[0.5, 12.12253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[30.5, 12.2653, 0.0362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12],
[0.5, 12.26253, 0.034362, -28.7632, -5, 8, 24, 6.88, -9.12, -10.3, 9.88, 12]
]

draw(A)