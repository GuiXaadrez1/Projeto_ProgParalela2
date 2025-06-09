FLUXO DETALHADO DO PROGRAMA DE PROCESSAMENTO MPI DE IMAGENS .TIF

    Este programa tem como objetivo processar uma imagem georreferenciada no formato .tif, utilizando paralelismo com MPI (Message Passing Interface). O processamento é dividido em blocos verticais, e cada processo MPI trata uma parte da imagem. No final, os blocos processados são reunidos em uma imagem final binarizada. Abaixo está o passo a passo detalhado do fluxo:

1. Inicialização MPI

    O programa começa inicializando o ambiente de comunicação MPI.

    Cada processo recebe um identificador único (rank) e todos conhecem o total de processos (size).

    O processo com rank == 0 será o responsável por consolidar os dados e salvar a imagem final.

2. Leitura das Informações da Imagem
    
    Uma imagem .tif é aberta com a biblioteca rasterio para extrair:

    Altura e largura da imagem.

    Número de bandas (canais de cor).

    Formato e dimensões gerais.

    Essas informações são utilizadas para configurar o corte da imagem em blocos.

3. Divisão da Imagem em Blocos para Processamento Paralelo

    A imagem é dividida em 128 blocos horizontais (linhas).

    Cada processo MPI só trabalha nos blocos onde o número do bloco mod size é igual ao seu rank, garantindo divisão equilibrada entre os processos.

    Para cada bloco:

        Define-se uma janela (window) para ler apenas a parte da imagem correspondente.

        São lidas as bandas RGB (ou só a banda 1 se houver apenas uma).

        Se RGB, a imagem é convertida para tons de cinza.

        Aplica-se uma limiarização binária invertida (THRESH_BINARY_INV) com valor 120.

        O bloco resultante é salvo como uma imagem .png temporária.

4. Redução e Montagem da Imagem Final

    Cada processo mantém uma lista dos blocos que salvou, contendo o ID do bloco e o caminho do arquivo.

    Uma etapa de redução binária é realizada:

        Os processos se comunicam entre si em pares, usando XOR de seus ranks, trocando dados.

        Processos de rank maior enviam suas listas para processos de rank menor.

        Apenas o processo de rank 0 permanece no final com todos os blocos recebidos.

    O processo de rank 0:

        Ordena os blocos pelo ID.

        Lê cada imagem de bloco e as empilha verticalmente (np.vstack) para formar a imagem final.

        Salva a imagem final processada no caminho de saída.

5. Medição de Tempo e Finalização

    O tempo total de execução é medido desde o início até o salvamento da imagem.

    Apenas o rank 0 imprime o tempo de execução total.


6. Resumo

    O programa divide uma imagem .tif em blocos verticais.

    Cada processo MPI trata parte da imagem, aplicando uma limiarização invertida.

    Os blocos são temporariamente salvos como imagens em disco.

    Um algoritmo de redução binária junta os blocos no processo principal.

    O resultado é uma nova imagem que representa uma versão processada da original.