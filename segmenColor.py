import cv2 as cv

# Imagen 1
img1 = cv.imread('D:/ESCUELA/GRAFICACION/ejemploGrafi/Actividades/SegmentacionColor/figuras.jpg', 1)
hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
uba1 = (130, 255, 255)
ubb1 = (110, 60, 60)
mask1 = cv.inRange(hsv1, ubb1, uba1)
res1 = cv.bitwise_and(img1, img1, mask=mask1)
cv.imshow('img1', img1)
cv.imshow('res1', res1)

# Imagen 2
img2 = cv.imread('D:/ESCUELA/GRAFICACION/ejemploGrafi/Actividades/SegmentacionColor/frutas.jpg', 1)
hsv2 = cv.cvtColor(img2, cv.COLOR_BGR2HSV)
uba2 = (5, 255, 255)
ubb2 = (0, 60, 60)
uba2_2 = (180, 255, 255)
ubb2_2 = (172, 60, 60)
mask2_1 = cv.inRange(hsv2, ubb2, uba2)
mask2_2 = cv.inRange(hsv2, ubb2_2, uba2_2)
mask2 = mask2_1 + mask2_2
res2 = cv.bitwise_and(img2, img2, mask=mask2)
cv.imshow('img2', img2)
cv.imshow('res2', res2)

# Imagen 3
img3 = cv.imread('D:/ESCUELA/GRAFICACION/ejemploGrafi/Actividades/SegmentacionColor/circles.jpg', 1)
hsv3 = cv.cvtColor(img3, cv.COLOR_BGR2HSV)
uba3 = (70, 255, 255)
ubb3 = (30, 30, 30)
mask3 = cv.inRange(hsv3, ubb3, uba3)
res3 = cv.bitwise_and(img3, img3, mask=mask3)
cv.imshow('img3', img3)
cv.imshow('res3', res3)

# Imagen 4
img4 = cv.imread('D:/ESCUELA/GRAFICACION/ejemploGrafi/Actividades/SegmentacionColor/flor.jpg', 1)
hsv4 = cv.cvtColor(img4, cv.COLOR_BGR2HSV)
uba4 = (30, 255, 255)
ubb4 = (5, 60, 60)
mask4 = cv.inRange(hsv4, ubb4, uba4)
res4 = cv.bitwise_and(img4, img4, mask=mask4)
cv.imshow('img4', img4)
cv.imshow('res4', res4)

# Imagen 5
img5 = cv.imread('D:/ESCUELA/GRAFICACION/ejemploGrafi/Actividades/SegmentacionColor/arbol.jpg', 1)
hsv5 = cv.cvtColor(img5, cv.COLOR_BGR2HSV)
uba5 = (30, 255, 255)
ubb5 = (7, 30, 30)
mask5 = cv.inRange(hsv5, ubb5, uba5)
res5 = cv.bitwise_and(img5, img5, mask=mask5)
cv.imshow('img5', img5)
cv.imshow('res5', res5)

cv.waitKey(0)
cv.destroyAllWindows()