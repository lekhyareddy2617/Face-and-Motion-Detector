import cv2

img=cv2.imread ("C:\\Users\\lekhy\\OneDrive\\Desktop\\lekhya\\recognition\\duck.jpg",1)
resized =cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))

cv2.imshow("Duck",resized)

#print(img)

#cv2.imshow("Duck",img)
cv2.waitKey(0)
cv2.destroyAllWindows()