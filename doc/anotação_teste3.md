1 - O OBJETIVO DESSA ANOTAÇÃO DE TESTE É REALIZAR A MÉDIA ARITIMÉTICA DAS EXECUÇÕES 

    OBS.: O ARQUIVO.TIF POSSUI 2,7 GIGAS

    SERIAL(1 RANK TARBALHANDO) = (38.13 + 38.48 + 38.11 + 38.0 + 37.84 + 37.93 + 38.48 + 36.06 + 38.67 + 37.81)/10 = 37.95

    PARALELIZADO COM 2 RANKS = (25.23 + 24.66 + 24.67 + 24.62 + 24.48 +  25.66 + 24.81 + 24.79 +  24.95 + 24.51 )/10 = 24.84s

    PARALELIZADO COM 3 RANKS = ( 20.51 + 20.44 + 20.71 + 19.97 + 20.24 +  20.13 + 20.26 + 20.29 + 20.22 + 21.03 )/10 = 20.38s 

    PARALELIZADO COM 4 RANKS = ( 19.29 + 18.68 + 19.63 + 18.78 + 19.24 + 20.17 + 19.83 + 19.23 + 19.49 + 18.78 )/10 = 19.31s

    PARALELIZADO COM 5 RANKS = ( 17.75 + 17.91 + 17.46 + 17.95 + 17.28 + 17.63 +  17.53 + 18.02 + 18.16 + 17.84 )/10 = 17.55s

    PARALELIZADO COM 6 RANKS = ( 17.03 + 16.94 + 16.77 + 17.19 + 17.35 + 17.19 + 17.43 + 17.49 + 17.27 + 17.32  )/10 = 17.30s

    PARALELIZADO COM 7 RANKS = ( 16.75 + 16.64 + 16.99 + 17.07 + 16.50 + 16.78 + 17.41 + 17.07 + 16.94 + 17.15 )/10 = 16.93s

    PARALEIZADO COM 8 RANKS = ( 17.16 + )/10 = 

    PARALELIZADO COM 10 RANKS = (  17.28 + )/10 = 

    PARALELIZADO COM 15 RANKS = ( 18.29 + )/10 = 

    PARALELIZADO COM 18 RANKS = ( 18.53 + )/10 = 

    PARALELIZADO COM 20 RANKS = ( 18.41 + )/10 =

2 - DADOS PARA  ANÁLISE DOS PROCESSOS E QUAL É A QUANTIDADE IDEAL PARA ESSA SOLUÇÃO: 

+--------+---------------+----------+------------+
| Ranks  | Tempo (s)     | Speedup  | Eficiência |
+--------+---------------+----------+------------+
|   1    |  37.95        |  1.00    |  1.000     |
|   2    |  24.84        |  1.53    |  0.765     |
|   3    |  20.38        |  1.86    |  0.619     |
|   4    |  19.31        |  1.96    |  0.491     |
|   5    |  17.55        |  2.16    |  0.431     |
|   6    |  17.30        |  2.19    |  0.365     |
|   7    |  16.93        |  2.24    |  0.320     |
+--------+---------------+----------+------------+

Análise:

    O Speedup cresce conforme aumentam os ranks, mas de forma cada vez menos eficiente (lei dos retornos decrescentes).

    A Eficiência cai à medida que mais processos são usados, indicando sobrecarga de paralelismo ou limites do hardware/software para essa tarefa específica.

3 - CONCLUSÃO:


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