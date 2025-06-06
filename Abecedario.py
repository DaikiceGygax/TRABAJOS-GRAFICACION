import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def dedos_estirados(landmarks):
    # Devuelve una lista booleana de si cada dedo está estirado (excepto el pulgar)
    dedos = []
    # Índice, medio, anular, meñique
    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        dedos.append(landmarks[tip][1] < landmarks[pip][1])
    return dedos

def reconocer_letra(hand_landmarks, frame):
    h, w, _ = frame.shape
    puntos = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    pulgar, indice, medio, anular, meñique = puntos[4], puntos[8], puntos[12], puntos[16], puntos[20]

    # Mostrar los números de los landmarks en la imagen
    for i, (x, y) in enumerate(puntos):
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.putText(frame, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Calcular distancias
    distancia_pulgar_indice = np.linalg.norm(np.array(pulgar) - np.array(indice))
    distancia_indice_medio = np.linalg.norm(np.array(indice) - np.array(medio))
    distancia_pulgar_meñique = np.linalg.norm(np.array(pulgar) - np.array(meñique))
    distancia_pulgar_anular = np.linalg.norm(np.array(pulgar) - np.array(anular))
    distancia_indice_anular = np.linalg.norm(np.array(indice) - np.array(anular))

    # Detección de dedos estirados
    landmarks = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    dedos = dedos_estirados(landmarks)

    # Ejemplo de reglas para varias letras (puedes seguir agregando)
    # A: Puño cerrado, pulgar al lado
    if distancia_pulgar_indice < 30 and not any(dedos):
        return "A"
    # B: Todos los dedos estirados menos el pulgar
    elif all(dedos) and pulgar[1] > indice[1]:
        return "B"
    # C: Mano en forma de C (distancias grandes entre pulgar e índice y entre índice y medio)
    elif distancia_pulgar_indice > 50 and distancia_indice_medio > 50 and not dedos[3]:
        return "C"
    # D: Índice arriba, los demás doblados
    elif dedos[0] and not any(dedos[1:]):
        return "D"
    # E: Todos los dedos doblados hacia la palma
    elif not any(dedos) and pulgar[1] > indice[1]:
        return "E"
    # F: Pulgar e índice juntos formando un círculo, los demás estirados
    elif distancia_pulgar_indice < 30 and all(dedos[1:]):
        return "F"
    # G: Índice y pulgar estirados, los demás doblados
    elif dedos[0] and not any(dedos[1:]) and distancia_pulgar_indice > 40:
        return "G"
    # H: Índice y medio estirados, los demás doblados
    elif dedos[0] and dedos[1] and not any(dedos[2:]):
        return "H"
    # I: Solo meñique estirado
    elif not any(dedos[:3]) and dedos[3]:
        return "I"
    # L: Pulgar e índice estirados formando una L, los demás doblados
    elif dedos[0] and not dedos[1] and not dedos[2] and not dedos[3] and distancia_pulgar_indice > 40:
        return "L"
    # O: Todos los dedos formando un círculo (pulgar y meñique cerca)
    elif distancia_pulgar_meñique < 40 and all(dedos):
        return "O"
    # V: Índice y medio estirados, separados, los demás doblados
    elif dedos[0] and dedos[1] and not any(dedos[2:]) and distancia_indice_medio > 30:
        return "V"
    # W: Índice, medio y anular estirados, meñique y pulgar doblados
    elif dedos[0] and dedos[1] and dedos[2] and not dedos[3]:
        return "W"
    # Y: Pulgar y meñique estirados, los demás doblados
    elif not dedos[0] and not dedos[1] and not dedos[2] and dedos[3] and distancia_pulgar_meñique > 60:
        return "Y"
    # Z: Índice estirado, los demás doblados, y movimiento de trazo (no se puede detectar solo con una imagen)
    elif dedos[0] and not any(dedos[1:]):
        return "Z"
    # Puedes seguir agregando reglas para más letras...

    return "Desconocido"

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            letra_detectada = reconocer_letra(hand_landmarks, frame)
            cv2.putText(frame, f"Letra: {letra_detectada}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Reconocimiento de Letras", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()