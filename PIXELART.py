import numpy as np
import cv2 as cv

# Crear imagen blanca con dimensiones específicas
img = np.ones((578, 480, 3), dtype=np.uint8) * 255
cell_size = 32

# Función para pintar una celda en (x, y)
def pintar_celda(x, y, color):
    start_x = x * cell_size
    start_y = y * cell_size
    img[start_y:start_y + cell_size, start_x:start_x + cell_size] = color

# Colores en BGR
rojo     = (0, 0, 255)
azul     = (255, 0, 0)
piel     = (188, 180, 253)
cafe     = (42, 42, 165)
negro    = (0, 0, 0)
amarillo = (0, 255, 255)

# Definir el arte de Mario usando coordenadas (x, y) y colores
pixeles = [
    # Gorro
    *[(x, 0, rojo) for x in range(4, 10)],
    *[(x, 1, rojo) for x in range(3, 13)],
    
    # Cara y oreja
    *[(x, 2, piel) for x in range(6, 9)],
    *[(x, 2, cafe) for x in range(3, 6)],
    *[(9, y, negro) for y in range(2, 4)],
    (10, 2, piel), 
    *[(2, y, cafe) for y in range(3, 6)],
    *[(3, y, piel) for y in range(3, 5)],
    (3, 5, cafe), 
    *[(4, y, cafe) for y in range(3, 5)],
    (4,5, piel),
    *[(x, 3, piel) for x in range(5, 9)],
    (5,4, cafe),
    *[(x, 3, piel) for x in range(10, 13)],
    *[(x, 4, piel) for x in range(6, 10)],
    *[(x, 4, piel) for x in range(10, 14)],
    *[(x, 5, piel) for x in range(5, 9)],
    *[(x, 6, piel) for x in range(4, 12)],

    # Bigote
    (10, 4, negro), 
    *[(x, 5, negro) for x in range(9, 13)],

    # Ropa (camisa roja)
    *[(4, y, rojo) for y in range(7, 10)],
    *[(3, y, rojo) for y in range(7, 10)],
    *[(2, y, rojo) for y in range(8, 10)],
    (1,9, rojo),
    *[(6, y, rojo) for y in range(7, 9)],
    *[(7, y, rojo) for y in range(7, 9)],
    *[(x, 7, rojo) for x in range(8, 10)],
    *[(9, y, rojo) for y in range(8, 10)],
    *[(10, y, rojo) for y in range(8, 11)],
    *[(11, y, rojo) for y in range(8, 10)],
    (12,9, rojo),
    (3,10, rojo),

    # Tirantes azules
    (5, 9, azul), 
    *[(10, y, azul) for y in range(12, 14)],
    *[(9, y, azul) for y in range(10, 14)],
    *[(8, y, azul) for y in range(11, 14)],
    *[(8, y, azul) for y in range(8, 11)],
    *[(5, y, azul) for y in range(7, 9)],
    *[(5, y, azul) for y in range(11, 14)],
    *[(4, y, azul) for y in range(10, 14)],
    *[(3, y, azul) for y in range(12, 14)],
    *[(6, y, azul) for y in range(9, 13)],
    *[(7, y, azul) for y in range(9, 13)],

    # Botones amarillos
    (5, 10, amarillo), (8, 10, amarillo),

    # Manos
    *[(1, y, piel) for y in range(10, 13)],
    *[(2, y, piel) for y in range(10, 13)],
    (3,11, piel),
    (10,11, piel),
    *[(11, y, piel) for y in range(10, 13)],
    *[(12, y, piel) for y in range(10, 13)],
    

    # Zapatos
   *[(x, 14, cafe) for x in range(2, 5)], 
   *[(x, 14, cafe) for x in range(9, 12)], 
   *[(x, 15, cafe) for x in range(1, 5)], 
   *[(x, 15, cafe) for x in range(9, 13)], 
    
]

# Pintar píxeles
for x, y, color in pixeles:
    pintar_celda(x, y, color)

# Dibujar la cuadrícula
for i in range(0, img.shape[0], cell_size):
    cv.line(img, (0, i), (img.shape[1], i), (0, 0, 0), 1)
for j in range(0, img.shape[1], cell_size):
    cv.line(img, (j, 0), (j, img.shape[0]), (0, 0, 0), 1)

# Mostrar resultado
cv.imshow("Mario Pixel Art", img)
cv.waitKey(0)
cv.destroyAllWindows()



