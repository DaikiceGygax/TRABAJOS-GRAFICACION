import cv2 as cv
import numpy as np

# Parámetros de la ventana y la pelota
width, height = 500, 500
radius = 30
x, y = width // 2, height // 2  # Posición inicial
vx, vy = 5, 3                   # Velocidad inicial

while True:
    img = np.ones((height, width, 3), dtype=np.uint8) * 255  # Fondo blanco

    # Dibujar el círculo
    cv.circle(img, (x, y), radius, (0, 0, 255), -1)

    # Mostrar la imagen
    cv.imshow('PingPong', img)

    # Actualizar posición
    x += vx
    y += vy

    # Rebote en los bordes
    if x - radius <= 0 or x + radius >= width:
        vx *= -1
    if y - radius <= 0 or y + radius >= height:
        vy *= -1

    # Salir con ESC
    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()