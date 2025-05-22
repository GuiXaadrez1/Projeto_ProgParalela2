import rasterio
import matplotlib.pyplot as plt

# Caminho da imagem
IMAGEM_PATH = r"C:\Projeto_ProgParalela2\imagens_satelites\satelit_google.tif"

# Abrir a imagem com rasterio
with rasterio.open(IMAGEM_PATH) as src:
    # Obter dimensões da imagem
    largura = src.width
    altura = src.height
    
    # Definir o tamanho da janela (ex: metade da imagem)
    janela = rasterio.windows.Window(0, 0, largura // 2, altura // 2)
    
    # Ler apenas a janela especificada
    imagem = src.read(1, window=janela)

# Exibir a imagem em tons de cinza
plt.figure(figsize=(10, 8))
plt.imshow(imagem, cmap='gray')
plt.title("Imagem em Escala de Cinza - Janela")
plt.axis('off')
plt.colorbar(label="Valor do Pixel")
plt.show()
