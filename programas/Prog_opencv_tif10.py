from mpi4py import MPI
import numpy as np
import cv2
import os

# Inicializa MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Caminhos
IMAGEM_PATH = r"C:\Projeto_ProgParalela2\imagens_satelites\satelit_google.tif"
PASTA_SAIDA = r"C:\Projeto_ProgParalela2\resultados_rasterio"
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Função para segmentar estradas em tons de marrom claro
def segmentar_estradas(imagem):
    # Converter RGB para HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_RGB2HSV)

    # Intervalo de cor ajustado (marrom claro)
    lower = np.array([0, 0, 50])     # Cor mais escura
    upper = np.array([180, 50, 200]) # Cor mais clara

    # Criar a máscara com inRange para o intervalo ajustado
    mascara = cv2.inRange(hsv, lower, upper)

    # Morfologia: remover pequenos buracos e suavizar
    kernel = np.ones((3, 3), np.uint8)
    mascara_limpa = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)

    # Encontrar contornos e aplicar mais filtros
    contornos, _ = cv2.findContours(mascara_limpa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mascara_filtrada = np.zeros_like(mascara_limpa)

    for cnt in contornos:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h) if h != 0 else 0

        # Filtrando áreas grandes e com forma alongada (com razão de aspecto maior)
        if area > 500 and aspect_ratio > 2.5:  
            cv2.drawContours(mascara_filtrada, [cnt], -1, 255, -1)

    return mascara_filtrada

# Abrir imagem diretamente com OpenCV
imagem = cv2.imread(IMAGEM_PATH)

# Verificar se a imagem foi carregada corretamente
if imagem is None:
    print(f"Erro ao carregar a imagem: {IMAGEM_PATH}")
    exit()

# Dividir a imagem em blocos horizontais para processamento paralelo
altura, largura, canais = imagem.shape
n_subblocks = 8
blocos = np.array_split(np.arange(altura), size * n_subblocks)
blocos_rank = [b for i, b in enumerate(blocos) if i % size == rank]

resultados = []

for idx, bloco in enumerate(blocos_rank):
    linha_ini = bloco[0]
    linha_fim = bloco[-1] + 1
    altura_local = linha_fim - linha_ini

    print(f"[Processo {rank}] Processando linhas {linha_ini} a {linha_fim} (bloco {idx})")

    # Extrair o bloco da imagem
    img_bloco = imagem[linha_ini:linha_fim, :]

    # Aplicar segmentação
    mascara_segmentada = segmentar_estradas(img_bloco)

    # Inverter máscara (opcional: estradas brancas)
    mascara_invertida = cv2.bitwise_not(mascara_segmentada)

    # Armazenar ou enviar resultado
    if rank == 0:
        resultados.append((linha_ini, mascara_invertida))
    else:
        comm.send((linha_ini, mascara_invertida), dest=0, tag=idx)

# Processo mestre junta os blocos
if rank == 0:
    for src_rank in range(1, size):
        blocos_esperados = sum(1 for i in range(size * n_subblocks) if i % size == src_rank)
        for _ in range(blocos_esperados):
            linha_ini_recv, bloco_recv = comm.recv(source=src_rank, tag=MPI.ANY_TAG)
            resultados.append((linha_ini_recv, bloco_recv))

    # Ordenar resultados pelas linhas
    resultados.sort(key=lambda x: x[0])
    imagem_final = np.vstack([r[1] for r in resultados])

    # Salvar imagem segmentada
    caminho_saida = os.path.join(PASTA_SAIDA, "imagem_final_segmentada_binaria.png")
    cv2.imwrite(caminho_saida, imagem_final)
    print(f"[Processo 0] Imagem final salva em: {caminho_saida}")
