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

with rasterio.open(IMAGEM_PATH) as src:
    altura = src.height
    largura = src.width
    canais = src.count

    n_subblocks = 8
    blocos = np.array_split(np.arange(altura), size * n_subblocks)
    blocos_rank = [bloco for i, bloco in enumerate(blocos) if i % size == rank]

    for idx, bloco in enumerate(blocos_rank):
        linha_ini = bloco[0]
        linha_fim = bloco[-1] + 1
        altura_local = linha_fim - linha_ini

        print(f"[Processo {rank}] Processando linhas de {linha_ini} até {linha_fim} (bloco {idx})")

        window = rasterio.windows.Window(col_off=0, row_off=linha_ini, width=largura, height=altura_local)

        try:
            dados = src.read(window=window)
        except Exception as e:
            print(f"[Processo {rank}] Erro ao ler janela {linha_ini}:{linha_fim} - {e}")
            continue

        if canais >= 3:
            img_rgb = dados[:3].transpose(1, 2, 0)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        else:
            img_gray = dados[0]

        # Aplicar threshold (limiarização) para identificar áreas que podem ser estradas
        _, bordas = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY)

        nome_arquivo = os.path.join(saida_processo, f"bordas_{rank}_{idx}.png")
        cv2.imwrite(nome_arquivo, bordas)

        print(f"[Processo {rank}] Janela {idx} finalizada. Salvo em {nome_arquivo}")

print(f"[Processo {rank}] Todos blocos processados.")
