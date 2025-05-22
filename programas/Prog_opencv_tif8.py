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
    # Converter a imagem de RGB para HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_RGB2HSV)

    # Ajustar o intervalo de cor para o asfalto (tons escuros e saturação moderada)
    lower = np.array([10, 50, 100])  # Cor mais escura (marrom claro)
    upper = np.array([30, 150, 200])  # Cor mais clara (marrom claro)

    # Criar máscara de asfalto
    mascara_asfalto = cv2.inRange(hsv, lower, upper)

    # Operações morfológicas para limpar a máscara (fechar pequenas lacunas)
    kernel = np.ones((3, 3), np.uint8)  # Usar um kernel menor para evitar expansão excessiva
    limpo = cv2.morphologyEx(mascara_asfalto, cv2.MORPH_CLOSE, kernel)

    # Filtrar contornos com base em área e razão de aspecto
    contornos, _ = cv2.findContours(limpo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mascara_filtrada = np.zeros_like(limpo)

    for cnt in contornos:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h) if h != 0 else 0

        # Filtra áreas grandes com forma alongada (aspect_ratio > 2.5)
        if area > 500 and aspect_ratio > 2.5:  
            cv2.drawContours(mascara_filtrada, [cnt], -1, 255, -1)

    return mascara_filtrada

# Abrir imagem com Rasterio
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
            img_rgb = cv2.cvtColor(dados[0], cv2.COLOR_GRAY2RGB)

        # Segmentar a imagem para estradas
        bordas = segmentar_estradas(img_rgb)

        # Inverter a máscara para garantir que o asfalto seja branco e o resto preto
        bordas_binaria = cv2.bitwise_not(bordas)

        # Armazenar ou enviar resultado
        if rank == 0:
            resultados.append((linha_ini, bordas_binaria))
        else:
            comm.send((linha_ini, bordas_binaria), dest=0, tag=idx)

    # Processo mestre: juntar e salvar
    if rank == 0:
        for src_rank in range(1, size):
            blocos_esperados = sum(1 for i in range(size * n_subblocks) if i % size == src_rank)
            for _ in range(blocos_esperados):
                linha_ini_recv, bloco_recv = comm.recv(source=src_rank, tag=MPI.ANY_TAG)
                resultados.append((linha_ini_recv, bloco_recv))

        # Ordenar os blocos pelas linhas de origem
        resultados.sort(key=lambda x: x[0])
        imagem_final = np.vstack([r[1] for r in resultados])

        # Salvar a imagem final binária com estradas em branco
        caminho_saida = os.path.join(PASTA_SAIDA, "imagem_final_segmentada_binaria.png")
        cv2.imwrite(caminho_saida, imagem_final)
        print(f"[Processo 0] Imagem final salva em: {caminho_saida}")
