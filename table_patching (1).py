import cv2
import numpy as np
import matplotlib.pyplot as plt
import re


# mounting drive on google collab
# from google.colab import drive
# drive.mount('/content/drive')

# path to image, provide here if you'r using different path.
# specify path to image , according to your image input file path.
file=r'/content/drive/My Drive/Table_Patching/img/results_3.jpg'  
 



img = cv2.imread(file,0)
#thresholding the image to a binary image
thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
#inverting the image 
img_bin = 255-img_bin



kernel_len = np.array(img).shape[1]//100
# Defining a vertical kernel to detect all vertical lines of image 
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
# Defining a horizontal kernel to detect all horizontal lines of image
hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
# A kernel of 2x2
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

#Use horizontal kernel to detect and save the horizontal lines in a jpg
image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
print(horizontal_lines)
ln=(len(horizontal_lines))

# file=r'C://Users//Aaditya Raj//Deep Learning//projects//praemineo//img/horizontal2.jpg'
hor_kernel = np.ones((1,ln), np.uint8)  # note this is a horizontal kernel
d_im = cv2.dilate(image_2, hor_kernel, iterations=1)
e_im = cv2.erode(d_im, hor_kernel, iterations=1)


#Using vertical kernel to detect and save the vertical lines in a jpg
image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
v_ln=len(vertical_lines)


vert_kernel = np.ones((v_ln,1), np.uint8)

dv_im = cv2.dilate(image_1, vert_kernel, iterations=1)
ev_im = cv2.erode(dv_im, vert_kernel, iterations=1)


# Combining horizontal and vertical lines in a new third image, with both having same weight.
img_vh = cv2.addWeighted(ev_im, 0.5, e_im, 0.5, 0.0)
#Eroding and thesholding the image
img_vh = cv2.erode(~img_vh, kernel, iterations=2)
thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imwrite("C://Users//Aaditya Raj//Deep Learning//projects//premenio//img//combined2.jpg", img_vh)
bitxor = cv2.bitwise_xor(img,img_vh)
bitnot = cv2.bitwise_not(bitxor)


#Extracting image name and extension to save final image in same extension and related name
picture_detail = file
regex = re.compile('(.*\/(?P<name>\w+)\.(?P<ext>\w+))')
pic_name= regex.search(picture_detail).group('name')
pic_ext= regex.search(picture_detail).group('ext')


#Path to save output image, change it according to your path or location you wish to save
img_path=r'/content/drive/My Drive/Table_Patching/img/'    




img_to_save=pic_name+'_patched.'+pic_ext

#saving the generated image
cv2.imwrite(img_path+img_to_save, bitnot)


