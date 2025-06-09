import rasterio
from mpi4py import MPI
import cv2
import os
import time
import numpy as np
import gc  # Import para coletor de lixo

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
                dados = raster.read([1,2,3] if banda_img >= 3 else [1], window=window)
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

def reduzir_blocos_em_imagem_final_mpi(lista_blocos, caminho_saida_final):
    """
    Cada rank envia seus blocos como (bloco_id, imagem_numpy). A imagem final é montada no rank 0 com ordem global correta.
    """
    blocos_ordenados = []

    # Carrega os blocos em memória com seus respectivos IDs
    for bloco_id, caminho_img in lista_blocos:
        img = cv2.imread(caminho_img, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"[Rank {rank}] Erro ao carregar {caminho_img}")
            continue
        blocos_ordenados.append((bloco_id, img))

    # Etapa de redução binária
    etapa = 1
    while etapa < size:
        parceiro = rank ^ etapa
        if parceiro >= size:
            etapa *= 2
            continue

        if rank < parceiro:
            # Recebe lista de blocos do parceiro
            recv_data = comm.recv(source=parceiro, tag=100 + etapa)
            blocos_ordenados.extend(recv_data)
        else:
            # Envia lista para o parceiro
            comm.send(blocos_ordenados, dest=parceiro, tag=100 + etapa)
            return  # após envio, o processo termina
        etapa *= 2

    # Rank 0 junta tudo
    blocos_ordenados.sort(key=lambda x: x[0])  # Ordena globalmente por bloco_id
    imagem_final = np.vstack([img for _, img in blocos_ordenados])
    cv2.imwrite(caminho_saida_final, imagem_final)
    print(f"[Rank 0] Imagem final salva em: {caminho_saida_final}")

if __name__ == "__main__":
    tempo_inicio = time.time()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    caminho_tif = os.path.join(os.getcwd(), "..", "imagens_satelites", "img_satelite2.tif")
    #caminho_tif = os.path.join(os.getcwd(), "..", "imagens_convertidas_tif", "imagem1.tif")
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

    # Nova função com redução distribuída
    if blocos_salvos:
        reduzir_blocos_em_imagem_final_mpi(blocos_salvos, caminho_saida)

    if rank == 0:
        tempo_final = time.time()
        print(f"Tempo de execucao: {tempo_final - tempo_inicio:.2f} segundos")
