import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Casa: cuerpo
cv.rectangle(img, (150, 300), (350, 450), (150, 100, 50), -1)
# Casa: techo
pts = np.array([[140, 300], [360, 300], [250, 200]], np.int32)
cv.fillPoly(img, [pts], (100, 50, 0))
# Puerta
cv.rectangle(img, (230, 380), (270, 450), (80, 40, 0), -1)
# Ventana
cv.rectangle(img, (170, 330), (210, 370), (200, 220, 255), -1)
cv.rectangle(img, (290, 330), (330, 370), (200, 220, 255), -1)

# Chimenea
cv.rectangle(img, (320, 220), (340, 282), (100, 50, 0), -1)
# Humo (círculos, para animar después)
cv.circle(img, (330, 200), 12, (180, 180, 180), -1)
cv.circle(img, (340, 180), 10, (200, 200, 200), -1)
cv.circle(img, (350, 160), 8, (220, 220, 220), -1)

cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows()