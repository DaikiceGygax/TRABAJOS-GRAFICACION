import cv2 as cv
import numpy as np

# Posiciones iniciales del humo
humo_pos = [
    [330, 200, 12, (180, 180, 180)],
    [340, 180, 10, (200, 200, 200)],
    [350, 160, 8, (220, 220, 220)]
]

while True:
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255

    # Casa: cuerpo
    cv.rectangle(img, (150, 300), (350, 450), (150, 100, 50), -1)
    # Casa: techo
    pts = np.array([[140, 300], [360, 300], [250, 200]], np.int32)
    cv.fillPoly(img, [pts], (100, 50, 0))
    # Chimenea
    cv.rectangle(img, (320, 220), (340, 282), (100, 50, 0), -1)
    # Puerta
    cv.rectangle(img, (230, 380), (270, 450), (80, 40, 0), -1)
    # Ventana
    cv.rectangle(img, (170, 330), (210, 370), (200, 220, 255), -1)
    cv.rectangle(img, (290, 330), (330, 370), (200, 220, 255), -1)

    # Animar el humo (sube y se expande)
    for i in range(len(humo_pos)):
        x, y, r, color = humo_pos[i]
        cv.circle(img, (int(x), int(y)), int(r), color, -1)
        # Transformaciones: subir y expandir
        humo_pos[i][1] -= 2  # sube
        humo_pos[i][2] += 0.2  # se expande

        # Si el humo sale de la pantalla, reiniciar
        if humo_pos[i][1] < 100:
            humo_pos[i][1] = 200 - i*20
            humo_pos[i][2] = 12 - i*2

    cv.imshow('img', img)
    if cv.waitKey(30) & 0xFF == 27:
        break

cv.destroyAllWindows()