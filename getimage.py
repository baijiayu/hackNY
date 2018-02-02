import Tkinter as tk
import Image,ImageDraw
import string
import random

def find_linear_interpolation (x1,y1,x2,y2):
	k = (y2-y1)/(x2-x1)
	b = y1 - x1*k
	return (k,b)

def find_quad_interpolation (x1,y1,x2,y2,x3,y3):
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

def find_third_interpolation (x1,y1,x2,y2,x3,y3,x4,y4):
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
	d = y1 - a*(x1**3) + b*(x1**2) + c*x1 + d
	return (a,b,c,d)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def draw(RBGs,name):
	height = 400
	width = 360
	rowHeight = 10
	colWidth = 30
	#tkinter draw
	root = tk.Tk()
	cv = tk.Canvas(width = width, height=height)
	cv.pack()
	#PILdraw
	image1 = Image.new("RGB", (width, height),white)
	draw = ImageDraw.Draw(image1)
	#draw
	for row in len(list):
		for col in len(list):
			x1 = row*rowHeight
			y1 = col*colWidth
			x2 = (row+1)*rowHeight
			y2 = (col+1)*colWidth
			color = get_pixel(RBG,x1,y1)
			#tkinter draw
			cv.create_rectangle(x1,y1,x2,y2,fill=color)
			#PILdraw
			draw.rectangle(x1,y1,x2,y2,fill=color)
	filename = id_generator() + '.jpeg'  #need coordination
	#tkinter save
	img = tkinter.PhotoImg(filename)
	#PIL save
	image1.save(filename)













