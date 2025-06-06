import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluSphere
import sys

# Variables globales para la cámara
camera_pos = [4.0, 3.0, 8.0]  # Posición de la cámara
camera_target = [0.0, 1.0, 0.0]  # Punto al que mira
camera_up = [0.0, 1.0, 0.0]  # Vector hacia arriba

# Variables para el movimiento
camera_speed = 0.2  # Velocidad de movimiento
keys = {}  # Diccionario para controlar el estado de las teclas


def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)


def draw_tree(x, z):
    """Dibuja un árbol en la posición especificada"""
    # Tronco
    glPushMatrix()
    glColor3f(0.4, 0.2, 0.0)
    glTranslatef(x, 1, z)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 0.2)
    gluCylinder(gluNewQuadric(), 0.5, 0.5, 4, 40, 10)
    glPopMatrix()
    
    # Copa principal del árbol (esfera verde)
    glPushMatrix()
    glColor3f(0.0, 0.5, 0.0)
    glTranslatef(x, 1.5, z)
    gluSphere(gluNewQuadric(), 0.8, 20, 20)
    glPopMatrix()
    
    # Follaje adicional: esfera a la izquierda
    glPushMatrix()
    glColor3f(0.0, 0.55, 0.0)
    glTranslatef(x - 0.6, 1.7, z)
    gluSphere(gluNewQuadric(), 0.5, 20, 20)
    glPopMatrix()
    
    # Follaje adicional: esfera al frente-derecha
    glPushMatrix()
    glColor3f(0.0, 0.55, 0.0)
    glTranslatef(x + 0.5, 1.4, z + 0.4)
    gluSphere(gluNewQuadric(), 0.4, 20, 20)
    glPopMatrix()


def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para el suelo
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()


def draw_scene():
    """Dibuja la escena completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],  # Posición de la cámara
              camera_target[0], camera_target[1], camera_target[2],  # Punto al que mira
              camera_up[0], camera_up[1], camera_up[2])  # Vector hacia arriba

    draw_ground()  # Dibuja el suelo
    draw_tree(0,0)  # Dibuja el tronco

    glfw.swap_buffers(window)


def process_input():
    """Procesa el estado de las teclas para mover la cámara"""
    global camera_pos

    if keys.get(glfw.KEY_W, False):  # Mover hacia adelante
        camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S, False):  # Mover hacia atrás
        camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A, False):  # Mover a la izquierda
        camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D, False):  # Mover a la derecha
        camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP, False):  # Subir
        camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN, False):  # Bajar
        camera_pos[1] -= camera_speed


def key_callback(window, key, scancode, action, mods):
    """Actualiza el estado de las teclas"""
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Mover Escena Completa", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Configurar callback de teclado
    glfw.set_key_callback(window, key_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        process_input()  # Procesar teclas presionadas
        draw_scene()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()