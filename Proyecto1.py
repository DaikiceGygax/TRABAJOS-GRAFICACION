import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)

def reconocer_gesto(hand_landmarks, frame):
    dedos = [hand_landmarks.landmark[i] for i in range(21)]
    # Puntas y bases
    punta_pulgar, base_pulgar = dedos[4], dedos[2]
    punta_indice, base_indice, primer_fal_indice = dedos[8], dedos[5], dedos[6]
    punta_medio, base_medio, primer_fal_medio = dedos[12], dedos[9], dedos[10]
    punta_anular, base_anular = dedos[16], dedos[13]
    punta_meñique, base_meñique = dedos[20], dedos[17]

    dist_indice = np.linalg.norm([punta_indice.x - base_indice.x, punta_indice.y - base_indice.y])
    dist_medio = np.linalg.norm([punta_medio.x - base_medio.x, punta_medio.y - base_medio.y])
    dist_anular = np.linalg.norm([punta_anular.x - base_anular.x, punta_anular.y - base_anular.y])
    dist_meñique = np.linalg.norm([punta_meñique.x - base_meñique.x, punta_meñique.y - base_meñique.y])
    primer_fal_indice_array = np.array([primer_fal_indice.x, primer_fal_indice.y])

    # Estado de los dedos
    pulgar_ext = abs(punta_pulgar.x - base_pulgar.x) > 0.08 and punta_pulgar.y > base_pulgar.y
    indice_ext = dist_indice > 0.08 and punta_indice.y < base_indice.y - 0.02
    medio_ext = dist_medio > 0.08 and punta_medio.y < base_medio.y - 0.02
    anular_ext = dist_anular > 0.08 and punta_anular.y < base_anular.y - 0.02
    meñique_ext = dist_meñique > 0.08 and punta_meñique.y < base_meñique.y - 0.02

    # Distancias
    dist_pulgar_indice = np.linalg.norm([punta_pulgar.x - punta_indice.x, punta_pulgar.y - punta_indice.y])
    dist_pulgar_medio = np.linalg.norm([punta_pulgar.x - punta_medio.x, punta_pulgar.y - punta_medio.y])
    dist_pulgar_anular = np.linalg.norm([punta_pulgar.x - punta_anular.x, punta_pulgar.y - punta_anular.y])
    dist_indice_medio = np.linalg.norm([punta_indice.x - punta_medio.x, punta_indice.y - punta_medio.y])
    dist_medio_anular = np.linalg.norm([punta_medio.x - punta_anular.x, punta_medio.y - punta_anular.y])
    dist_anular_meñique = np.linalg.norm([punta_anular.x - punta_meñique.x, punta_anular.y - punta_meñique.y])

# Letra Q: índice y medio extendidos apuntando hacia abajo, los demás doblados
    if (not indice_ext and not anular_ext and not meñique_ext and
          (punta_pulgar.y > base_pulgar.y) and (punta_medio.y > base_medio.y)):
        return "Q"
    
    # Letra G: meñique, anular y medio cerrados; índice y pulgar apuntando hacia arriba
    if (not meñique_ext and not anular_ext and not medio_ext and
        (base_indice.y > punta_indice.y) and (base_pulgar.y > punta_pulgar.y)):
        return "G"

    # Letra Z: solo el índice extendido y apuntando hacia arriba, los demás dedos doblados
    if (indice_ext and not pulgar_ext and not medio_ext and not anular_ext and not meñique_ext and
        (punta_indice.y < base_indice.y)):
        return "Z"

    # Número 7: dedo pulgar y anular cerrados; índice y medio extendidos (símbolo de la paz) y meñique bien estirado
    if (indice_ext and medio_ext and meñique_ext and not pulgar_ext and not anular_ext):
        return "7"


    return "Desconocido"

def check_patron(hand_landmarks, tipo):
    dedos = [hand_landmarks.landmark[i] for i in range(21)]
    # Puntas y bases
    punta_pulgar, base_pulgar = dedos[4], dedos[2]
    punta_indice, base_indice = dedos[8], dedos[5]
    punta_medio, base_medio = dedos[12], dedos[9]
    punta_anular, base_anular = dedos[16], dedos[13]
    punta_meñique, base_meñique = dedos[20], dedos[17]

    # Estados de extensión
    pulgar_ext = abs(punta_pulgar.x - base_pulgar.x) > 0.08 and punta_pulgar.y > base_pulgar.y
    indice_ext = np.linalg.norm([punta_indice.x - base_indice.x, punta_indice.y - base_indice.y]) > 0.08 and punta_indice.y < base_indice.y - 0.02
    medio_ext   = np.linalg.norm([punta_medio.x - base_medio.x, punta_medio.y - base_medio.y])   > 0.08 and punta_medio.y < base_medio.y - 0.02
    anular_ext  = np.linalg.norm([punta_anular.x - base_anular.x, punta_anular.y - base_anular.y])  > 0.08 and punta_anular.y < base_anular.y - 0.02
    menique_ext = np.linalg.norm([punta_meñique.x - base_meñique.x, punta_meñique.y - base_meñique.y]) > 0.08 and punta_meñique.y < base_meñique.y - 0.02

    if tipo == "patron1":
        # Sólo el índice y el medio extendidos, los demás cerrados.
        return indice_ext and medio_ext and (not pulgar_ext) and (not anular_ext) and (not menique_ext)
    elif tipo == "patron2":
        # Índice, anular y meñique extendidos; pulgar y medio cerrados.
        return indice_ext and anular_ext and menique_ext and (not pulgar_ext) and (not medio_ext)
    else:
        return False

def check_all_extended(hand_landmarks):
    dedos = [hand_landmarks.landmark[i] for i in range(21)]
    # Puntas y bases
    punta_pulgar, base_pulgar = dedos[4], dedos[2]
    punta_indice, base_indice = dedos[8], dedos[5]
    punta_medio, base_medio = dedos[12], dedos[9]
    punta_anular, base_anular = dedos[16], dedos[13]
    punta_meñique, base_meñique = dedos[20], dedos[17]
    # Estados de extensión
    pulgar_ext = abs(punta_pulgar.x - base_pulgar.x) > 0.08 and punta_pulgar.y > base_pulgar.y
    indice_ext = np.linalg.norm([punta_indice.x - base_indice.x, punta_indice.y - base_indice.y]) > 0.08 and punta_indice.y < base_indice.y - 0.02
    medio_ext   = np.linalg.norm([punta_medio.x - base_medio.x, punta_medio.y - base_medio.y]) > 0.08 and punta_medio.y < base_medio.y - 0.02
    anular_ext  = np.linalg.norm([punta_anular.x - base_anular.x, punta_anular.y - base_anular.y]) > 0.08 and punta_anular.y < base_anular.y - 0.02
    menique_ext = np.linalg.norm([punta_meñique.x - base_meñique.x, punta_meñique.y - base_meñique.y]) > 0.08 and punta_meñique.y < base_meñique.y - 0.02
    return pulgar_ext and indice_ext and medio_ext and anular_ext and menique_ext

def check_all_closed(hand_landmarks):
    dedos = [hand_landmarks.landmark[i] for i in range(21)]
    # Puntas y bases
    punta_pulgar, base_pulgar = dedos[4], dedos[2]
    punta_indice, base_indice = dedos[8], dedos[5]
    punta_medio, base_medio = dedos[12], dedos[9]
    punta_anular, base_anular = dedos[16], dedos[13]
    punta_meñique, base_meñique = dedos[20], dedos[17]
    # Estados de extensión (usados los mismos thresholds)
    pulgar_ext = abs(punta_pulgar.x - base_pulgar.x) > 0.08 and punta_pulgar.y > base_pulgar.y
    indice_ext = np.linalg.norm([punta_indice.x - base_indice.x, punta_indice.y - base_indice.y]) > 0.08 and punta_indice.y < base_indice.y - 0.02
    medio_ext   = np.linalg.norm([punta_medio.x - base_medio.x, punta_medio.y - base_medio.y]) > 0.08 and punta_medio.y < base_medio.y - 0.02
    anular_ext  = np.linalg.norm([punta_anular.x - base_anular.x, punta_anular.y - base_anular.y]) > 0.08 and punta_anular.y < base_anular.y - 0.02
    menique_ext = np.linalg.norm([punta_meñique.x - base_meñique.x, punta_meñique.y - base_meñique.y]) > 0.08 and punta_meñique.y < base_meñique.y - 0.02
    # Si ningún dedo está extendido se considera cerrado
    return (not pulgar_ext) and (not indice_ext) and (not medio_ext) and (not anular_ext) and (not menique_ext)

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)

    # Dibujar puntos de la mano y reconocer gestos
    if results.multi_hand_landmarks:
        hand_landmarks_list = results.multi_hand_landmarks

        # Si hay dos manos, solo dibujar y diferenciarlas (sin gesto especial)
        if len(hand_landmarks_list) == 2:
            mano1 = hand_landmarks_list[0]
            mano2 = hand_landmarks_list[1]
            x1 = mano1.landmark[0].x
            x2 = mano2.landmark[0].x
            if x1 > x2:
                mano_izq = mano1
                mano_der = mano2
            else:
                mano_izq = mano2
                mano_der = mano1

            mp_drawing.draw_landmarks(frame, mano_izq, mp_hands.HAND_CONNECTIONS)
            mp_drawing.draw_landmarks(frame, mano_der, mp_hands.HAND_CONNECTIONS)

            # --- Condición para detectar "trabajo": ambos puños cerrados (todos los dedos no extendidos) ---
            if check_all_closed(mano_izq) and check_all_closed(mano_der):
                cv2.putText(frame, "Gesto: trabajo", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
            # --- Condición para detectar "55": ambas manos con los 5 dedos estirados ---
            elif check_all_extended(mano_izq) and check_all_extended(mano_der):
                cv2.putText(frame, "Gesto: 55", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
            # Aquí continúan otras condiciones (por ejemplo, para el número 28)
            elif ((check_patron(mano_izq, "patron1") and check_patron(mano_der, "patron2")) or
                  (check_patron(mano_izq, "patron2") and check_patron(mano_der, "patron1"))):
                cv2.putText(frame, "Gesto: 28", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            for hand_landmarks in hand_landmarks_list:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # Identificar el gesto
                gesto_detectado = reconocer_gesto(hand_landmarks, frame)
                # Mostrar el gesto en pantalla
                cv2.putText(frame, f"Gesto: {gesto_detectado}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el video
    cv2.imshow("Reconocimiento de LSM", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()