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
import math

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
    
    if (x >= 400 or y >= 360):
        return (0,0,0)
    S = convert_initial_list(A)
    start = (y // 10) * 10
    end = start + 10
    (r1,g1,b1) = S[x // 10][y // 30]
    # (30, 56) --> (3,1)
    temp = y//30 + 1
    if(temp >= 12):
        temp = 10
    (r2,g2,b2) = S[x // 10][temp]
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
    if (x >= 400 or y >= 360):
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
        (a_g,b_g,c_g) = find_second(x0,g0,x1,g1,x2,g2)
        (p_b,q_b,r_b,s_b) = find_third(x0,b0,x1,b1,x2,b2,x3,b3)

        final_r = k_r * x + b_r
        final_g = a_g * (x**2) + b_g*x + c_g
        final_b = p_b * (x**3) + q_b*(x**2) + r_b*x + s_b

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
            print(R,G,B)
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
        rowHeight = 5
        colWidth = 5
        #PILdraw
        [(min_R,range_R),(min_G,range_G),(min_B,range_B)] = findRange(RGBs,height,width,rowHeight,colWidth)
        image1 = Image.new("RGB", (width, height),'white')
        draw = ImageDraw.Draw(image1)
        #draw
        for row in range(0,height,rowHeight):
                for col in range(0,width,colWidth):
                        x1 = row
                        y1 = col
                        x2 = row + rowHeight
                        y2 = col + colWidth
                        (R,G,B) = get_pixel(RGBs,x1,y1)
                        R = int((R - min_R)*255/range_R)
                        G = int((G - min_G)*255/range_G)
                        B = int((B - min_B)*255/range_B)
                        color = (R,G,B)
                        #PILdraw
                        draw.rectangle([(y1,x1),(y2,x2)],fill=color)
        name = id_generator()+'.jpeg'  #need coordination
        #PIL save
        image1.save(name)

def combineData(alphaList,omegaList):
    result = list()
    for row in range(40):
        l = list()
        for col in range(12):
            if(col<=5):
                l.append(alphaList[row][col])
            if(col>5):
                l.append(omegaList[row][col-6])
        result.append(l)
    return result
#findRange(A,400,330,10,10)

#raw data
A = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
[1893.6492518427006, -500.3054525440565, -1102.5201949234424, -2444.714599814332, -400.77734763754137, 91.38831657229036],
[-1894.3424345971189, 500.48859264315746, 1102.9237796869752, 2445.6095036611855, 400.92405481970485, -91.42176986621034],
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
[4667.547319311407, 1970.958692623958, -3083.0130991801093, -4856.824182314104, -55.9823964106505, 800.3825993919759]
,[-5227.691970058326, -2107.918436702985, 3975.3317714211203, 5378.558531969296, -5.633844559436099, -1256.3196657982876]
,[509.4840704845869, 115.57684167913258, -858.8066160909324, -469.0252115163274, 62.2173629610745, 447.21565334057357]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-6330.4655958887515, 597.822064280168, 3882.9822907921794, 9796.166886393547, 1936.600916488418, 699.4425595509493]
,[6356.091280926763, -1697.8578640162443, -4146.827858809883, -8734.832837757602, -1119.430872431455, 202.30972136166906]
,[-25.99948487962346, 1099.330404981023, 263.9074078051909, -1060.0126358617183, -816.4989579831391, -901.1005478702959]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[5472.66405357591, -6320.574833518317, -862.3196096297936, 1858.9957255969207, 2560.0377383268274, 782.4626834580101]
,[-3957.3999703693294, 1834.0216026178248, 1239.5573355598276, -1186.97161128887, -2314.936018404377, -121.70249076599083]
,[-1517.6929338884158, 4488.668671079216, -376.69975694908345, -672.8095159644429, -246.3547810056889, -660.9955250089338]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-4533.605315855243, 9339.67368934004, -1775.5851073614633, -6701.572768954117, -5209.387202038048, -3489.424272731407]
,[4527.340010198124, -9326.76654230701, 1773.131302355778, 6692.311397737244, 5202.187986219038, 3484.601993747488]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[4666.150763056075, 2216.772170597931, -3290.0095916102878, -6219.215336269004, -364.3852115040674, 818.1505092202179]
,[-4726.261312113309, -2245.32919737993, 3332.3923376889284, 6299.332860873686, 369.07931511196284, -828.690133595422]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-1980.0793930745463, 164.50381002420156, 1788.5959937135465, 2518.2566545460218, 258.6397119194461, 292.0059256690115]
,[1978.6961435199191, -164.3888904796892, -1787.34651118251, -2516.497443572956, -258.45903064597155, -291.8019353300166]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-5179.786913335384, 1913.517986860369, 2207.465171373311, 8090.012233190847, 4568.185531535197, 3061.2883847237163]
,[5118.9244292761905, -1891.034155011526, -2181.5274607972165, -7994.954608462379, -4514.509362274892, -3025.318253397239]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[5915.3522593050475, -8130.354977414222, 8.429267330823771, 759.7255716093024, 878.4837649515302, -77.6609467519475]
,[-2286.9247868860675, 5535.644131726853, 432.03348767887866, 9.583714006581072, -548.0968234477103, 241.97647094641187]
,[-3683.868265352008, 2671.0252032587177, -440.5210569996824, -776.4152815842856, -338.6303185107112, -163.57757880144754]]

B = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[95.00382688462828, -25.100177636739772, -55.31311441830521, -122.65061356905231, -20.10688184054492, 4.58492500575956]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[236.52756512888962, 99.87816483556075, -156.23142771204365, -246.11915413239805, -2.836903197168856, 40.55932044276402]
,[-25.543538867454966, -5.794570858320731, 43.05720521719403, 23.515089900236706, -3.1193352669793395, -22.421643943399395]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-317.36214907482236, 29.970322436870386, 194.66366035155352, 491.1064642355102, 97.0866707112637, 35.06481324180071]
,[1.3043803227614512, -55.15282149279994, -13.24009423132303, 53.18026993604611, 40.96331828416825, 45.20773503450272]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[274.4419082901213, -316.9627446193874, -43.243407032843265, 93.22449349008282, 128.3801883914407, 39.2387601197101]
,[76.08901742411997, -225.03787235129778, 18.885713789761844, 33.73107552933766, 12.35091289278895, 33.13878512355771]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-227.28859391389102, 468.2369003408062, -89.01750688690038, -335.9778687262854, -261.1683659720794, -174.9394314816987]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[236.7849813841863, 112.4906553178392, -166.95235526273854, -315.59562954588677, -18.490818214830686, 41.51725114177237]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-99.27013270767272, 8.247303168315668, 89.67022346546432, 126.25133778125831, 12.966752048184683, 14.639547835291403]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[-259.6695602224774, 95.92718434934196, 110.66314499949947, 405.56299977877296, 229.00917505592815, 153.46643054540561]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
,[299.3453378062284, -411.4351522126492, 0.42656155812788177, 38.44577599173013, 44.45551301920228, -3.9300182509408863]
,[184.6938701104038, -133.91412135774124, 22.08589803485351, 38.92624079893863, 16.977519161230305, 8.201101102414702]
,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
draw(combineData(A,B))