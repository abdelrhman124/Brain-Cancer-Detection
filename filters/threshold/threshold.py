import cv2


image = cv2.imread("blur3.jpg")
image2 = cv2.imread("Y2.jpg")
print("width: {} pixels".format(image.shape[1]))
print("height: {} pixels".format(image.shape[0]))
print("channels: {}".format(image.shape[2]))
dim=(500,590)
image=cv2.resize(image, dim)
image2=cv2.resize(image2, dim)
cv2.imshow("image", image)
cv2.imshow("image2", image2)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, 0.7)
cv2.imshow("gray",gray)

(T, thresh) = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)
cv2.imshow("thresh",thresh)

(T, threshInv) = cv2.threshold(gray, 155, 255,cv2.THRESH_BINARY_INV)
cv2.imshow("threshInv",threshInv)

cv2.waitKey(0)
cv2.destroyAllWindows()
