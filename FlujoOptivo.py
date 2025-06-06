import numpy as np 
import cv2 as cv

cap = cv.VideoCapture(0)

lkparm = dict(winSize=(15,15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03)) 

_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

# Definimos los puntos iniciales para formar una malla
p0 = np.array([(x, y) for y in range(100, 500, 100) for x in range(100, 600, 100)])
p0 = np.float32(p0[:, np.newaxis, :])

mask = np.zeros_like(vframe) 

while True:
    _, frame = cap.read()
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm) 

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        p0 = np.array([(x, y) for y in range(100, 500, 100) for x in range(100, 600, 100)])
        p0 = np.float32(p0[:, np.newaxis, :])
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]
        
        # Dibujar la malla
        for i in range(0, len(bp1), 5):  # Conectar puntos en filas
            for j in range(i, i+4):
                if j+1 < len(bp1):
                    a, b = [int(x) for x in bp1[j].ravel()]
                    c, d = [int(x) for x in bp1[j+1].ravel()]
                    frame = cv.line(frame, (a, b), (c, d), (0, 0, 255), 2)

        for i in range(5):  # Conectar puntos en columnas
            for j in range(i, len(bp1), 5):
                if j+5 < len(bp1):
                    a, b = [int(x) for x in bp1[j].ravel()]
                    c, d = [int(x) for x in bp1[j+5].ravel()]
                    frame = cv.line(frame, (a, b), (c, d), (0, 0, 255), 2)

        # Dibujar los puntos
        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a, b = (int(x) for x in nv.ravel())
            c, d = (int(x) for x in vj.ravel())
            frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)

        cv.imshow('ventana', frame)

        vgris = fgris.copy()

        if cv.waitKey(1) & 0xff == 27:
            break

cap.release()
cv.destroyAllWindows()