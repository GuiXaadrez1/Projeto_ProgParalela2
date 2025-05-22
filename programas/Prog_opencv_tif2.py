from mpi4py import MPI
import os
import numpy as np
from PIL import Image
import cv2


 
# Inicialização MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Caminho da imagem TIFF
IMAGEM_PATH = r"C:\Projeto_ProgParalela\imagens_satelites\satelit_google1.tif"
Image.MAX_IMAGE_PIXELS = None
# Verifica se o arquivo existe
if rank == 0:
    if not os.path.exists(IMAGEM_PATH):
        raise Exception("Arquivo TIFF não encontrado.")
comm.Barrier()

# Somente o processo 0 carrega a imagem
if rank == 0:
    pil_image = Image.open(IMAGEM_PATH)
    np_image = np.array(pil_image)
else:
    np_image = None

# Broadcast da imagem para todos os processos
np_image = comm.bcast(np_image, root=0)

# Converte para escala de cinza se ainda for colorida
if len(np_image.shape) == 3:
    gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
else:
    gray = np_image

# Divide a imagem por linhas
altura_total = gray.shape[0]
partes = np.array_split(gray, size, axis=0)
parte_local = partes[rank]

# Aplica filtro Canny na parte local
bordas_local = cv2.Canny(parte_local, 60, 255)

# Junta os resultados no processo 0
resultados = comm.gather(bordas_local, root=0)

# Processo 0 junta tudo e salva
if rank == 0:
    imagem_final = np.vstack(resultados)
    cv2.imwrite(r"C:\Projeto_ProgParalela\resultados\grande_bordas.png", imagem_final)
    print("[Processo 0] Resultado final salvo.")
