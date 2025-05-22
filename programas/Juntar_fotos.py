import cv2
import numpy as np
import os

PASTA_SAIDA = r"C:\Projeto_ProgParalela\resultados_rasterio"

# Número total de processos (ranks)
size = 4  
n_subblocks = 8  # igual do código que gera as imagens

# Lista para guardar as imagens já ordenadas
imagens_todas = []

for rank in range(size):
    pasta_rank = os.path.join(PASTA_SAIDA, f"rank_{rank}")
    # Lista e ordena as imagens do rank pelo índice do bloco
    arquivos = sorted([f for f in os.listdir(pasta_rank) if f.endswith('.png')],
                      key=lambda x: int(x.split('_')[2].split('.')[0]))
    
    for arquivo in arquivos:
        caminho_img = os.path.join(pasta_rank, arquivo)
        img = cv2.imread(caminho_img, cv2.IMREAD_GRAYSCALE)  # Ler em escala de cinza
        imagens_todas.append(img)

# Agora concatena verticalmente (stack de blocos de linhas)
imagem_final = np.vstack(imagens_todas)

# Salvar a imagem final
cv2.imwrite(os.path.join(PASTA_SAIDA, "resultado_final.png"), imagem_final)
print("Imagem final salva em resultado_final.png")
