from mpi4py import MPI
import numpy as np
import tifffile as tiff
import cv2
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

IMAGEM_PATH = r"C:\Projeto_ProgParalela\imagens_satelites\satelit_google1.tif"
PASTA_RESULTADOS = r"C:\Projeto_ProgParalela\resultados_blocos"

if rank == 0:
    print("Processo 0: carregando imagem completa...")
    imagem = tiff.imread(IMAGEM_PATH)  # Carrega tudo
    altura, largura = imagem.shape[:2]
    canais = imagem.shape[2] if len(imagem.shape) == 3 else 1
else:
    imagem = None
    altura = largura = canais = 0

# Distribui as dimensões para todos
altura = comm.bcast(altura, root=0)
largura = comm.bcast(largura, root=0)
canais = comm.bcast(canais, root=0)

# Cada processo calcula qual fatia de linhas vai receber
linhas = np.array_split(np.arange(altura), size)
inicio = linhas[rank][0]
fim = linhas[rank][-1] + 1
qtd_linhas = fim - inicio

# Envio da fatia do processo 0 para os demais
if rank == 0:
    for i in range(1, size):
        fatia_i = imagem[linhas[i][0]:linhas[i][-1]+1]
        comm.send(fatia_i, dest=i, tag=11)
    minha_fatia = imagem[inicio:fim]
else:
    minha_fatia = comm.recv(source=0, tag=11)

# Cria pasta de saída
saida = os.path.join(PASTA_RESULTADOS, f"rank_{rank}")
os.makedirs(saida, exist_ok=True)

# Converte para tons de cinza se necessário
if len(minha_fatia.shape) == 3 and minha_fatia.shape[2] >= 3:
    minha_fatia = minha_fatia[:, :, :3]
    gray = cv2.cvtColor(minha_fatia, cv2.COLOR_RGB2GRAY)
else:
    gray = minha_fatia

# Aplica Canny
bordas = cv2.Canny(gray, 60, 255)

# Salva imagem de saída
saida_img = os.path.join(saida, f"bordas_rank{rank}.png")
cv2.imwrite(saida_img, bordas)

print(f"[Processo {rank}] Processou linhas {inicio} a {fim}.")
