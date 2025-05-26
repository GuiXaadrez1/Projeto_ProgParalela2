'''

# O objetivo deste código é codar python com numpy na prática  para entender seus métodos

'''

if __name__ == "__main__":

    import numpy as np

    # np.arange cria um array unidimensional numpy
    print(np.arange(15))
    
    # criando um array (matriz de duas dimensões ) de 3 linhas  com 5 colunas
    matriz_2d = np.arange(15).reshape(3,5)

    print("Criamos uma matriz n-dimensional: \n", matriz_2d) 

    # np.reshape() reoganiza os elementos dentro de uma matriz


    print(matriz_2d.ndim)
    '''
    
        retorna 2, indicando a dimensão do array, numero de eixos

    '''

    print(matriz_2d.shape)
    
    '''
        retorna as dimensões da matriz. Esta é uma tupla de inteiros
        indicando o tamanho da matriz em cada dimensão 
        O tamanho de uma dimensão se refere ao número de elementos
        que existem em cada eixo (ou dimensão) do array.

        2 → tamanho da primeira dimensão (linhas): o array tem 2 listas internas.

        3 → tamanho da segunda dimensão (colunas): cada lista tem 3 elementos.
    '''

    print(matriz_2d.size) # retorna a quantidade de elementos dentro do array

    print(matriz_2d.dtype.name) # retorna o tipo de dado array int64

    print(matriz_2d.itemsize) # retorna o tamanho em bytes de cada elemento da matriz

   # craindo um array de com numpy de tamanhos diferentes

    array_np = np.array([[1, 2, 3, 4], [1, 2, 3, 4, 5, 7]],dtype=object)

    print(array_np)

    '''
        criamos um array com sublistas de tamanhos diferentes 
        dtype = object adimite que o array tenha tamanhos diferentes
        sem ele o console lança uma mensagem de erro
        e o dtype modifica o tipo de elemetento para objeto
    '''

    # craindo um array de com numpy de tamanhos iguais

    array_np2 = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
    print(array_np2)

    print(type(array_np2))

    # veja que a  classe é <class 'numpy.ndarray'>
    # ou seja é um array do numpy