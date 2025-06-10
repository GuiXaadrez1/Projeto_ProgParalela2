1 - Requisitos e Ferramentas Utilizadas

    Python 3.13 

        Descrição:  Linguagem de programação principal utilizada no projeto
        A versão 3.13 é uma versão mais recente com melhorias de performance e sintaxe.

        Uso: Base para execução de todos os scripts e bibliotecas.
    
    Opencv

        Descrição: Biblioteca de código aberto voltada para visão computacional.

        Uso: anipulação de imagens (leitura, conversão de cor, filtros, transformações, etc.),
        essencial para tarefas de pré-processamento na segmentação.


    rasterio

        Descrição: Biblioteca para leitura e escrita de dados raster 
        (imagens georreferenciadas, como satélites ou drones).

        Uso: Importante para carregar imagens geoespaciais (GeoTIFF, por exemplo) com precisão de coordenadas.
    
    os

        Descrição: Biblioteca padrão do Python para interagir com o sistema operacional.

        Uso: Gerenciamento de diretórios, caminhos de arquivos, e automação de tarefas como leitura em 

    mpi4py

        Descrição: Interface Python para o padrão MPI (Message Passing Interface).

        Uso:  Processamento paralelo distribuído entre múltiplos núcleos ou máquinas.
        Utilizado para acelerar o processamento de imagens grandes ou em lotes.

    time 

        Descrição: Módulo padrão para manipulação de tempo.

        Uso: Medição de tempo de execução, controle de delays, benchmarking de performance.
    
    numpy 

        Descrição:  Biblioteca para computação numérica eficiente em arrays multidimensionais.

        Uso: Manipulação de matrizes de imagens, operações matemáticas rápidas e eficientes.
    
    gc ( Garbage Collector )

        Descrição: Módulo que fornece acesso ao coletor de lixo do Python.

        Uso: Liberação de memória manualmente durante ou após o processamento de grandes quantidades de dados, 
        evitando estouros de memória.
