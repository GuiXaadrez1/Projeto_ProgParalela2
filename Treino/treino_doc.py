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

        #print(f' processo de id {rank}, recebeu o bloco: {get_bloc}')
               
        return n_subblocos, get_bloc
        
        '''
            Basicamente um unico processo (serializado) está pegando todos os blocos
            
            Use o forloop abaixo para saber qual rank está processando o bloco:

            for i, bloco in enumerate(get_bloc):
                print(f"Bloco {i}: {bloco}")
        
        '''

    elif size > 1:
        
        blocos_rank = [bloco for i, bloco in enumerate(blocos) if i % size == rank]
        
        #blocos_rank = comm.scatter(blocos_para_scatter,root=0)
        #print(f' processo de id {rank}, recebeu o bloco: {blocos_rank} do rank 0')
        
        return n_subblocos, blocos_rank
        
        '''
            blocos é uma lista de arrays numpy.
            
            enumerate(blocos) gera pares de: (i, bloco) 

            i é o índice na lista de blocos

            bloco é o sub-array correspondente (ex: array([0, 1, 2, 3]))
            
            Para cada índice i de bloco, o processo com rank == i % size vai pegar esse bloco.

            Assim, os blocos são distribuídos de forma intercalada (round-robin) entre os processos.

            Essa condição if i % size == rank
            
            É a condição de distribuição de blocos entre processos.

            i % size calcula o resto da divisão do índice do bloco pelo número de processos.

            Se o resto for igual ao rank do processo atual, esse processo pega o bloco.
            
            Formula matématica para calcular uma divisão de inteiro com resto:
                    
                    a = b ⋅ q + r

                Informações:    
                    
                    a = dividendo
                    b = divisor
                    q = quociente inteiro (parte inteira da divisão)
                    r = resto
                
                condição: 0 ≤ r < b 

                Exemplo: 

                    Vamos encontrar q (quociente inteiro) e r (resto):                    
                
                    a = 3
                    b = 4 

                    
                    3 = 4.q+r 

                    Sabemos que 4 não cabe nenhuma vez inteira dentro de 3, então:
                
                    q = 0 

                    Agora, substituímos:

                    3 = 4 ⋅ 0 + r ⇒ r = 3
                    
                    portanto: 

                    3 ÷ 4 ⇒ quociente = 0 , resto = 3

        '''
    
def processar_linhas_img(blocos_rank, img_largura, banda_img, n_subblocos, caminho_tif):

    """
    
        blocos_rank: lista de blocos (linhas da imagem) que esse processo deve processar.
        img_largura: largura (colunas) da imagem (lembre- se que a imagem é um array do numpy)
        banda_img: número de bandas do raster (ex: 3 = RGB).
        blocos: número de sub-blocos que foram criados para cada processo, lembre - se que esse blocos, são uma lista de array
    
    
    """

    # criando uma lista de resultados vazia para comportar blocos, sub_blocos processados de cada rank
    resultados = []
   
    with rasterio.open(caminho_tif) as raster: # ler a imagem do nosso raster e fecha automaticamente após o processamento e leitura
    
        for idx, bloco in enumerate(blocos_rank):
                linha_ini = bloco[0]
                linha_fim = bloco[-1] + 1
                altura_local = linha_fim - linha_ini

                '''
                Cada bloco contém uma fatia de linhas da imagem.

                    linha_ini → linha inicial do bloco

                    linha_fim → linha final (inclusive)

                    altura_local → número de linhas (altura) que serão processadas
                
                
                '''

                print(f"[Processo {rank}] Processando linhas: {linha_ini} a {linha_fim} (bloco {idx})")

                window = rasterio.windows.Window(col_off=0, row_off=linha_ini, width=img_largura, height=altura_local)

                '''
                
                    Essa janela pega todas as colunas, mas só um subconjunto de linhas

                    Isso evita carregar a imagem toda na memória    
                
                '''

                try:
                    dados = raster.read(window=window)
                except Exception as e:
                    print(f"[Processo {rank}] Erro ao ler janela {linha_ini}:{linha_fim} - {e}")
                    continue

                '''

                    Lê as bandas da imagem na região da window

                    Se ocorrer erro na leitura (ex: arquivo corrompido), ele pula

                    Quando você usa .read() em uma imagem raster com múltiplas bandas 
                    (ex: RGB), o resultado é um array NumPy com 3 dimensões:

                    dimensão 0: bandas (ex: 3 para R, G, B)

                    dimensão 1: altura (linhas)

                    dimensão 2: largura (colunas)

                    ou seja:

                    dados[0] → banda 1 (ex: vermelho)

                    dados[1] → banda 2 (ex: verde)

                    dados[2] → banda 3 (ex: azul)

                    forma padrão do método: raster.read → retorna (bands, height, width)

                    Exemplo:

                        dados.shape = (3, 512, 512)
                    
                    Porém é um problema para o Opencv, pois ele espera no formato: (height, width, bands)

                    Então, para que a imagem seja compatível com o OpenCV, precisamos reordenar os eixos 
                    de (bands, height, width) para (height, width, bands)
                
                '''

                if banda_img >= 3:
                            
                    # slicing de 0 até 2, ou seja, avança por indicie até chegar no terceiro
                    
                    img_rgb = dados[:3].transpose(1, 2, 0)  # (bands, H, W) → (H, W, bands)
                    
                    # aqui converte a imagem RGB para Gray (tons de cinza)

                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
                    
                    '''

                        Se a imagem tiver mais de  três ou mais canais (bandas):
                            
                            - Captamos a banda retornada como dados do  raster.read(window=window)
                            e realizamos a reordenação dos eixos para ser compatível com o Opencv:
                            (bands, H, W) → (H, W, bands)

                        O método .transpose(axes) -> é um método que reorganiza as dimensões (eixos) de um array NumPy, sem alterar os dados,
                        penas muda a forma como eles são acessados.
                    
                        axes: uma tupla que define a nova ordem dos eixos.

                        Se nada for passado: para arrays 2D, faz array.T (inverte os dois eixos).

                        Para arrays 3D ou superiores: você deve passar a nova ordem dos eixos manualmente.
                    
                    '''
                
                else:
                    
                    img_gray = dados[0]

                _, bordas = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
                #_, bordas = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                '''
                
                    Essa função do OpenCV aplica limiarização (thresholding) em uma imagem, 
                    ou seja, transforma uma imagem em preto e branco (binária), com base em um valor
                    de corte (limiar).

                    Sintaxe: cv2.threshold(src, thresh, maxval, type)

                    Parâmetros:

                        src: imagem de entrada (deve estar em escala de cinza).

                        thresh: valor de limiar (threshold) manual.

                        maxval: valor para atribuir aos pixels que passam no teste.

                        type: tipo de limiarização.

                    Atributos: 

                    cv2.THRESH_BINARY: aplica limiar binário — pixels acima do limiar ficam com valor 255, e os abaixo com 0.

                    cv2.THRESH_OTSU: ativa o método automático de detecção do melhor limiar, com base no histograma da imagem.

                    Especificações: 

                    O trecho _, bordas = ... é uma forma comum em Python de descartar um valor retornado por uma função que retorna múltiplos 
                    resultados, mantendo apenas o que interessa.

                    O símbolo _ (underline) em Python é uma convenção para indicar que uma variável não será usada. Ele é muito comum quando:

                    Você recebe múltiplos valores de retorno de uma função, mas só se importa com um deles.

                    Você percorre um loop e não usa o índice/valor.

                    função cv2.threshold() retorna dois valores:

                    O limiar usado (útil às vezes).

                    A imagem processada, que você realmente quer.

                    Você ignora o primeiro valor usando _, e só guarda o segundo na variável bordas

                    Exemplo: 

                        a, _ = (1, 2)
                        print(a)  # 1

                    quando você faz = a,b = [i for i in range(0,100)] você obtem um tupla representando os dois valores (a,b)
                    porém neste caso descartamos uma das variáveis
                
                '''


                # Armazenar localmente se estivermos apenas um processo
                if size == 1:
                    resultados.append((linha_ini, bordas))


                # Armazenar localmente se estivermos apenas um processo                
                elif size > 1:
                    
                    if rank == 0:
                        resultados.append((linha_ini, bordas))

                        
                        '''
                            Se o processo atual é o mestre (rank == 0):

                            Ele guarda localmente as bordas no array resultados.

                            linha_ini indica onde esse bloco começa na imagem original (importante para ordenar depois).
                        
                        '''

                    else:
                        comm.send((linha_ini, bordas), dest=0, tag=idx)

                        '''
                            Se for um worker (rank != 0):

                            Ele envia o bloco de bordas de volta para o processo mestre via MPI com:

                            linha_ini: para saber onde encaixar o bloco.

                            tag=idx: o índice do bloco, útil para identificar as mensagens.
                        
                        '''
            
    # Processo mestre: coleta, ordena e salva
    if rank == 0:
       
        # Recebe os blocos dos outros ranks
        for src_rank in range(1, size):

            '''
            
            O laço vai percorrer os outros processos (que são os trabalhadores).

            size é o número total de processos MPI.

            src_rank vai variar de 1 até size-1, ou seja, percorre todos os processos exceto o mestre (rank 0).
            
            '''
            
            blocos_esperados = sum(1 for i in range(size * n_subblocos) if i % size == src_rank)

            '''
            
                Aqui, o mestre calcula quantos blocos ele espera receber do processo src_rank.

                O cálculo funciona assim:

                n_subblocos é o número de subblocos em que a imagem foi dividida por processo (uma divisão total é size * n_subblocos blocos).

                O somatório conta quantos índices i no intervalo de 0 até size * n_subblocos - 1 satisfazem a condição i % size == src_rank.

                Isso representa quantos blocos foram atribuídos ao processo com src_rank.

                Exemplo: Se size=4 e n_subblocos=3, temos 4*3=12 blocos no total.

                Para src_rank=1, a condição conta todos i entre 0 e 11 onde i % 4 == 1, ou seja, índices 1, 5, 9 → 3 blocos.
            
            
            '''
            
            for _ in range(blocos_esperados):
                
                linha_ini_recv, bloco_recv = comm.recv(source=src_rank, tag=MPI.ANY_TAG)
               
                resultados.append((linha_ini_recv, bloco_recv))


            '''
                Agora, para cada bloco que o mestre espera receber daquele processo (blocos_esperados vezes), ele:

                Recebe uma mensagem MPI de src_rank (o processo trabalhador) com comm.recv.

                Essa mensagem contém um par:

                linha_ini_recv: número da linha inicial desse bloco na imagem original.

                bloco_recv: dados do bloco (por exemplo, uma parte da imagem processada).

                Adiciona esse par (linha_ini_recv, bloco_recv) na lista resultados.

                Essa etapa coleta todos os pedaços da imagem processada que os outros processos enviaram.
            
            '''

        # Ordenar os blocos pelas linhas de origem
        resultados.sort(key=lambda x: x[0])

        '''
            Depois de receber todos os blocos, o mestre ordena a lista resultados pela linha inicial linha_ini_recv.

            Isso é crucial para montar a imagem final na ordem correta, pois os blocos podem ter chegado fora de ordem.
        '''

        imagem_final = np.vstack([r[1] for r in resultados])

        '''

        Aqui, o mestre empilha verticalmente todos os blocos da imagem na ordem certa para formar a imagem completa.

        np.vstack cria um array maior juntando os blocos um embaixo do outro.

        [r[1] for r in resultados] pega só o bloco de dados de cada par (descarta a linha inicial já que só usou para ordenar).

        O que é o r?

        Aqui, r é uma variável usada no loop da list comprehension [r[1] for r in resultados].

        O resultados é uma lista de tuplas, e cada tupla tem dois elementos:

        r[0] = linha_ini_recv (a linha inicial do bloco na imagem original)

        r[1] = bloco_recv (os dados do bloco, como um array NumPy contendo parte da imagem)

        Então, r representa cada tupla da lista resultados.

        O que está acontecendo?
  
        A expressão [r[1] for r in resultados] cria uma nova lista pegando apenas o segundo elemento de cada tupla — ou seja,
        só os blocos de dados, descartando a linha inicial que foi usada para ordenar.
                
        '''

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
    
    caminho_saida = os.path.join(os.getcwd(),"imagens_processadas","imagem_final.png")

    if size == 1:
        
        informacoes = read_tif(caminho_tif=caminho_tif)
        
        # definindo os indices das informações
        for idx, i in enumerate(informacoes):
            
            print(f'informação de indice {idx}: {i}')
            
            #print(f'informação de indice {idx}: {type(i)}') # usei para descobrir os tipos de dados que cada informação retorna

        sub_blocos_rank = dividir_matriz(64,altura_img=informacoes[3]) 

        img_processada = processar_linhas_img(sub_blocos_rank[1],informacoes[4],informacoes[2],sub_blocos_rank[0], caminho_tif=caminho_tif)

        salvar_img_processada(caminho_saida=caminho_saida, imagem_final= img_processada)    
        
        tempo_final = time.time()

        print(f"Tempo de execução: {tempo_final - tempo_inicio:.2f} segundos")
    
    else:
        
        caminho_tif = os.path.join(os.getcwd(), "..", "imagens_satelites", "img_satelite.tif") 

        caminho_saida2 = os.path.join(os.getcwd(),"..","imagens_processadas","imagem_final_mpi.png")   
        
        informacoes = read_tif(caminho_tif=caminho_tif)
        
       
            
            #print(f'informação de indice {idx}: {type(i)}') # usei para descobrir os tipos de dados que cada informação retorna
        
        sub_blocos_rank = dividir_matriz(64,altura_img=informacoes[3]) 

        img_processada = processar_linhas_img(
            sub_blocos_rank[1],
            informacoes[4],
            informacoes[2],
            n_subblocos=sub_blocos_rank[0],
            caminho_tif=caminho_tif
        )

        # Reunir partes da imagem processada em todos os ranks
        partes_processadas = comm.gather(img_processada, root=0)

        if rank == 0:
            if img_processada is not None and img_processada.size > 0:
                salvar_img_processada(caminho_saida=caminho_saida2, imagem_final=img_processada)
            else:
                print(f"[Rank {rank}] Erro: imagem processada é vazia ou None! Não será salva.")

        tempo_final = time.time()

        if rank == 0:
            print(f"Tempo de execucao: {tempo_final - tempo_inicio:.2f} segundos")  

'''
        
             # definindo os indices das informações
            for idx, i in enumerate(informacoes):
            
            print(f'informação de indice {idx}: {i}')       
'''