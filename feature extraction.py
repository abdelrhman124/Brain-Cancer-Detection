# #Import the necessary libraries 
# import cv2 
# import matplotlib.pyplot as plt 
# import numpy as np 

# # Load the image 
# image = cv2.imread('his.jpg') 

# #Plot the original image 
# plt.subplot(3, 3, 1) 
# plt.title("Original") 
# plt.imshow(image) 

# # # Adjust the brightness and contrast 
# # # Adjusts the brightness by adding 10 to each pixel value 
# # brightness = 5
# # # Adjusts the contrast by scaling the pixel values by 2.3 
# # contrast = 1.3
# # image2 = cv2.addWeighted(image, contrast, np.zeros(image.shape, image.dtype), 0, brightness) 

# # #Save the image 
# # # cv2.imwrite('modified_image.jpg', image2) 
# # #Plot the contrast image 
# # plt.subplot(3, 3, 2) 
# # plt.title("Brightness & contrast") 
# # plt.imshow(image2) 


# averaging = cv2.blur(image,(11,11))
# # cv2.imwrite('modified_image.jpg', image2) 
# #Plot the contrast image 
# plt.subplot(3, 3, 3) 
# plt.title("averaging") 
# plt.imshow(averaging) 


# # gray = cv2.cvtColor(averaging, cv2.COLOR_BGR2GRAY, 0.7)
# # plt.subplot(2, 3, 4) 
# # plt.title("gray") 
# # plt.imshow(gray) 


# # (T, thresh) = cv2.threshold(averaging, 155, 255, cv2.THRESH_BINARY)
# # plt.subplot(2, 3, 5) 
# # plt.title("thresh") 
# # plt.imshow(thresh) 

# # (T, threshInv) = cv2.threshold(averaging, 155, 255,cv2.THRESH_BINARY_INV)
# # plt.subplot(2, 3, 6) 
# # plt.title("threshInv") 
# # plt.imshow(threshInv) 

# ret, thresh1 = cv2.threshold(averaging, 155, 255, cv2.THRESH_BINARY) 
# plt.subplot(3, 3, 4) 
# plt.title("thresh1") 
# plt.imshow(thresh1) 


# ret, thresh2 = cv2.threshold(averaging, 155, 255, cv2.THRESH_BINARY_INV) 
# plt.subplot(3, 3, 5) 
# plt.title("thresh2") 
# plt.imshow(thresh2) 

# ret, thresh3 = cv2.threshold(averaging, 155, 255, cv2.THRESH_TRUNC) 
# plt.subplot(3, 3, 6) 
# plt.title("thresh3") 
# plt.imshow(thresh3) 

# ret, thresh4 = cv2.threshold(averaging, 155, 255, cv2.THRESH_TOZERO) 
# plt.subplot(3, 3, 7) 
# plt.title("thresh4") 
# plt.imshow(thresh4) 

# ret, thresh5 = cv2.threshold(averaging, 155, 255, cv2.THRESH_TOZERO_INV) 
# plt.subplot(3, 3, 8) 
# plt.title("thresh5") 
# plt.imshow(thresh5) 


# plt.show()


# # # import Opencv 
# # import cv2 

# # # import Numpy 
# # import numpy as np 

# # # read a image using imread 
# # img = cv2.imread("Y4.jpg", 0) 

# # # creating a Histograms Equalization 
# # # of a image using cv2.equalizeHist() 
# # equ = cv2.equalizeHist(img) 

# # # stacking images side-by-side 
# # res = np.hstack((img, equ)) 

# # # show image input vs output 
# # cv2.imshow("Y4.jpg", res) 

# # cv2.waitKey(0) 
# # cv2.destroyAllWindows() 







import cv2
import numpy as np
import argparse
import glob



img_path = "D:\image processing\Y10.jpg"
image = cv2.imread(img_path)
print("width: {} pixels".format(image.shape[1]))
print("height: {} pixels".format(image.shape[0]))
print("channels: {}".format(image.shape[2]))
dim=(500,590)
image=cv2.resize(image, dim)
cv2.imshow("image", image)




gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, 0.7)
cv2.imshow("gray",gray)
(T, thresh) = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)
cv2.imshow("thresh",thresh)
(T, threshInv) = cv2.threshold(gray, 155, 255,cv2.THRESH_BINARY_INV)
cv2.imshow("threshInv",threshInv)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow("closed",closed)

closed = cv2.erode(closed, None, iterations = 14)
closed = cv2.dilate(closed, None, iterations = 13)
def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged
canny = auto_canny(closed)

(cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, cnts, -1, (0, 0, 255), 2)
cv2.imshow("image",image)

cv2.waitKey(0)
cv2.destroyAllWindows()
