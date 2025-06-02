# Projeto_ProgParalela
1.Introdução 
Este projeto tem como objetivo principal realizar o processamento eficiente de imagens geográficas ou científicas no formato .tif com quatro canais (RGBA), convertendo-as para imagens em escala de cinza (Grayscale), utilizando as extensões .jpeg ou .png. A solução implementa paralelismo com MPI (Message Passing Interface) para acelerar o processamento em ambientes com múltiplos núcleos ou máquinas, buscando otimização de desempenho e economia de recursos computacionais.

2.Desafios da Solução
2.1. Conversão de arquivo .tif RGBA para .jpeg ou .png Gray
O formato .tif com quatro canais representa imagens com componentes Red, Green, Blue e Alpha (transparência). Para convertê-la para uma imagem de duas dimensões em escala de cinza, é necessário aplicar uma transformação que reduza os canais RGB em um único canal de intensidade.

Solução adotada:
O código utiliza a biblioteca Rasterio para abrir imagens .tif com múltiplos canais (neste caso, até 4).
A função segmentar_imagem() converte os dados lidos para o formato RGB (dados[:3]), descartando o canal Alpha se houver.
Essa imagem RGB é depois convertida em tensor do TensorFlow e processada por um modelo de segmentação semântica, que retorna uma máscara segmentada (matriz 2D).
A saída (mascara_segmentacao) é uma imagem em escala de cinza (com classes segmentadas) que é salva em formato .png com cv2.imwrite()

2.2. Divisão de trabalho MPI
O uso da biblioteca MPI permite distribuir o carregamento e processamento da imagem entre vários processos. Esse modelo de paralelismo é especialmente útil para imagens de grande dimensão, otimizando tempo e uso da CPU.

Solução adotada:
O código inicializa o MPI com mpi4py, e cada processo recebe um rank.
A imagem é dividida em blocos horizontais por linha (np.array_split).
Cada processo MPI (com base no seu rank) é responsável por processar apenas os blocos que lhe pertencem.
O processo mestre (rank 0) coordena o processo: processa seus próprios blocos e coleta os resultados dos outros processos com comm.recv().


2.3. Nível de Complexidade
A solução exige domínio sobre:
Processamento de imagens multidimensionais
Programação paralela com MPI
Sincronização de processos
Manipulação eficiente de arquivos grandes
A combinação dessas áreas torna o projeto desafiador, demandando planejamento e conhecimento técnico sólido.

Solução adotada:
O código lida com vários níveis de complexidade, como:
Leitura de arquivos grandes com múltiplos canais.
Divisão eficiente da imagem entre processos MPI.
Integração com um modelo de machine learning da web (TensorFlow Hub).
Tratamento de erros na leitura com try/except.
Coleta e ordenação dos blocos processados para reconstrução da imagem final.


2.4. Otimização do uso de memória RAM
Durante o processamento de grandes imagens, é fundamental evitar o carregamento de toda a imagem na memória de uma só vez, pois isso pode causar estouro de memória (Out of Memory).

Solução adotada:
A imagem não é carregada completamente na memória.
Em vez disso, são usadas janelas de leitura (rasterio.windows.Window) para ler apenas o bloco correspondente às linhas atribuídas ao processo.
Isso permite um processamento em partes, ideal para imagens grandes.
Além disso, o uso de np.array_split() com blocos menores (8 vezes o número de processos) evita sobrecarga de RAM mesmo em sistemas com menos recursos.

2.5. Entendimento do problema de segmentação
Em algumas aplicações, além da conversão para escala de cinza, é necessário segmentar áreas de interesse na imagem. Isso pode ser feito com:
Espaço de cor HSV: separa cor, saturação e intensidade, útil para destacar regiões específicas.
Limiarização (Thresholding): converte a imagem em preto e branco com base em um valor de corte, útil para detecção de bordas ou regiões específicas.

Solução adotada:
Neste código, a segmentação não utiliza HSV ou limiarização manual, mas           sim uma abordagem muito mais sofisticada com Deep Learning:
Utiliza o modelo DeepLabV3+, carregado via tensorflow_hub.
Esse modelo realiza segmentação semântica automática, reconhecendo e classificando regiões da imagem de forma muito mais precisa que métodos tradicionais como HSV ou thresholding.
O resultado é uma máscara de classes, onde cada pixel recebe um rótulo predito



3.Ferramentas utilizadas
3.1. Linguagem
Python: escolhida pela ampla disponibilidade de bibliotecas de processamento de imagem, facilidade de uso e compatibilidade com bibliotecas MPI via mpi4py.

3.2. Bibliotecas

rasterio: Leitura de imagens .tif, especialmente com dados georreferenciados
opencv (cv2): Manipulação de imagens, conversão de formatos, limiarização
numpy: Operações matriciais de alto desempenho
os: Navegação e manipulação de arquivos e diretórios
time: Medição de tempo de execução
matplotlib.pyplot: Visualização e salvamento de imagens para depuração
mpi4py: Comunicação entre processos MPI em python


4.Como funciona o programa?
O programa segue um fluxo de execução dividido entre os processos MPI, onde o rank 0 atua como coordenador (mestre) e os demais como trabalhadores (slaves).

Fluxo de Execução:
Inicialização com MPI
O programa inicia com mpi4py, detectando o número de processos disponíveis e atribuindo um rank a cada um deles.

Leitura da Imagem (Rank 0)
O rank 0 utiliza a biblioteca rasterio para abrir a imagem .tif.
Ele extrai as informações relevantes da imagem: largura, altura, número de bandas, dados dos canais (RGBA), etc.

Distribuição dos Dados
O rank 0 divide a imagem em partes (ex: faixas horizontais) e envia os blocos e metadados para os demais ranks via comm.send.

Processamento Paralelo
Cada rank trabalhador (rank > 0) recebe sua parte da imagem e:
Converte a parte recebida de RGBA para escala de cinza (Grayscale)
Salva essa parte como uma imagem .jpeg ou .png

Pós-processamento (Rank 0)
O rank 0 também pode salvar sua parte da imagem.
Em seguida, utiliza OpenCV (cv2) para abrir a imagem já convertida e aplicar técnicas de segmentação como:
Conversão para HSV e limiarização
Limiarização adaptativa ou global

Finalização
Todos os processos finalizam e liberam os recursos.
O rank 0 pode exibir ou salvar a imagem segmentada final em um diretório de resultados.


Avaliação de Otimização
5.1. Primeiros resultados
|RANKS  | TEMPOS(s) |  SPEEDUP  | EFICIêNCIA |
|-------|-----------|-----------|------------|
|2      | 30.39     | 0.94      |   46.0     |
|4      | 30.57     |  0.93     |  23.3      |
|5      | 32.13     |  0.89     |   17.      |
|6      | 30.30     |  0.94     |   15.6     |
|7      | 30.77     |  0.93     |   13.3     |
|8      | 30.89     |  0.92     |   11.5     |
|9      | 30.18     |  0.94     |   10.5     |
|10     | 30.17     |  0.95     |    9.5     |
|11     | 30.34     |  0.94     |    8.6     |
|12     | 29.37     |  0.97     |    8.1     |  
|13     | 29.84     |  0.96     |    7.4     |
|14     | 29.65     |  0.96     |    6.8     |
|15     | 29.94     |  0.95     |    6.3     |
|16     | 30.12     |  0.95     |    5.9     |
|17     | 28.69     |  0.99     |    5.8     |
|18     | 30.17     |  0.95     |    5.3     |
|19     | 29.33     |  0.97     |    5.1     |
|20     | 28.36     |  1.01     |    5.0     |
|21     | 30.69     |  0.93     |    4.4     |
|22     | 29.36     |  0.97     |    4.4     |
|23     | 32.23     |  0.88     |    3.8     |
|24     | 30.68     |  0.93     |    3.9     |
|25     | 31.32     |  0.91     |    3.6     |


5.2. Quadro de comparação
|TIPO DE EXECUÇÃO                 | TEMPO(s)        | OBSERVAÇÕES                       |
|---------------------------------|-----------------|-----------------------------------|
|Serial (1 rank)                  |28.51            |  Tempo mais baixo                 |
|Paralelizado (2-25 ranks)        |28.36-32.23      |  Tempos > 30s, ficou mais lento   |
|Melhor tempo paralelo (20 ranks) |28.36            |  Ganho irrelevante                |
|Pior tempo paralelo (23 ranks)   |32.23            |  3.72s mais lento que o serial    |

5.3. Conclusão
O tempo de execução serial foi mais eficiente do que o tempo paralelizado com MPI, ou seja, a estratégia usada para paralelização não está sendo vantajosa para a resolução do problema. 

Localização do código: ./Treino2_1/Treino2_1.py
Tamanho aproximado: 2,7GB

6.Anotação dos Testes de tempo de execução - Treino2_1.py
6.1. Resumo dos tempos de execução

|Execução       |   Tempo(s)  |
|---------------|-------------|
|Serial (1 rank)|    38       |
|2 ranks        |    27       |
|3 ranks        |    24       |
|4 ranks        |    22       |
|5 ranks        |    22       |
|6 ranks        |    21       |
|7 ranks        |    20       |
|8-20 ranks     |    20       |



6.2. Análise de Desempenho
Melhoria inicial constante
Observa-se uma redução significativa no tempo de execução ao aumentar o número de processos de 1 para 4 ranks.
De 38s (serial) para 22s com 4 ranks - uma melhora de aproximadamente 42%
Entre 4 e 6 ranks, os ganhos continuam, porém em ritmo menor

Saturação do Desempenho a partir de 7 ranks
A partir de 7 processos, o tempo estabiliza em 20 segundos, sem apresentar melhorias adicionais até 20 ranks
Isso indica que o limite útil do paralelismo foi atingido
Continuar aumentando o número de processos pode inclusive gerar overhead, sem ganho de performance.

Causas Prováveis de Saturação
Overhead de comunicação MPI: a troca de mensagens entre muitos processos pode impactar negativamente o tempo total
Gargalo de I/O: vários processos acessando simultaneamente o mesmo arquivo grande gera concorrência e limita o desempenho
Tamanho dos blocos: com muitos processos, cada um recebe uma fração menor dos dados, e o tempo gasto com leitura, escrita e sincronização passa a dominar a execução.

6.3. Conclusão Prática
O código treino2_1.py apresenta boa escalabilidade até cerca de 6 ou 7 processos, com ganhos significativos no tempo de execução
Acima de 7 ranks, o desempenho se estabiliza, o que é típico em aplicações com gargalo de I/O ou com pouca carga computacional por processo
Configuração recomendada: utilizar entre 6 e 8 ranks, pois proporciona melhor equilíbrio entre desempenho e uso eficiente de recursos computacionais.



7.Resultados Esperados
Redução de até 80% no tempo de processamento para imagens grandes (comparado com versão sequencial)
Conversão precisa das imagens RGBA para Grayscale
Segmentação clara (quando aplicada)
Baixo uso de memória RAM (evitando crashes)
Código modular e de fácil manutenção

8.Conclusão
Este projeto mostra a importância de unir processamento paralelo com eficiência computacional em tarefas de manipulação de imagens pesadas. A utilização de MPI via Python, aliada a bibliotecas especializadas como Rasterio e OpenCV, permite alcançar alta performance mesmo em máquinas com recursos limitados

