import rasterio
from mpi4py import MPI
import cv2
import os
import time
import numpy as np
import gc

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
    total_blocos = 128
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
            window = rasterio.windows.Window(col_off=0, row_off=inicio, width=img_largura, height=altura_local)

            try:
                dados = raster.read([1, 2, 3] if banda_img >= 3 else [1], window=window)
            except Exception as e:
                print(f"[Rank {rank}] Erro ao ler bloco {bloco_id}: {e}")
                continue

            if banda_img >= 3:
                img_rgb = dados[:3].transpose(1, 2, 0)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            else:
                img_gray = dados[0]

            _, bordas = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY_INV)
            nome_bloco = f"bloco_{bloco_id:03d}.png"
            caminho_bloco = os.path.join(pasta_blocos, nome_bloco)
            cv2.imwrite(caminho_bloco, bordas)

            resultados.append((bloco_id, caminho_bloco))

            del dados, img_gray, bordas
            if banda_img >= 3:
                del img_rgb
            gc.collect()

    return resultados

def enviar_em_chunks(data, dest, tag_base=1000, chunk_size=100_000):
    for i in range(0, len(data), chunk_size):
        comm.send(data[i:i + chunk_size], dest=dest, tag=tag_base + i // chunk_size)
    comm.send(None, dest=dest, tag=tag_base + len(data) // chunk_size + 1)

def receber_em_chunks(source, tag_base=1000):
    recebido = []
    i = 0
    while True:
        parte = comm.recv(source=source, tag=tag_base + i)
        if parte is None:
            break
        recebido.extend(parte)
        i += 1
    return recebido

def reduzir_blocos_em_imagem_final_mpi(lista_blocos, caminho_saida_final):
    blocos_ordenados = list(lista_blocos)  # Garante que seja uma lista nova

    etapa = 1
    while etapa < size:
        parceiro = rank ^ etapa
        if parceiro >= size:
            etapa *= 2
            continue

        if rank < parceiro:
            recv_data = receber_em_chunks(source=parceiro, tag_base=etapa * 1000)
            blocos_ordenados.extend(recv_data)
        else:
            enviar_em_chunks(blocos_ordenados, dest=parceiro, tag_base=etapa * 1000)
            return
        etapa *= 2

    blocos_ordenados.sort(key=lambda x: x[0])
    imagens = []
    for bloco_id, caminho_img in blocos_ordenados:
        img = cv2.imread(caminho_img, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"[Rank 0] Falha ao carregar {caminho_img}")
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

    caminho_tif = os.path.join(os.getcwd(), "..", "imagens_satelites", "imagem1_2.tif")
    caminho_saida = os.path.join(os.getcwd(), "..", "imagens_processadas", "imagem_final_blocos_binary_inv.png")
    pasta_blocos = os.path.join(os.getcwd(), "..", "blocos_tmp")
    os.makedirs(pasta_blocos, exist_ok=True)

    inform = informacoes(caminho_tif=caminho_tif)

    blocos_salvos = processar_linhas_img(
        img_largura=inform[4],
        banda_img=inform[2],
        caminho_tif=caminho_tif,
        altura_total=inform[3],
        pasta_blocos=pasta_blocos
    )

    if blocos_salvos:
        reduzir_blocos_em_imagem_final_mpi(blocos_salvos, caminho_saida)

    if rank == 0:
        tempo_final = time.time()
        print(f"Tempo de execucao: {tempo_final - tempo_inicio:.2f} segundos")
