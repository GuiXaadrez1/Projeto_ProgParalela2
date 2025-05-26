'''

    O objetivo de bloco de código é aprender formas de criar array com o numpy

'''

import numpy as np

# criando lista e tuplas comum do python
lista = [1,3,4,5,6,] 
tupla = [1.0,2.0,4.0,5.0,6.0]

# usando o método array do numpy para transformar
# listas e tuplas em um array do numpy

array_np_lista = np.array(lista)

print(array_np_lista)

array_np_tupla = np.array(tupla)

print(array_np_tupla)

# descobrindo as dimensões do array e seus tipos de dados

print(array_np_lista.ndim) # 1 
print(array_np_tupla.ndim) # 1 

print(array_np_lista.dtype) # int32 
print(array_np_tupla.dtype) # float64


# Podemos fazer diretamente no método(objeto) também
print(np.array([1,2,3,4,5,6,7,8]))

# craindo um array de duas dimensões de mesmo tamanho
array_2d = np.array([[1,2,3,4,5],[6,7,8,9,10]])
print(array_2d)
print(array_2d.ndim)

# Criando um array que admite tamanhos diferentes nas sublistas
array_2d = np.array([[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6]], dtype=object)

print(array_2d)
print(array_2d.dtype)  # Retorna 'object', pois os elementos são listas de tamanhos diferentes
print(array_2d.ndim)   # Retorna 1, pois com dtype=object e tamanhos diferentes, vira um array unidimensional

# Isso acontece porque arrays NumPy não suportam nativamente subarrays de tamanhos diferentes

# Criando um array com somente zeros

print(np.zeros((2,3)))

# Criando um array somente com um
print(np.ones((4,2,4)))

# Criando um array aleatório com empty
print(np.empty((2,3),dtype=float))

# Lembrando que podemos especificas os tipos de dados de cada array no momento da sua criação

