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
    
def dividir_matriz(qtd_sub_blocos:int, altura_img:int):
    """
        Divide a altura da imagem (número total de linhas) em sub-blocos para distribuição entre processos MPI.

        Parâmetros:
        -----------
        
        qtd_sub_blocos : int
            Quantidade de sub-blocos por processo.
        
        altura_img : int
            Número total de linhas (altura) da imagem/matriz.

        Retorna:
        --------
       
         blocos_rank : list of numpy.ndarray
            Lista de arrays 1D contendo os índices das linhas da imagem que devem ser processadas pelo processo atual (rank).

        Detalhes:
        ---------
        - `np.arange(altura_img)` cria um array NumPy 1D com valores de 0 até altura_img - 1, representando os índices das linhas.
        Por exemplo, `np.arange(15)` gera o array [0, 1, 2, ..., 14].

        - A função np.array_split do NumPy serve para dividir um array em várias partes menores (sub-arrays) de forma personalizada
        assim você pode trabalhar com pedaços separados dos dados. Essa função vai retornar uma lista de array
        Exemplo:

            List[   
                
                array[
                    [
                        array([   0,    1,    2, ..., 1149, 1150, 1151], shape=(1152,)), 
                        array([1152, 1153, 1154, ..., 2301, 2302, 2303] (...)
                    ]
                ]   
            ]

            - Sintaxe Básica: np.array_split(ary, indices_or_sections, axis=0)

                matriz: É o array que você quer dividir (pode ser 1D, 2D, etc).

                índices_ou_seções:Define como o array será dividido. Pode ser:

                    - Um número inteiro: o array será dividido em partes aproximadamente iguais.

                    - Se não for divisível exatamente, algumas partes terão um elemento a mais.

                    - Uma lista de índices: define os pontos exatos onde o array será dividido.

                axis (opcional): eixo ao longo do qual o array será dividido (padrão é 0, que geralmente significa divisão por linhas).
        
        - Em seguida, cada processo recebe os sub-blocos intercalados correspondentes ao seu `rank`.
        Isso é feito com a seleção `if i % size == rank`.

        - Essa estratégia permite uma divisão mais granular e balanceada do trabalho entre processos,
        especialmente útil quando a altura da imagem não é múltipla exata do número de processos.

        Exemplo:
        --------
        Se altura_img = 18432, size = 4, qtd_sub_blocos = 8,
        então haverá 4 * 8 = 32 sub-blocos,
        e cada processo vai receber 8 sub-blocos contendo índices de linhas da imagem.
    """
    
    n_subblocos = qtd_sub_blocos
    blocos = np.array_split(np.arange(altura_img), size * n_subblocos)
    '''
        basicamente dividimos o a nosso array de 1D gerada com a função arange do Numpy com base na altura (linhas)
        pela quantidade de sub-blocos vezes a quantidade de processos do nosso comunicador Afim de obter
        pequenas partes do array array original em uma lista que colocamos na variável chamada de blocos
        
        use: 
                for idx in enumerate(blocos):
                    print(idx) 

        para descobobrir a quantidade de blocos que o array foi dividido

        logo, ele foi divido em 16 array menores (sub-array) dentro da variável blocos 
        Lembre-se que esses sub-arrays estão dentro de um lista 
        
        print(type(blocos))
        <class 'list'>
    
    '''
    if size == 1:
        
        get_bloc = [bloco for i, bloco in enumerate(blocos) if i % 1 == 0]

        print(f' processo de id {rank}, recebeu o bloco: {get_bloc}')
               
        return get_bloc
        
        '''
            Basicamente um unico processo (serializado) está pegando todos os blocos
            
            Use o forloop abaixo para saber qual rank está processando o bloco:

            for i, bloco in enumerate(get_bloc):
                print(f"Bloco {i}: {bloco}")
        
        '''

    elif size > 1:
        
        blocos_rank = [bloco for i, bloco in enumerate(blocos) if i % size == rank]
        
        #blocos_rank = comm.scatter(blocos_para_scatter,root=0)
        print(f' processo de id {rank}, recebeu o bloco: {blocos_rank} do rank 0')
        
        return blocos_rank
        
        '''

    
        '''
    
    

def processar_linhas():
    pass

if __name__ == "__main__":
    
    comm = MPI.COMM_WORLD # vai criar o canal de comunicação entre os processos MPI
    rank = comm.Get_rank() # vai retornar o id do rank
    size = comm.Get_size() # vai retornar a quantidade total de procesos ranks/trabalhadores no comunicador
    
    
    
    caminho_tif = os.path.join(os.getcwd(),"imagens_satelites","img_satelite.tif")

    
    if size == 1:
        
        informacoes = read_tif(caminho_tif=caminho_tif)
        
        # definindo os indices das informações
        for idx, i in enumerate(informacoes):
            
            print(f'informação de indice {idx}: {i}')
            
            #print(f'informação de indice {idx}: {type(i)}') # usei para descobrir os tipos de dados que cada informação retorna
        
        sub_blocos = dividir_matriz(32,altura_img=informacoes[3])     
        print(sub_blocos)
    
    else:
        
        caminho_tif = os.path.join(os.getcwd(), "..", "imagens_satelites", "img_satelite.tif")     
        
        informacoes = read_tif(caminho_tif=caminho_tif)
        
        # definindo os indices das informações
        for idx, i in enumerate(informacoes):
            
            print(f'informação de indice {idx}: {i}')
            
            #print(f'informação de indice {idx}: {type(i)}') # usei para descobrir os tipos de dados que cada informação retorna
        
        sub_blocos = dividir_matriz(32,altura_img=informacoes[3])     
        #print(sub_blocos)    
        
    pass