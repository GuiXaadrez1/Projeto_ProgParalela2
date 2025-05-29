O objetivo e fazer uma anotação de testes de tempo de execução do código Treino2_1.py
que se encontra na pasta Treino2_1

Maneira serializada:

    - Tempo de execução: 38s

Maneiras paralelizadas com MPI:

    2 rank - 27s
    3 rank - 24s
    4 rank - 22s
    5 rank - 22s
    6 rank - 21s
    7 rank - 20s
    8 rank - 20s
    9 rank - 20s
    10 rank - 20s
    20 rank - 20s


Com base nos resultados dos testes de tempo de execução do código Treino2_1.py, aplicado a um arquivo de 2,7 GB, podemos tirar a seguinte 
conclusão sobre a escalabilidade do seu processamento paralelo com MPI:

Resumo dos tempos de execução
Execução	Tempo (s)
Serial (1 rank)	38
2 ranks	27
3 ranks	24
4 ranks	22
5 ranks	22
6 ranks	21
7 ranks	20
8–20 ranks	20

Análise de desempenho

        Melhoria inicial consistente:

            A performance melhora de forma notável ao aumentar os ranks de 1 para 4, 
            com uma redução de 38s para 22s (~42% mais rápido).
            A partir de 4 ranks, os ganhos se tornam marginais.

        Saturação do desempenho a partir de 7 ranks:

            O tempo estabiliza em 20 segundos com 7 ou mais ranks, 
            indicando que o paralelismo atingiu seu limite útil para esse caso.

            Adicionar mais processos não traz benefícios adicionais — e pode até introduzir overhead desnecessário.

        Causas prováveis da saturação:

            Overhead de comunicação MPI (envio/recebimento de blocos processados).

            Gargalo de I/O: múltiplos processos acessando o mesmo arquivo grande simultaneamente.

            Tamanho dos blocos: com blocos muito pequenos por processo, o tempo de leitura/escrita e sincronização passa a dominar o tempo de computação útil.

        Conclusão prática

            Seu código Treino2_1.py escala bem até aproximadamente 6 ou 7 processos, com ganhos relevantes de tempo. 
            A partir daí, a eficiência paralela se estabiliza, o que é comum em pipelines limitados por I/O ou por carga computacional pequena por processo.

            Ideal para esse cenário: entre 6 a 8 ranks, pois oferece um bom equilíbrio entre desempenho e uso eficiente de recursos computacionais.