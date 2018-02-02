from PIL import Image
import random
new_img_list = []
for i in range(500):
	new_img_list.append(random.randint(0,1000))

new_img = Image.new("L", (400, 400), "white")
new_img.putdata(new_img_list)
new_img.save('out.jpeg')