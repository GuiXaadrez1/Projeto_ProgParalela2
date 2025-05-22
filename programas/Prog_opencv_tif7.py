from mpi4py import MPI
import numpy as np
import cv2
import os
import rasterio

# Inicializa MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Caminhos
IMAGEM_PATH = r"C:\Projeto_ProgParalela2\imagens_satelites\satelit_google.tif"
PASTA_SAIDA = r"C:\Projeto_ProgParalela2\resultados_rasterio"
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Função para segmentação de estradas
def segmentar_estradas(imagem):
    # Converter para escala de cinza
    img_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    # Aplicar limiarização de Otsu
    _, limiarizado = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Operações morfológicas para remover ruído e preencher lacunas
    kernel = np.ones((5, 5), np.uint8)
    dilatada = cv2.dilate(limiarizado, kernel, iterations=2)
    erodida = cv2.erode(dilatada, kernel, iterations=1)

    return erodida

# Abrir imagem com rasterio
with rasterio.open(IMAGEM_PATH) as src:
    altura = src.height
    largura = src.width
    canais = src.count

    # Dividir a imagem em blocos horizontais
    n_subblocks = 8
    blocos = np.array_split(np.arange(altura), size * n_subblocks)
    blocos_rank = [bloco for i, bloco in enumerate(blocos) if i % size == rank]

    resultados = []

    for idx, bloco in enumerate(blocos_rank):
        linha_ini = bloco[0]
        linha_fim = bloco[-1] + 1
        altura_local = linha_fim - linha_ini

        print(f"[Processo {rank}] Processando linhas {linha_ini} a {linha_fim} (bloco {idx})")

        window = rasterio.windows.Window(col_off=0, row_off=linha_ini, width=largura, height=altura_local)

        try:
            dados = src.read(window=window)
        except Exception as e:
            print(f"[Processo {rank}] Erro ao ler janela {linha_ini}:{linha_fim} - {e}")
            continue

        if canais >= 3:
            img_rgb = dados[:3].transpose(1, 2, 0)
        else:
            img_rgb = dados[0]

        # Segmentar a imagem para estradas
        bordas = segmentar_estradas(img_rgb)

        # Armazenar localmente ou enviar ao rank 0
        if rank == 0:
            resultados.append((linha_ini, bordas))
        else:
            comm.send((linha_ini, bordas), dest=0, tag=idx)

    # Processo mestre: coleta, ordena e salva
    if rank == 0:
        # Recebe os blocos dos outros ranks
        for src_rank in range(1, size):
            blocos_esperados = sum(1 for i in range(size * n_subblocks) if i % size == src_rank)
            for _ in range(blocos_esperados):
                linha_ini_recv, bloco_recv = comm.recv(source=src_rank, tag=MPI.ANY_TAG)
                resultados.append((linha_ini_recv, bloco_recv))

        # Ordenar os blocos pelas linhas de origem
        resultados.sort(key=lambda x: x[0])
        imagem_final = np.vstack([r[1] for r in resultados])

        # Salvar a imagem completa
        caminho_saida = os.path.join(PASTA_SAIDA, "imagem_final_segmentada.png")
        cv2.imwrite(caminho_saida, imagem_final)
        print(f"[Processo 0] Imagem final salva em: {caminho_saida}")
