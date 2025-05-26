
'''

    BAICAMENTE VAMOS APRENDER O BÁSICO DE RASTERIO PARA PROCESSARMOS AS IMAGENS COM A FINALIDADE DE
    REALIZARMOS SEGUIMENTAÇÕES EM ESTRADAS NAS IMAGENS DE SATÉLITES

'''

import rasterio
import numpy
import matplotlib.pyplot as plt
import os

import rasterio.crs
import rasterio.transform 

cm_img = os.path.join(os.getcwd(),"imagens_satelites","img_satelite.tif")
print(cm_img)


# Abrindo um arquivo.tif com rasterio
with rasterio.open(cm_img) as src:
    
    print("\nDimensão: ", src.shape) # retorna em tupla a altura da imagem e a largura da imagem

    for i,item in enumerate(src.shape):
        if i == 0:
            print(f"index {i} -> Altura da imagem: {item}")
        else:
            print(f"index {i} -> Largura da imagem: {item}")

    print("\nBandas: ", src.count)


    print("\nProjeção: ", src.crs)
    print("\nTransformação:\n",src.transform)
    print("\nFormato: ", src.driver)
    print("\nAltura: ", src.height)
    print("\nLargura: ", src.width)
    
    print("\nLendo uma banda da imagem, vai retornar um array numpy")
    banda1 = src.read(1)
    print(banda1)


'''
amostra = banda1[:10000, :10000]  # Exibe só um bloco 1000x1000 pixels
plt.imshow(amostra, cmap='gray')
plt.title('Amostra da Banda 1')
plt.colorbar()
plt.show()
'''


