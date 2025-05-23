'''

O objetivo é entender o básico dessa lib para irmos evoluindo

'''

import cv2
import os  


cm_img = os.path.join(os.getcwd(),"imagens_satelites","imagem6.jpeg")
print(cm_img)

# lendo a imagem com o padrão de cor BGR
img = cv2.imread(cm_img)


print(f'propriedades de imagem BGR: {img.shape}')

# Convertendo o espaço de cor da imagem

img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # de BGR para RGB
img_gray = cv2.cvtColor(img_rgb,cv2.COLOR_RGB2GRAY) # RGB para GRAY
img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR) # GRAY para  BGR
img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) # BGR para HSV
img_bgr2 = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR) # HSV para BGR, voltamos ao padrão


# adiquirindo a propriedade da imagem cinza
print(f'Propriedades da imagem cinza: {img_gray.shape}')

# colocando  uma linha vermelha
cv2.line(img_bgr2, (50, 50), (450, 50), (0, 0, 255), 2)  # Vermelha

# colocando uma anotação na imagem
cv2.putText(img_bgr2, "OpenCV.........", (180, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)


cv2.imshow("imagem",img_bgr2)
cv2.waitKey(0)
cv2.destroyAllWindows()