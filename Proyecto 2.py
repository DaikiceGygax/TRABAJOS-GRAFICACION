import cv2
import mediapipe as mp
import numpy as np
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import threading
import time

# Variables globales para la vista
viewer = [0.0, 1.0, 6.0]        # Posición de la cámara
theta = [0.0, 0.0, 0.0]         # Ángulos de rotación de la escena
orthoflag = False

# Variables globales para control por gestos
hand_control = {
    "move_x": 0.0,
    "move_y": 0.0,
    "zoom": 0.0
}
hand_thread_running = True

# ----- Tracker de Landmarks y Flujo Óptico -----
class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1)
        self.cap = cv2.VideoCapture(0)
        self.prev_gray = None

    def get_landmark_center(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        if results.multi_hand_landmarks:
            # Usamos la muñeca (landmark 0) para controlar la vista
            x = results.multi_hand_landmarks[0].landmark[0].x
            y = results.multi_hand_landmarks[0].landmark[0].y
            return (x, y), frame
        return None, frame

    def get_optical_flow_angle(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_gray is None:
            self.prev_gray = gray
            return 0, 0
        flow = cv2.calcOpticalFlowFarneback(self.prev_gray, gray, None,
                                            0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        avg_ang = np.mean(ang)
        avg_mag = np.mean(mag)
        self.prev_gray = gray
        return avg_mag * np.cos(avg_ang), avg_mag * np.sin(avg_ang)

    def release(self):
        self.cap.release()

tracker = HandTracker()

# ----- Objetos del cuarto -----
def draw_room():
    # Piso
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(-3, 0, -3)
    glVertex3f(3, 0, -3)
    glVertex3f(3, 0, 3)
    glVertex3f(-3, 0, 3)
    glEnd()
    # Paredes
    glColor3f(0.9, 0.9, 1.0)
    # Pared trasera
    glBegin(GL_QUADS)
    glVertex3f(-3, 0, -3)
    glVertex3f(3, 0, -3)
    glVertex3f(3, 2.5, -3)
    glVertex3f(-3, 2.5, -3)
    glEnd()
    # Pared izquierda
    glBegin(GL_QUADS)
    glVertex3f(-3, 0, -3)
    glVertex3f(-3, 0, 3)
    glVertex3f(-3, 2.5, 3)
    glVertex3f(-3, 2.5, -3)
    glEnd()
    # Pared derecha
    glBegin(GL_QUADS)
    glVertex3f(3, 0, -3)
    glVertex3f(3, 0, 3)
    glVertex3f(3, 2.5, 3)
    glVertex3f(3, 2.5, -3)
    glEnd()
    # Techo
    glColor3f(0.95, 0.95, 0.95)
    glBegin(GL_QUADS)
    glVertex3f(-3, 2.5, -3)
    glVertex3f(3, 2.5, -3)
    glVertex3f(3, 2.5, 3)
    glVertex3f(-3, 2.5, 3)
    glEnd()

def draw_bed():
    # Base (cama vertical)
    glColor3f(0.7, 0.5, 0.3)
    glPushMatrix()
    glTranslatef(0.0, 0.25, -1.5)  # Ahora la cama está contra la pared derecha, vertical
    glScalef(2.5, 0.5, 1.5)        # Largo en X, ancho en Z
    glutSolidCube(1)
    glPopMatrix()
    # Cabecera (respaldo, tamaño vertical de la cama)
    glColor3f(0.5, 0.3, 0.2)
    glPushMatrix()
    glTranslatef(0.0, 0.6, -2.2)   # Pegado al extremo de la cama
    glScalef(2.5, 1.2, 0.2)        # Mismo largo que la cama
    glutSolidCube(1)
    glPopMatrix()
    # Colchón
    glColor3f(0.9, 0.9, 0.8)
    glPushMatrix()
    glTranslatef(0.0, 0.6, -1.5)
    glScalef(2.45, 0.2, 1.45)
    glutSolidCube(1)
    glPopMatrix()

def draw_pillows():
    # Almohada 1 (pegada al respaldo, horizontal)
    glColor3f(1.0, 1.0, 0.9)
    glPushMatrix()
    glTranslatef(-0.5, 0.75, -2.0)  # Pegada al respaldo
    glScalef(0.6, 0.15, 0.5)
    glutSolidCube(1)
    glPopMatrix()
    # Almohada 2 (pegada a la anterior, horizontal)
    glColor3f(0.95, 0.95, 0.85)
    glPushMatrix()
    glTranslatef(0.5, 0.75, -2.0)   # Pegada a la anterior
    glScalef(0.6, 0.15, 0.5)
    glutSolidCube(1)
    glPopMatrix()

def draw_wardrobe():
    glColor3f(0.6, 0.4, 0.2)
    glPushMatrix()
    glTranslatef(2.2, 1.1, -2.0)
    glScalef(0.8, 2.2, 1.2)
    glutSolidCube(1)
    glPopMatrix()
    # Puertas
    glColor3f(0.7, 0.5, 0.3)
    glPushMatrix()
    glTranslatef(2.6, 1.1, -2.0)
    glScalef(0.05, 2.1, 1.15)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(1.8, 1.1, -2.0)
    glScalef(0.05, 2.1, 1.15)
    glutSolidCube(1)
    glPopMatrix()

def draw_fan(angle):
    # Eje central
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 2.45, 0)
    glScalef(0.1, 0.1, 0.1)
    glutSolidSphere(1, 16, 16)
    glPopMatrix()
    # Aspas
    glColor3f(0.7, 0.7, 0.7)
    for i in range(4):
        glPushMatrix()
        glTranslatef(0, 2.45, 0)
        glRotatef(angle + i*90, 0, 1, 0)
        glTranslatef(0.7, 0, 0)
        glScalef(1.2, 0.05, 0.2)
        glutSolidCube(1)
        glPopMatrix()

def draw_rug():
    glColor3f(0.7, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0.0, 0.01, 0.0)
    glScalef(2.0, 0.01, 1.2)
    glutSolidCube(1)
    glPopMatrix()

def draw_door():
    glColor3f(0.55, 0.27, 0.07)
    glPushMatrix()
    glTranslatef(2.99, 1.0, -0.5)  # Pared derecha, centrada verticalmente
    glRotatef(90, 0, 1, 0)         # Gira la puerta para que esté en la pared derecha
    glScalef(0.8, 2.0, 0.05)
    glutSolidCube(1)
    glPopMatrix()
    # Manija
    glColor3f(0.9, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(2.95, 1.0, -0.1)  # Ajusta la posición de la manija
    glScalef(0.08, 0.08, 0.08)
    glutSolidSphere(1, 12, 12)
    glPopMatrix()

def draw_toys():
    # Cubo de juguete
    glColor3f(0.2, 0.6, 0.9)
    glPushMatrix()
    glTranslatef(1.0, 0.1, 1.0)
    glScalef(0.2, 0.2, 0.2)
    glutSolidCube(1)
    glPopMatrix()
    # Pelota
    glColor3f(1.0, 0.7, 0.2)
    glPushMatrix()
    glTranslatef(0.5, 0.12, -1.0)
    glutSolidSphere(0.12, 16, 16)
    glPopMatrix()
    # Pirámide (tetraedro)
    glColor3f(0.6, 0.3, 0.8)
    glPushMatrix()
    glTranslatef(-0.8, 0.11, 0.5)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(0.13, 0.22, 4, 1)
    glPopMatrix()
    # Juguete adicional: cubo pequeño
    glColor3f(0.9, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(1.5, 0.1, 1.5)
    glScalef(0.15, 0.15, 0.15)
    glutSolidCube(1)
    glPopMatrix()
    # Juguete adicional: esfera pequeña
    glColor3f(0.3, 0.9, 0.3)
    glPushMatrix()
    glTranslatef(-1.0, 0.12, 1.0)
    glutSolidSphere(0.1, 16, 16)
    glPopMatrix()
    # Juguete adicional: cono
    glColor3f(0.8, 0.2, 0.8)
    glPushMatrix()
    glTranslatef(-1.5, 0.1, 1.5)
    glRotatef(90, 1, 0, 0)
    glutSolidCone(0.1, 0.2, 10, 1)
    glPopMatrix()

def draw_decor():
    # Florero sobre el armario
    glColor3f(0.8, 0.8, 0.95)
    glPushMatrix()
    glTranslatef(2.2, 2.3, -2.0)
    glScalef(0.12, 0.25, 0.12)
    glutSolidSphere(1, 16, 16)
    glPopMatrix()
    # Pelota verde en el piso (antes era planta sobre la cama)
    glColor3f(0.2, 0.7, 0.2)
    glPushMatrix()
    glTranslatef(-1.2, 0.12, 0.8)  # Cerca de la cama, en el piso
    glutSolidSphere(0.12, 16, 16)
    glPopMatrix()

def draw_window():
    # Ventana pegada a la pared izquierda
    glColor3f(0.7, 0.9, 1.0)
    glPushMatrix()
    # Se ubica en x cercano a -3 (pared izquierda) y alejada de las repisas (que usan x=-2.8)
    glTranslatef(-3.0, 1.5, 0.0)
    glScalef(0.05, 1.0, 1.2)
    glutSolidCube(1)
    glPopMatrix()
    # Marco en forma de cruz para la ventana
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(-3.0, 1.5, 0.0)
    # Línea vertical central
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glScalef(0.01, 1.0, 1.2)
    glutSolidCube(1)
    glPopMatrix()
    # Línea horizontal central
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glScalef(0.05, 0.05, 1.2)
    glRotatef(90, 0, 0, 1)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

def draw_desk():
    # Escritorio alejado del tocador: se mueve hacia la derecha para no estar pegado a la cama
    glColor3f(0.7, 0.5, 0.3)
    glPushMatrix()
    glTranslatef(-1.8, 0.45, 0.0)  # Desplazado hacia la derecha (menos negativo)
    glScalef(1.2, 0.1, 0.5)
    glutSolidCube(1)
    glPopMatrix()
    # Patas del escritorio
    for dx in [-0.5, 0.5]:
        for dz in [-0.2, 0.2]:
            glColor3f(0.5, 0.3, 0.2)
            glPushMatrix()
            glTranslatef(-1.8 + dx*0.5, 0.15, 0.0 + dz*0.5)
            glScalef(0.08, 0.6, 0.08)
            glutSolidCube(1)
            glPopMatrix()
    # Libros sobre el escritorio
    glColor3f(0.2, 0.3, 0.8)
    glPushMatrix()
    glTranslatef(-1.9, 0.55, 0.1)
    glScalef(0.18, 0.08, 0.28)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(0.8, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(-1.8, 0.55, 0.1)
    glScalef(0.14, 0.08, 0.22)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(0.2, 0.7, 0.2)
    glPushMatrix()
    glTranslatef(-1.7, 0.55, 0.1)
    glScalef(0.12, 0.08, 0.18)
    glutSolidCube(1)
    glPopMatrix()
    # Lámpara del escritorio
    glColor3f(0.9, 0.9, 0.5)
    glPushMatrix()
    glTranslatef(-1.9, 0.65, -0.15)
    glScalef(0.07, 0.18, 0.07)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(0.8, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(-1.9, 0.77, -0.15)
    glutSolidSphere(0.07, 12, 12)
    glPopMatrix()
    # Lapiceros
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(-2.05, 0.6, -0.15)
    glScalef(0.03, 0.12, 0.03)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(0.8, 0.4, 0.1)
    glPushMatrix()
    glTranslatef(-2.0, 0.6, -0.15)
    glScalef(0.03, 0.12, 0.03)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(0.1, 0.4, 0.8)
    glPushMatrix()
    glTranslatef(-1.95, 0.6, -0.15)
    glScalef(0.03, 0.12, 0.03)
    glutSolidCube(1)
    glPopMatrix()
    # Silla:
    # Asiento
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(-1.8, 0.22, -0.5)
    glScalef(0.5, 0.08, 0.5)
    glutSolidCube(1)
    glPopMatrix()
    # Patas de la silla
    for dx in [-0.18, 0.18]:
        for dz in [-0.18, 0.18]:
            glColor3f(0.2, 0.2, 0.2)
            glPushMatrix()
            glTranslatef(-1.8 + dx, 0.08, -0.5 + dz)
            glScalef(0.05, 0.16, 0.05)
            glutSolidCube(1)
            glPopMatrix()
    # Respaldo de la silla
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(-1.8, 0.38, -0.68)
    glScalef(0.5, 0.25, 0.08)
    glutSolidCube(1)
    glPopMatrix()

def draw_shelves():
    # Repisas en la pared izquierda, alejadas de la ventana
    glColor3f(0.6, 0.4, 0.2)
    # Primera repisa
    glPushMatrix()
    glTranslatef(-2.8, 1.8, 1.0)  # Se mueve más a la izquierda que antes
    glScalef(0.1, 0.05, 1.5)
    glutSolidCube(1)
    glPopMatrix()
    # Segunda repisa
    glPushMatrix()
    glTranslatef(-2.8, 1.3, 1.0)
    glScalef(0.1, 0.05, 1.5)
    glutSolidCube(1)
    glPopMatrix()
    # Objetos sobre la repisa: un libro y una planta, colocados encima (sin atravesarlas)
    glColor3f(0.2, 0.2, 0.8)  # Libro
    glPushMatrix()
    glTranslatef(-2.8, 1.92, 1.2)  # Aumentamos la altura para que quede sobre la repisa
    glScalef(0.1, 0.2, 0.1)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(0.0, 0.8, 0.0)  # Planta
    glPushMatrix()
    glTranslatef(-2.8, 1.92, 0.8)
    glScalef(0.15, 0.2, 0.15)
    glutSolidCube(1)
    glPopMatrix()

def draw_dresser():
    # Tocador (dressing) en el lado opuesto al armario, en la pared izquierda (del otro lado de la cama)
    glColor3f(0.7, 0.5, 0.3)
    glPushMatrix()
    glTranslatef(-2.0, 0.3, -1.5)  # Se mueve más a la izquierda para separarlo de la cama
    glScalef(1.0, 0.5, 0.6)
    glutSolidCube(1)
    glPopMatrix()
    # Lámpara sobre el tocador
    glColor3f(1.0, 1.0, 0.5)
    glPushMatrix()
    glTranslatef(-2.0, 1.0, -1.2)  # Posición de la lámpara sobre el tocador
    glScalef(0.2, 0.3, 0.2)
    glutSolidCube(1)
    glPopMatrix()
    # Soporte para la lámpara (un "palito" que la sujeta)
    glColor3f(0.8, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(-2.0, 0.8, -1.2)  # Debajo de la lámpara
    glScalef(0.05, 0.2, 0.05)
    glutSolidCube(1)
    glPopMatrix()

def draw_painting():
    # Marco del cuadro en la pared trasera, sobre la cama pero sin tocar el techo
    glColor3f(0.4, 0.2, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 2.0, -2.9)  # Marco del cuadro
    glScalef(1.2, 0.8, 0.05)
    glutSolidCube(1)
    glPopMatrix()
    # Fotito: parte superior azul
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 2.1, -2.84)  # Posicionado dentro del marco
    glScalef(1.0, 0.38, 0.01)
    glutSolidCube(1)
    glPopMatrix()
    # Fotito: parte inferior, pastito verde
    glColor3f(0.0, 0.8, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 1.9, -2.84)  # Debajo de la parte azul, dentro del marco
    glScalef(1.0, 0.38, 0.01)
    glutSolidCube(1)
    glPopMatrix()

# ----- Callbacks de OpenGL -----
fan_angle = 0
def display():
    global fan_angle
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2], 0, 1, 0, 0, 1, 0)
    glRotatef(theta[0], 1, 0, 0)
    glRotatef(theta[1], 0, 1, 0)
    glRotatef(theta[2], 0, 0, 1)
    draw_room()
    draw_bed()
    draw_pillows()
    draw_wardrobe()
    draw_fan(fan_angle)
    draw_rug()
    draw_door()
    draw_toys()
    draw_decor()
    draw_window()
    draw_desk()
    # Nuevos elementos decorativos:
    draw_shelves()
    draw_dresser()
    draw_painting()
    glutSwapBuffers()

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def update(value):
    global fan_angle, viewer
    fan_angle = (fan_angle + 5) % 360

    # --- Control por gestos de la mano ---
    viewer[0] += hand_control["move_x"] * 0.1
    viewer[1] -= hand_control["move_y"] * 0.1
    if hand_control["zoom"] == 1:
        viewer[2] -= 0.15  # Zoom in
    elif hand_control["zoom"] == -1:
        viewer[2] += 0.15  # Zoom out

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)

def special_keys(key, x, y):
    global viewer
    if key == GLUT_KEY_UP:
        viewer[1] += 0.1
    elif key == GLUT_KEY_DOWN:
        viewer[1] -= 0.1
    elif key == GLUT_KEY_LEFT:
        viewer[0] -= 0.1
    elif key == GLUT_KEY_RIGHT:
        viewer[0] += 0.1
    glutPostRedisplay()

def init_glut():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 700)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Proyecto 2 - Ricardo Mendoza Tello")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(special_keys)
    glutTimerFunc(30, update, 0)
    glutMainLoop()

def hand_gesture_thread():
    global hand_control, hand_thread_running, tracker, viewer
    last_x, last_y = None, None
    zoom_state = 0  # 1: zoom in, -1: zoom out, 0: nada
    while hand_thread_running:
        result, frame = tracker.cap.read()
        if not result:
            time.sleep(0.05)
            continue
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = tracker.hands.process(rgb)
        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0].landmark
            # Centro de la palma (landmarks 0, 5, 9, 13, 17)
            palm_x = np.mean([lm[i].x for i in [0, 5, 9, 13, 17]])
            palm_y = np.mean([lm[i].y for i in [0, 5, 9, 13, 17]])
            # Movimiento relativo
            if last_x is not None and last_y is not None:
                dx = palm_x - last_x
                dy = palm_y - last_y
                # Sensibilidad ajustable
                hand_control["move_x"] = -dx * 10
                hand_control["move_y"] = dy * 10
            last_x, last_y = palm_x, palm_y

                    
            # Nueva detección de zoom:
            # Zoom in: juntar pulgar (4) y dedo medio (12)
            # Zoom out: juntar pulgar (4) y dedo anular (16)
            dist_thumb_middle = np.sqrt((lm[4].x - lm[12].x)**2 + (lm[4].y - lm[12].y)**2)
            dist_thumb_ring = np.sqrt((lm[4].x - lm[16].x)**2 + (lm[4].y - lm[16].y)**2)
            if dist_thumb_middle < 0.07:
                hand_control["zoom"] = 1  # Zoom in
            elif dist_thumb_ring < 0.07:
                hand_control["zoom"] = -1  # Zoom out
            else:
                hand_control["zoom"] = 0
        else:
            hand_control["move_x"] = 0.0
            hand_control["move_y"] = 0.0
            hand_control["zoom"] = 0.0
            last_x, last_y = None, None
        time.sleep(0.05)

if __name__ == "__main__":
    hand_thread = threading.Thread(target=hand_gesture_thread, daemon=True)
    hand_thread.start()
    try:
        init_glut()
    except KeyboardInterrupt:
        hand_thread_running = False
        tracker.release()
        sys.exit()
