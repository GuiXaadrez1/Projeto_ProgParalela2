'''

    Objetivo é basicamente desenvolver um código do zero  com base no que venho estudando
    para seguimentação de estradas

'''

import rasterio 
from mpi4py import MPI
import cv2
import os 
import time
import numpy as np


def read_tif(caminho_tif):
    with rasterio.open(caminho_tif) as raster:
        
        corpo = raster.shape # tamanho da matriz/imagem/array -> tupla (total_linhas,total_coluna)
        formato = raster.driver # Formato do arquivo -> str
        banda = raster.count # Qunatidade de bandas -> int
        altura = raster.height # Altura -> int
        largura = raster.width # Largura -> int
        

        return corpo, formato, banda, altura, largura # vai retornar uma tupla
    
def processar_linhas_img(img_largura, banda_img, caminho_tif, altura_total):

    resultados = []
    total_blocos = 64
    linhas_por_bloco = altura_total // total_blocos
    resto = altura_total % total_blocos

    with rasterio.open(caminho_tif) as raster:
        for bloco_id in range(total_blocos):

            if bloco_id % size != rank:
                continue  # Pula blocos que não pertencem a este rank

            inicio = bloco_id * linhas_por_bloco
            fim = inicio + linhas_por_bloco

            # Ajusta o último bloco se houver sobra
            if bloco_id == total_blocos - 1:
                fim += resto

            altura_local = fim - inicio

            print(f"[Rank {rank}] Processando linhas {inicio} a {fim} (bloco {bloco_id})")

            window = rasterio.windows.Window(col_off=0, row_off=inicio, width=img_largura, height=altura_local)

            try:
                dados = raster.read(window=window)
            except Exception as e:
                print(f"[Rank {rank}] Erro ao ler bloco {bloco_id}: {e}")
                continue

            if banda_img >= 3:
                img_rgb = dados[:3].transpose(1, 2, 0)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            else:
                img_gray = dados[0]

            # Segmentação simples
            _, bordas = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

            if size == 1 or rank == 0:
                resultados.append((inicio, bordas))
            else:
                comm.send((inicio, bordas), dest=0, tag=bloco_id)

    if rank == 0:
        for src_rank in range(1, size):
            for bloco_id in range(total_blocos):
                if bloco_id % size != src_rank:
                    continue
                linha_ini_recv, bloco_recv = comm.recv(source=src_rank, tag=bloco_id)
                resultados.append((linha_ini_recv, bloco_recv))

        resultados.sort(key=lambda x: x[0])
        imagem_final = np.vstack([r[1] for r in resultados])
        return imagem_final

    return None

    '''
        Para qualquer outro processo que não seja o mestre (rank != 0), retorna None.

        Isso indica que somente o mestre monta e retorna a imagem completa, enquanto os trabalhadores só enviam os pedaços.
    '''

def salvar_img_processada(caminho_saida, imagem_final):
    # Salvar a imagem completa
        
        cv2.imwrite(caminho_saida, imagem_final)
        print(f"[Processo 0] Imagem final salva em: {caminho_saida}")




if __name__ == "__main__":
    
    tempo_inicio = time.time()

    comm = MPI.COMM_WORLD # vai criar o canal de comunicação entre os processos MPI
    rank = comm.Get_rank() # vai retornar o id do rank
    size = comm.Get_size() # vai retornar a quantidade total de procesos ranks/trabalhadores no comunicador
    
    
    
    caminho_tif = os.path.join(os.getcwd(),"imagens_satelites","img_satelite2.tif")
    
    caminho_saida = os.path.join(os.getcwd(),"imagens_processadas","imagem_final_serial.png")

    if size == 1:
        
        informacoes = read_tif(caminho_tif=caminho_tif)
        
        # definindo os indices das informações
        for idx, i in enumerate(informacoes):
            
            print(f'informação de indice {idx}: {i}')
            
            #print(f'informação de indice {idx}: {type(i)}') # usei para descobrir os tipos de dados que cada informação retorna

        img_processada = processar_linhas_img(
            img_largura=informacoes[4],
            banda_img=informacoes[2],
            caminho_tif=caminho_tif,
            altura_total=informacoes[3]
        )

        salvar_img_processada(caminho_saida=caminho_saida, imagem_final= img_processada)    
        
        tempo_final = time.time()

        print(f"Tempo de execução: {tempo_final - tempo_inicio:.2f} segundos")
    
    else:
        
        caminho_tif2 = os.path.join(os.getcwd(), "..", "imagens_satelites", "img_satelite2.tif") 

        caminho_saida2 = os.path.join(os.getcwd(),"..","imagens_processadas","imagem_final_mpi.png")   
        
        informacoes = read_tif(caminho_tif=caminho_tif2)
        
       
            
            #print(f'informação de indice {idx}: {type(i)}') # usei para descobrir os tipos de dados que cada informação retorna

        img_processada = processar_linhas_img(
            img_largura=informacoes[4],
            banda_img=informacoes[2],
            caminho_tif=caminho_tif2,
            altura_total=informacoes[3]
        )

        if rank == 0:
            if img_processada is not None and img_processada.size > 0:
                salvar_img_processada(caminho_saida=caminho_saida2, imagem_final=img_processada)
            else:
                print(f"[Rank {rank}] Erro: imagem processada é vazia ou None! Não será salva.")

        tempo_final = time.time()

        if rank == 0:
            print(f"Tempo de execucao: {tempo_final - tempo_inicio:.2f} segundos")  
