import cv2 as cv
import numpy as np

img = cv.imread('D:\ESCUELA\GRAFICACION\ejemploGrafi\Actividades\Convolucion\images.jpg', cv.IMREAD_GRAYSCALE)

if img is None:
    print("Error: No se pudo cargar la imagen. Verifica la ruta.")
    exit()

x, y = img.shape

scale_x, scale_y = 2,2
scaled_img = np.zeros((int(x*scale_y), int(y*scale_x)), dtype=np.uint8)

for i in range(x):
    for j in range(y):
        scaled_img[i*2,j*2] = img[i,j]
        
for i in range(1, (x*2)-1):
    for j in range(1, (y*2)-1):
        scaled_img[i,j] = ((scaled_img[i-1,j-1]*(1/9))+(scaled_img[i-1,j]*(1/9))+(scaled_img[i-1,j+1]*(1/9))
                           +(scaled_img[i,j-1]*(1/9))+(scaled_img[i,j]*(1/9))+(scaled_img[i,j+1]*(1/9))
                           +(scaled_img[i+1,j-1]*(1/9))+(scaled_img[i+1,j]*(1/9))+(scaled_img[i+1,j+1]*(1/9)))

cv.imshow('imagen', img)
cv.imshow('escalada', scaled_img)
cv.waitKey(0)
cv.destroyAllWindows()