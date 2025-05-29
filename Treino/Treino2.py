import rasterio
from mpi4py import MPI
import cv2
import os
import time
import numpy as np


# VERSÃO 2, TENTADO MELHORAR O CONSUMO DE MEMÓRIA MAS NÃO DEU

def informacoes(caminho_tif):
    with rasterio.open(caminho_tif) as raster:
        corpo = raster.shape
        formato = raster.driver
        banda = raster.count
        altura = raster.height
        largura = raster.width
        return corpo, formato, banda, altura, largura


def processar_linhas_img(img_largura, banda_img, caminho_tif, altura_total, pasta_blocos):
    resultados = []
    total_blocos = 64
    linhas_por_bloco = altura_total // total_blocos
    resto = altura_total % total_blocos

    with rasterio.open(caminho_tif) as raster:
        for bloco_id in range(total_blocos):
            if bloco_id % size != rank:
                continue

            inicio = bloco_id * linhas_por_bloco
            fim = inicio + linhas_por_bloco
            if bloco_id == total_blocos - 1:
                fim += resto

            altura_local = fim - inicio

            print(f"[Rank {rank}] Processando linhas {inicio} a {fim} (bloco {bloco_id})")

            window = rasterio.windows.Window(col_off=0, row_off=inicio, width=img_largura, height=altura_local)

            try:
                dados = raster.read([1, 2,3] if banda_img >= 3 else [1], window=window)
            except Exception as e:
                print(f"[Rank {rank}] Erro ao ler bloco {bloco_id}: {e}")
                continue

            if banda_img >= 3:
                img_rgb = dados[:3].transpose(1, 2, 0)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            else:
                img_gray = dados[0]

            _, bordas = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

            nome_bloco = f"bloco_{bloco_id:03d}.png"
            caminho_bloco = os.path.join(pasta_blocos, nome_bloco)
            cv2.imwrite(caminho_bloco, bordas)
            print(f"[Rank {rank}] Bloco {bloco_id} salvo em {caminho_bloco}")

            if rank == 0:
                resultados.append((bloco_id, caminho_bloco))
            else:
                comm.send((bloco_id, caminho_bloco), dest=0, tag=bloco_id)

    if rank == 0:
        for src_rank in range(1, size):
            for bloco_id in range(total_blocos):
                if bloco_id % size != src_rank:
                    continue
                bloco_info = comm.recv(source=src_rank, tag=bloco_id)
                resultados.append(bloco_info)

        resultados.sort(key=lambda x: x[0])
        return resultados

    return None


def juntar_blocos_em_imagem_final(lista_blocos, caminho_saida_final):
    imagens = []

    for _, caminho_img in lista_blocos:
        img = cv2.imread(caminho_img, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"[ERRO] Não foi possível carregar {caminho_img}")
            continue
        imagens.append(img)

    imagem_final = np.vstack(imagens)
    cv2.imwrite(caminho_saida_final, imagem_final)
    print(f"[Rank 0] Imagem final salva em: {caminho_saida_final}")


if __name__ == "__main__":
    tempo_inicio = time.time()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    caminho_tif = os.path.join(os.getcwd(), "imagens_satelites", "img_satelite2.tif")
    caminho_saida = os.path.join(os.getcwd(), "imagens_processadas", "imagem_final_blocos.png")

    pasta_blocos = os.path.join(os.getcwd(), "blocos_tmp")
    os.makedirs(pasta_blocos, exist_ok=True)

    inform = informacoes(caminho_tif=caminho_tif)

    blocos_salvos = processar_linhas_img(
        img_largura=inform[4],
        banda_img=inform[2],
        caminho_tif=caminho_tif,
        altura_total=inform[3],
        pasta_blocos=pasta_blocos
    )

    if rank == 0:
        if blocos_salvos:
            juntar_blocos_em_imagem_final(blocos_salvos, caminho_saida)
        else:
            print("[Rank 0] Nenhum bloco processado.")
        tempo_final = time.time()
        print(f"Tempo de execução: {tempo_final - tempo_inicio:.2f} segundos")
