# esse é um código opecv com suport a tif como exemplo

from mpi4py import MPI
import os
import cv2
import numpy as np

# Inicialização MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Diretórios (caminhos absolutos)
PASTA_IMAGENS = r"C:\Projeto_ProgParalela\imagens_satelites"
PASTA_RESULTADOS = r"C:\Projeto_ProgParalela\resultados"

# Cria pasta de resultados (apenas processo 0)
if rank == 0:
    if not os.path.exists(PASTA_RESULTADOS):
        os.makedirs(PASTA_RESULTADOS)
comm.Barrier()  # Espera a criação da pasta

# Lista de imagens (apenas processo 0)
if rank == 0:
    arquivos = sorted([
        f for f in os.listdir(PASTA_IMAGENS)
        #if f.lower().endswith((".jpg", ".jpeg"))
        if f.lower().endswith((".jpg", ".jpeg", ".tif", ".tiff"))  # Suporte estendido
    ])
else:
    arquivos = None

# Distribui lista para todos os processos
arquivos = comm.bcast(arquivos, root=0)

# Divide a lista entre os processos
lista_local = np.array_split(arquivos, size)[rank]

# Função que aplica filtro e salva resultado
def processar_imagem(nome_arquivo):
    caminho_entrada = os.path.join(PASTA_IMAGENS, nome_arquivo)
    
    img = cv2.imread(caminho_entrada, cv2.IMREAD_COLOR)
    if img is None:
        print(f"[Processo {rank}] Falha ao carregar: {nome_arquivo}")
        return
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold para segmentação simples
   # _, bordas = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)

    # Alternativamente, pode usar Canny (basta descomentar)
    bordas = cv2.Canny(gray, 60, 255)

    # Gerar nome do arquivo de saída
    nome_saida = os.path.splitext(nome_arquivo)[0] + "_bordas.png"
    caminho_saida = os.path.join(PASTA_RESULTADOS, nome_saida)
    cv2.imwrite(caminho_saida, bordas)

    print(f"[Processo {rank}] Processou: {nome_arquivo}")

# Processa as imagens atribuídas a este processo
for arquivo in lista_local:
    processar_imagem(arquivo)

print(f"[Processo {rank}] Finalizou {len(lista_local)} imagens.")
