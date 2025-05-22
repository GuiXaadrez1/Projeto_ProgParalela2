import cv2
import numpy as np

# Carregar imagem
image = cv2.imread( r"C:\Projeto_ProgParalela2\imagens_satelites\imagem6.jpeg")

# Converter para HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir intervalo de cores para estradas (exemplo)
lower = np.array([0, 0, 50])  # Cor mais escura
upper = np.array([180, 50, 200])  # Cor mais clara

# Criar a máscara
mask = cv2.inRange(hsv, lower, upper)

# Aplicar a máscara à imagem
result = cv2.bitwise_and(image, image, mask=mask)

# Exibir a imagem resultante
cv2.imshow('Detected Roads', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
