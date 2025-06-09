1 - O OBJETIVO DESSA ANOTAÇÃO DE TESTE É REALIZAR A MÉDIA ARITIMÉTICA DAS EXECUÇÕES  dDO PROGRAMA Producao.py

    OBS.: O ARQUIVO.TIF POSSUI 2,7 GIGAS

    SERIAL(1 RANK TARBALHANDO) = (38.13 + 38.48 + 38.11 + 38.0 + 37.84 + 37.93 + 38.48 + 36.06 + 38.67 + 37.81)/10 = 37.95

    PARALELIZADO COM 2 RANKS = (25.23 + 24.66 + 24.67 + 24.62 + 24.48 +  25.66 + 24.81 + 24.79 +  24.95 + 24.51 )/10 = 24.84s

    PARALELIZADO COM 3 RANKS = ( 20.51 + 20.44 + 20.71 + 19.97 + 20.24 +  20.13 + 20.26 + 20.29 + 20.22 + 21.03 )/10 = 20.38s 

    PARALELIZADO COM 4 RANKS = ( 19.29 + 18.68 + 19.63 + 18.78 + 19.24 + 20.17 + 19.83 + 19.23 + 19.49 + 18.78 )/10 = 19.31s

    PARALELIZADO COM 5 RANKS = ( 17.75 + 17.91 + 17.46 + 17.95 + 17.28 + 17.63 +  17.53 + 18.02 + 18.16 + 17.84 )/10 = 17.55s

    PARALELIZADO COM 6 RANKS = ( 17.03 + 16.94 + 16.77 + 17.19 + 17.35 + 17.19 + 17.43 + 17.49 + 17.27 + 17.32  )/10 = 17.30s

    PARALELIZADO COM 7 RANKS = ( 16.75 + 16.64 + 16.99 + 17.07 + 16.50 + 16.78 + 17.41 + 17.07 + 16.94 + 17.15 )/10 = 16.93s

    PARALEIZADO COM 8 RANKS = ( 17.16 + 19.75 + 17.26 + 17.30 + 18.42 + 17.11 + 16.98 + 16.85 + 17.70 + 18.02 )/10 = 17.56s

    PARALELIZADO COM 10 RANKS = (  17.28 + 17.40 + 29.25 + 23.83 + 17.17 + 17.65 + 16.76 + 17.53 + 17.06 + 17.48 )/10 = 17.34s

    PARALELIZADO COM 15 RANKS = ( 18.29 + 17.72 + 17.81 + 18.26 + 17.49 + 17.45 + 17.56 + 17.98 + 17.51 + 17.64 )/10 = 17.57s

    PARALELIZADO COM 18 RANKS = ( 18.53 + 18.11 + 18.70 + 17.92 + 18.18 + 17.76 + 18.19 + 19.02 + 18.0 + 17.59 )/10 = 17.90s

    PARALELIZADO COM 20 RANKS = ( 18.41 + 17.01 + 17.88 + 18.18 + 17.57 + 17.62 + 18.11 + 17.80 + 17.79 + 18.25 )/10 = 17.56s

2 - DADOS PARA  ANÁLISE DOS PROCESSOS E QUAL É A QUANTIDADE IDEAL PARA ESSA SOLUÇÃO: 

+-----------+----------------+---------+-------------+
| Ranks     | Tempo Médio (s)| Speedup | Eficiência  |
+-----------+----------------+---------+-------------+
| 1         | 37.95          | 1.00    | 100.00 %    |
| 2         | 24.84          | 1.53    | 76.50 %     |
| 3         | 20.38          | 1.86    | 62.00 %     |
| 4         | 19.31          | 1.96    | 49.00 %     |
| 5         | 17.55          | 2.16    | 43.20 %     |
| 6         | 17.30          | 2.19    | 36.50 %     |
| 7         | 16.93          | 2.24    | 32.00 %     |
| 8         | 17.56          | 2.16    | 27.00 %     |
| 10        | 17.34          | 2.19    | 21.90 %     |
| 15        | 17.57          | 2.16    | 14.40 %     |
| 18        | 17.90          | 2.12    | 11.78 %     |
| 20        | 17.56          | 2.16    | 10.80 %     |
+-----------+----------------+---------+-------------+s



DEFINIÇÕES IMPORTANTES:
    
    Tempo Médio (s): Tempo médio de execução da tarefa para determinado número de processos.

    Speedup: Razão entre o tempo de execução sequencial e o tempo paralelo:  

        Speedup = ( tempo serial / tempo paralelizado )
    
    Eficiência (%): Mede o quanto os processos estão sendo utilizados de maneira eficaz:

        Eficiência = ( speedup/quantidade_processos ) * 100 

OBSERVAÇÕES:


    O Speedup cresce conforme aumentam os ranks, mas de forma cada vez menos eficiente (lei dos retornos decrescentes).

    A Eficiência cai à medida que mais processos são usados, indicando sobrecarga de paralelismo ou limites do hardware/software para essa tarefa específica.

    O Speedup foi calculado por: Speedup = TempoSerial / TempoParalelo

    A Eficiência foi calculada por: Eficiência = (Speedup / Ranks) * 100

    A eficiência naturalmente tende a cair à medida que se aumentam os ranks, especialmente quando o overhead de paralelização e I/O supera os ganhos computacionais.


ANÁLISE DETALHADA:


    Resumo dos Dados:

        Tempo serial médio (1 rank): 37,95 segundos

        Menor tempo paralelo observado: 16,93 segundos com 7 ranks

        Melhor speedup observado: 2,24× com 7 ranks

        Testes realizados com 1 a 20 ranks 


    A tabela apresenta uma análise de desempenho de um algoritmo ou aplicação paralela em função do número de ranks (processos paralelos). 
    São mostrados o tempo médio de execução, o speedup obtido e a eficiência da execução paralela para diferentes quantidades de ranks. 
    Abaixo, segue uma análise detalhada:


        1 a 4 Ranks: Boa Escalabilidade Inicial:

            Há um ganho expressivo de desempenho até 4 processos.

            Contudo, mesmo com apenas 4 ranks, a eficiência já começa a cair (de 100% para 49%), indicando overhead de paralelização crescente.

        5 a 8 Ranks: Diminuição Acentuada da Eficiência:

            A partir de 5 ranks, o tempo não melhora significativamente.

            A eficiência despenca — isso aponta que os custos de comunicação e sincronização estão superando os benefícios da divisão de trabalho.

        10 a 20 Ranks: Saturação Completa:

            A partir de 10 processos, não há praticamente nenhum ganho adicional em tempo.

            Eficiência muito baixa (< 15%) — significa que recursos estão sendo desperdiçados.
    

RESUMO CONCEITUAL  (TENDÊNCIA):

    Speedup: Cresce rapidamente até 4-5 processos, depois estabiliza.

    Eficiência: Decai exponencialmente conforme o número de processos aumenta.


CONCLUSÕES E RECOMENDAÇÕES:

    Escalabilidade limitada: A aplicação escala bem até cerca de 4 processos. Depois disso, há uma saturação clara.

    Ponto ótimo: 4 ou 5 processos parece ser o ponto de melhor custo-benefício. Acima disso, o ganho em tempo é marginal, mas o custo computacional aumenta.

    Gargalos prováveis: Overhead de comunicação entre processos.

    Seção crítica não paralelizável (lei de Amdahl).

    Latência de sincronização.


3 - CONCLUSÃO TÉCINICA:


    Ideal técnico (bom balanceamento): 3 Ranks

        Speedup: 1.86

        Eficiência: 0.619

        Boa relação ganho/custo.

    Limite prático antes de retornos marginais: 5 Ranks

        Speedup: 2.16

        Eficiência: 0.431

    Após isso, o ganho de tempo quase não compensa o uso de mais recursos.

    Recomendação:

        Use 3 Ranks se busca eficiência equilibrada.

        Use até 5 Ranks se o foco for reduzir o tempo ao máximo com recursos disponíveis.

        Evite mais de 5 se estiver preocupado com consumo de recursos ou escalabilidade real.