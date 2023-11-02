from PIL import Image, ImageFilter
import os

for filename in os.listdir('D://Music Player App//blur'):

    im = Image.open(rf'D://Music Player App//blur//{filename}')

    im1 = im.filter(ImageFilter.GaussianBlur(3))

    im1.save(f"D://Music Player App//blur//{filename+'-bg.png'}")


'''
im = Image.open(rf'D://Music Player App//images//Bharatham.jpeg')
 
im1 = im.filter(ImageFilter.GaussianBlur(4))
 
im1.save(f"D://Music Player App//images//Bharatham.jpeg"+'-bg.png')
'''
