import cv2

img = cv2.imread("class_photo.jpg")
cv2.imshow("Test Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()