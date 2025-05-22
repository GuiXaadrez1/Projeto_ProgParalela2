# detecta_estradas_mpi.py

from mpi4py import MPI
import os
import numpy as np
import cv2
import tensorflow as tf

# ===========================
# 1. Inicialização do MPI
# ===========================

comm = MPI.COMM_WORLD      # Objeto de comunicação
rank = comm.Get_rank()     # ID do processo atual
size = comm.Get_size()     # Número total de processos

# ===========================
# 2. Configuração de caminhos
# ===========================

PASTA_IMAGENS = os.path.join(os.getcwd(),"imagens_satelites")
print(os.path.abspath(PASTA_IMAGENS))

PASTA_RESULTADOS = r"C:\Projeto_ProgParalela"

CAMINHO_MODELO = os.path.join(PASTA_IMAGENS, "imagem1.jpg")

# ===========================
# 3. Função: carregar modelo
# ===========================

def carregar_modelo():
    """Carrega o modelo treinado para detectar estradas"""
    print(f"[Processo {rank}] Carregando modelo...")
    return tf.keras.models.load_model(CAMINHO_MODELO)

# ===========================
# 4. Função: processar imagem
# ===========================

def processar_imagem(caminho_imagem, modelo):
    """
    Executa a detecção de estrada em uma imagem e salva o resultado como máscara.
    """
    try:
        # Carrega a imagem com OpenCV
        img = cv2.imread(caminho_imagem)
        if img is None:
            print(f"[Processo {rank}] Falha ao ler imagem: {caminho_imagem}")
            return

        # Redimensiona a imagem para o tamanho de entrada do modelo
        img_resized = cv2.resize(img, (256, 256))
        input_tensor = np.expand_dims(img_resized / 255.0, axis=0)

        # Inferência com o modelo
        pred = modelo.predict(input_tensor, verbose=0)[0]

        # Criação da máscara binária (thresholding)
        mask = (pred > 0.5).astype(np.uint8) * 255

        # Gera nome do arquivo de saída
        nome_saida = os.path.basename(caminho_imagem).replace(".tif", "_mascara.png")
        caminho_saida = os.path.join(PASTA_RESULTADOS, nome_saida)

        # Salva a máscara como imagem
        cv2.imwrite(caminho_saida, mask)
        print(f"[Processo {rank}] Processou: {caminho_imagem}")

    except Exception as e:
        print(f"[Processo {rank}] Erro ao processar {caminho_imagem}: {e}")

# ===========================
# 5. Preparar lista de imagens
# ===========================

'''
if rank == 0:
    # Processo 0 lista todos os arquivos .tif na pasta de imagens
    all_images = sorted([
        os.path.join(PASTA_IMAGENS, f)
        for f in os.listdir(PASTA_IMAGENS)
        if f.lower().endswith(".jpg")
    ])
else:
    all_images = None
'''


if rank == 0:
    # Processo 0 lista todos os arquivos .tif na pasta de imagens
    all_images = sorted([
        os.path.join(PASTA_IMAGENS, f)
        for f in os.listdir(PASTA_IMAGENS)
        if f.lower().endswith(".jpg")
    ])
else:
    all_images = None


# Broadcast: envia a lista para todos os processos
all_images = comm.bcast(all_images, root=0)

# Divide as imagens igualmente entre os processos
imagens_do_processo = np.array_split(all_images, size)[rank]

# ===========================
# 6. Preparar pasta de saída
# ===========================

if rank == 0:
    if not os.path.exists(PASTA_RESULTADOS):
        os.makedirs(PASTA_RESULTADOS)
comm.Barrier()  # Aguarda todos os processos

# ===========================
# 7. Processar imagens
# ===========================

modelo = carregar_modelo()

for caminho_img in imagens_do_processo:
    processar_imagem(caminho_img, modelo)

print(f"[Processo {rank}] Finalizou {len(imagens_do_processo)} imagens.")
