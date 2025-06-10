O objetivo dessa anotação é criar um ambiente de desenvolvimento com
as tecnologias e ferramentas descritas na pasta: 
    
    C:\Projeto_ProgParalela2\doc\Requerimentos_Ferramentas.md


1 - Pré-Requisitos: 

    - Python na versão 3.13 instalado e devidamente configurado na máquina

   - MPI instalado: 
   
        Você precisa instalar duas partes:

            
            MS-MPI Redistributable Package (Runtime) — necessário para executar programas MPI.
                (msmpisetup.exe)

            MS-MPI SDK (Software Development Kit) — necessário para compilar/instalar mpi4py.
                (msmpisdk.msi)

        Links diretos da Microsoft:

            Runtime: https://www.microsoft.com/en-us/download/details.aspx?id=105289

        Dica: 

            SDK: Mesmo link acima, procure por msmpisdk.msi

            Dica: Instale primeiro o runtime, depois o SDK.
        

2 - Instalar as libs pelo gerenciador de pacotes pip

    pip install opencv-python 
    
    pip install rasterio 
    
    pip  install mpi4py 
    
    pip install numpy

3 - Ensiando a rodar o seu script com mpi:

    mpiexec -n 4 python3.13 seu_script.py


    observação: deve ser dentro da pasta do seu projeto, exemplo:

        PS C:\Projeto_ProgParalela2\programas> mpiexec -n 4 python3.13 Producao3.py 


