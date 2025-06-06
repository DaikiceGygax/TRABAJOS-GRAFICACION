import cv2 as cv
import numpy as np

rostro = cv.CascadeClassifier('D:\ESCUELA\GRAFICACION\ejemploGrafi\src\haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)
x=y=w=h= 0 
count = 0
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in rostros:
        #m= int(h/2)
        #n= int(w/2)
        #frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) 

        centro_cachete_izquierdo = (x + int(w / 4), y + int(h / 1.5))
        
        centro_cachete_derecho = (x + int(3 * w / 4), y + int(h / 1.5))
        
        for i in range(5):
            radio = np.random.randint(3, 6) 
            color_peca = (203, 192, 255) 
            cv.circle(frame, 
                      (centro_cachete_izquierdo[0] + np.random.randint(-w//10, w//10), 
                       centro_cachete_izquierdo[1] + np.random.randint(-h//10, h//10)),
                      radio, color_peca, -1) 
            
            # Pecas en el cachete derecho
            cv.circle(frame, 
                      (centro_cachete_derecho[0] + np.random.randint(-w//10, w//10), 
                       centro_cachete_derecho[1] + np.random.randint(-h//10, h//10)),
                      radio, color_peca, -1)
    
    cv.imshow('rostros', frame)
    
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()