from mpi4py import MPI
import numpy as np
import cv2
import os
import rasterio

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

IMAGEM_PATH = r"C:\Projeto_ProgParalela\imagens_satelites\satelit_google1.tif"
PASTA_SAIDA = r"C:\Projeto_ProgParalela\resultados_rasterio"

# Cria pasta para salvar resultados do processo atual
saida_processo = os.path.join(PASTA_SAIDA, f"rank_{rank}")
os.makedirs(saida_processo, exist_ok=True)

# Cada processo abre o dataset para evitar concorrência
with rasterio.open(IMAGEM_PATH) as src:
    altura = src.height
    largura = src.width
    canais = src.count

    n_subblocks = 8  # Aumentei para 8 para blocos menores, ajuste conforme memória
    blocos = np.array_split(np.arange(altura), size * n_subblocks)

    # Filtra blocos correspondentes ao rank do processo
    blocos_rank = [bloco for i, bloco in enumerate(blocos) if i % size == rank]

    for idx, bloco in enumerate(blocos_rank):
        linha_ini = bloco[0]
        linha_fim = bloco[-1] + 1
        altura_local = linha_fim - linha_ini

        print(f"[Processo {rank}] Processando linhas de {linha_ini} até {linha_fim} (bloco {idx})")

        window = rasterio.windows.Window(col_off=0, row_off=linha_ini, width=largura, height=altura_local)

        try:
            dados = src.read(window=window)  # (canais, altura_local, largura)
        except Exception as e:
            print(f"[Processo {rank}] Erro ao ler janela {linha_ini}:{linha_fim} - {e}")
            continue

        if canais >= 3:
            img_rgb = dados[:3].transpose(1, 2, 0)  # (altura_local, largura, 3)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        else:
            img_gray = dados[0]

        bordas = cv2.Canny(img_gray, 60, 255)

        nome_arquivo = os.path.join(saida_processo, f"bordas_{rank}_{idx}.png")
        cv2.imwrite(nome_arquivo, bordas)

        print(f"[Processo {rank}] Janela {idx} finalizada. Salvo em {nome_arquivo}")

print(f"[Processo {rank}] Todos blocos processados.")
