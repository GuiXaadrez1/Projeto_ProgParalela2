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
comm.Barrier()  # Espera pasta criada

# Lista de imagens (apenas processo 0)
if rank == 0:
    arquivos = sorted([
        f for f in os.listdir(PASTA_IMAGENS)
        if f.lower().endswith((".jpg", ".jpeg"))
    ])
else:
    arquivos = None

# Distribui lista para todos
arquivos = comm.bcast(arquivos, root=0)

# Divide lista entre processos
lista_local = np.array_split(arquivos, size)[rank]

# Função simples que aplica filtro Canny e salva resultado
def processar_imagem(nome_arquivo):
    caminho_entrada = os.path.join(PASTA_IMAGENS, nome_arquivo)
    caminho_saida = os.path.join(PASTA_RESULTADOS, nome_arquivo)

    img = cv2.imread(caminho_entrada, cv2.IMREAD_COLOR)
    if img is None:
        print(f"[Processo {rank}] Falha ao carregar: {nome_arquivo}")
        return
    
    # Converter para cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold (limiarização) para identificar áreas que podem ser estradas
    _, bordas = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)

    # Aplica filtro Canny (detecta bordas)
    #bordas = cv2.Canny(gray, 125, 200)

    # Salva resultado (bordas em PNG)
    nome_saida = os.path.splitext(nome_arquivo)[0] + "_bordas.png"
    caminho_saida = os.path.join(PASTA_RESULTADOS, nome_saida)
    cv2.imwrite(caminho_saida, bordas)

    print(f"[Processo {rank}] Processou: {nome_arquivo}")

# Processa as imagens da lista local
for arquivo in lista_local:
    processar_imagem(arquivo)

print(f"[Processo {rank}] Finalizou {len(lista_local)} imagens.")
