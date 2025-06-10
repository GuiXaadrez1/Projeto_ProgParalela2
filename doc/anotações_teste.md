Maneira serializada:

Tempo de execução: 28.51 segundos para processar um arquivo de 2,7 GB

Maneira paralelizada com MPI:

2 ranks: 30.39 segundos

3 ranks: 30.84 segundos

4 ranks: 30.57 segundos

5 ranks: 32.13 segundos

6 ranks: 30.30 segundos

7 ranks: 30.77 segundos

8 ranks: 30.89 segundos

9 ranks: 30.18 segundos

10 ranks: 30.17 segundos

11 ranks: 30.34 segundos

12 ranks: 29.37 segundos

13 ranks: 29.84 segundos

14 ranks: 29.65 segundos

15 ranks: 29.94 segundos

16 ranks: 30.12 segundos

17 ranks: 28.69 segundos

18 ranks: 30.17 segundos

19 ranks: 29.33 segundos

20 ranks: 28.36 segundos

21 ranks: 30.69 segundos

22 ranks: 29.36 segundos

23 ranks: 32.23 segundos

24 ranks: 30.68 segundos

25 ranks: 31.32 segundos


Conclusão do Relatório de Desempenho

    Apesar da paralelização com MPI, o ganho de desempenho em relação à execução serial foi mínimo ou inexistente. 
    Em vários casos, a versão paralelizada foi mais lenta do que a versão serial, mesmo utilizando até 25 processos (ranks).

Principais observações:
    
    Execução serial (1 processo): 28.51 s

    Melhor tempo paralelizado (20 ranks): 28.36 s — apenas 0.15 segundos mais rápido que a versão serial.

    Pior tempo paralelizado (23 ranks): 32.23 s — mais de 3.7 segundos mais lento que a versão serial.

    Os tempos com 2 a 10 ranks ficaram consistentemente acima de 30 segundos.

    Não há uma melhoria proporcional com o aumento do número de ranks, indicando overhead de comunicação e/ou subutilização do paralelismo.

Possíveis causas:

    Sobrecarga de comunicação entre os processos MPI supera o ganho de paralelismo.

    I/O de disco (leitura do .tif) pode estar sendo um gargalo, não paralelizável eficientemente.

    O número de blocos fixo (64) pode estar limitando o balanceamento da carga, especialmente quando ranks > 64.

    O processo de montagem da imagem final é feito apenas pelo rank 0, centralizando o trabalho.
