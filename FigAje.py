import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

camera_pos = [6.0, 4.0, 15.0]
camera_target = [0.0, 1.0, 0.0]
camera_up = [0.0, 1.0, 0.0]
camera_speed = 0.2
keys = {}

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_cylinder(base, top, height):
    quadric = gluNewQuadric()
    gluCylinder(quadric, base, top, height, 32, 32)

def draw_sphere(radius):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)

def draw_rook():
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)  # Hace que el cilindro quede vertical
    draw_cylinder(0.4, 0.4, 1.0)
    glTranslatef(0, 0, 1.0)
    draw_sphere(0.4)
    glPopMatrix()

def draw_knight():
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.4, 0.4, 1)
    glTranslatef(0, 0, 1)
    glRotatef(45, 0, 1, 0)
    draw_cylinder(0.25, 0.1, 0.6)
    glPopMatrix()

def draw_bishop():
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.4, 0.4, 1.0)
    glTranslatef(0, 0, 1.0)
    draw_sphere(0.35)
    glTranslatef(0, 0, 0.4)
    draw_sphere(0.1)
    glPopMatrix()

def draw_queen():
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.4, 0.4, 1.0)
    glTranslatef(0, 0, 1.0)
    draw_sphere(0.4)
    glTranslatef(0, 0, 0.45)
    draw_sphere(0.15)
    glPopMatrix()

def draw_king():
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.4, 0.4, 1.0)
    glTranslatef(0, 0, 1.0)
    draw_sphere(0.4)
    glTranslatef(0, 0, 0.45)
    draw_cylinder(0.08, 0.08, 0.25)
    glTranslatef(0, 0, 0.25)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.02, 0.02, 0.15)
    glPopMatrix()
    draw_cylinder(0.02, 0.02, 0.15)
    glPopMatrix()

def draw_pawn():
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.3, 0.3, 0.8)
    glTranslatef(0, 0, 0.8)
    draw_sphere(0.3)
    glPopMatrix()

def draw_ground():
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(*camera_pos, *camera_target, *camera_up)

    draw_ground()

    glColor3f(0.0, 0.0, 1.0)
    # Dibuja cada figura individualmente, alineadas y de pie
    # Orden: Peón, Reina, Rey, Alfil, Caballo, Torre
    glPushMatrix()
    glTranslatef(-6.0, 1.0, 0.0)
    draw_pawn()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-4.5, 1.0, 0.0)
    draw_queen()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-3.0, 1.0, 0.0)
    draw_king()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.5, 1.0, 0.0)
    draw_bishop()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 1.0, 0.0)
    draw_knight()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.5, 1.0, 0.0)
    draw_rook()
    glPopMatrix()

    glfw.swap_buffers(window)

def process_input():
    global camera_pos
    if keys.get(glfw.KEY_W): camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S): camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A): camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D): camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP): camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN): camera_pos[1] -= camera_speed

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS: keys[key] = True
    elif action == glfw.RELEASE: keys[key] = False

def main():
    global window
    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Piezas de Ajedrez con Primitivas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        process_input()
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
