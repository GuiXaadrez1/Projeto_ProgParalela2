'''

O objetivo aqui é entender o básico de numpy para manipulação de array
toda imagem carregada pela opencv é basicamente um array do numpy

'''


if __name__ == "__main__":

    import cv2
    import numpy as np
    import os

    cm_img = os.path.join(os.getcwd(),"imagens_satelites","imagem6.jpeg")
    
    # lendo uma imagem com cv2
    img = cv2.imread(cm_img)

    # pegando propriedades da tabela
    print(img.shape)

    # Acessa pixel na coordenada (100, 200)
    
    b, g, r = img[100, 200]
    print(f"Pixel (100,200) - B:{b}, G:{g}, R:{r}")

    # Modifica o pixel
    img[100, 200] = [255, 255, 255]  # Branco


    #  Criação de Imagens com NumPy

    # Imagem preta 512x512
    img = np.zeros((512, 512, 3), dtype=np.uint8)

    # Imagem branca
    white_img = np.ones((512, 512, 3), dtype=np.uint8) * 255

    # Círculo azul no centro
    cv2.circle(img, (256, 256), 100, (255, 0, 0), -1)

    # 3. Máscaras e Segmentação

    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # Cria uma máscara circular
    cv2.circle(mask, (150, 150), 100, 255, -1)

    # Aplica a máscara
    result = cv2.bitwise_and(img, img, mask=mask)


    # visuaizando a imagem
    
    #cv2.imshow("Imagem",cv2.cvtColor(white_img, cv2.COLOR_BGR2GRAY))
    cv2.imshow("Segmentacao",result)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()