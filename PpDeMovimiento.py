import numpy as np
import cv2 as cv

# Iniciar la captura de video desde la cámara
cap = cv.VideoCapture(0)

# Parámetros para el flujo óptico Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Leer el primer frame de la cámara
ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Posición inicial de la pelotita (un único punto en el centro de la imagen)
ball_pos = np.array([[300, 300]], dtype=np.float32)
ball_pos = ball_pos[:, np.newaxis, :]

# Punto de generación original de la pelota
original_pos = np.array([[300, 300]], dtype=np.float32)
original_pos = original_pos[:, np.newaxis, :]

# Definir los límites del marco azul
frame_margin = 60

while True:
    # Capturar el siguiente frame
    ret, frame = cap.read()
    if not ret:
        break

    x, y = frame.shape[:2]
    frame = cv.flip(frame, 1)

    # Convertir el frame a escala de grises
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular el flujo óptico para mover la pelotita
    new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)

    # Si se detecta el nuevo movimiento, actualizar la posición de la pelotita
    if new_ball_pos is not None:
        ball_pos = new_ball_pos

        # Verificar si la pelota está dentro del marco
        a, b = ball_pos.ravel()
        if a < frame_margin or a > y - frame_margin or b < frame_margin or b > x - frame_margin:
            # Si la pelota se sale del marco, regresarla al punto de generación original
            ball_pos = original_pos
            a, b = ball_pos.ravel()

        # Dibujar la pelotita en su nueva posición
        frame = cv.circle(frame, (int(a), int(b)), 20, (0, 255, 0), -1)

    # Dibujar el marco azul
    cv.rectangle(frame, (frame_margin, frame_margin), (y - frame_margin, x - frame_margin), (1000, 900, 90), 5)

    # Mostrar solo una ventana con la pelotita en movimiento
    cv.imshow('Pelota en movimiento', frame)

    # Actualizar el frame anterior para el siguiente cálculo
    prev_gray = gray_frame.copy()

    # Presionar 'Esc' para salir
    if cv.waitKey(30) & 0xFF == 27:
        break

# Liberar la captura y destruir todas las ventanas
cap.release()
cv.destroyAllWindows()