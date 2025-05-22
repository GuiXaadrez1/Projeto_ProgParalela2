import cv2
import numpy as np
import matplotlib.pyplot as plt
import os 

# Carregar a imagem de satélite (substitua pelo caminho da sua imagem)
#image_path = os.path.join(os.getcwd(),'imagens_satelites','imagem1.jpg')  # Caminho para sua imagem

image_path = r"C:\Projeto_ProgParalela\imagens_satelites\imagem1.jpg"

print(image_path)

img = cv2.imread(image_path)

# Converter para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar o filtro de bordas Canny
#edges = cv2.Canny(gray, 100, 200)

# Aplicar threshold (limiarização) para identificar áreas que podem ser estradas
_, edges = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)

# Mostrar a imagem original e a detecção de bordas
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Imagem Original")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Detecção de Bordas (Canny)")
plt.imshow(edges, cmap='gray')
plt.axis('off')

plt.show()

# Salvar a imagem com as bordas detectadas
cv2.imwrite('estradas_detectadas.jpg', edges)

print("Processamento concluído e imagem com bordas salva como 'estradas_detectadas.jpg'.")
