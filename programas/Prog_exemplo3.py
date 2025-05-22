import cv2
import numpy as np
import matplotlib.pyplot as plt

# Caminho para a imagem de satélite (substitua pelo caminho correto da sua imagem)
image_path = r"C:\Projeto_ProgParalela\imagens_setelites\imagem6.jpeg"

# Carregar a imagem
img = cv2.imread(image_path)

if img is None:
    print("Erro ao carregar a imagem. Verifique o caminho e a integridade do arquivo.")
else:
    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold (limiarização) para identificar áreas que podem ser estradas
    _, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)

    # Mostrar a imagem original e a imagem segmentada
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Imagem Original")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Segmentação com Threshold")
    plt.imshow(thresh, cmap='gray')
    plt.axis('off')

    plt.show()

    # Salvar a imagem segmentada
    cv2.imwrite('estradas_segmentadas.jpg', thresh)

    print("Processamento concluído e imagem com segmentação salva como 'estradas_segmentadas.jpg'.")
