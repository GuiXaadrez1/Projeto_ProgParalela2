from PIL import Image
import numpy as np
import tifffile

def expand_image_to_7gb(input_path, output_path):
    # Abrir imagem pequena
    img = Image.open(input_path).convert("RGB")
    arr = np.array(img)

    # Estimativa de multiplicador necessário
    bytes_per_pixel = 3  # RGB
    target_size_gb = 20
    target_bytes = target_size_gb * (1024 ** 3)

    # Calcula tamanho da imagem final
    pixels_needed = target_bytes // bytes_per_pixel
    current_pixels = arr.shape[0] * arr.shape[1]
    scale_factor = int(np.ceil(np.sqrt(pixels_needed / current_pixels)))

    # Tile da imagem original
    big_img = np.tile(arr, (scale_factor, scale_factor, 1))

    # Corta para tamanho exato (se necessário)
    h = int(np.sqrt(pixels_needed))
    w = pixels_needed // h
    big_img = big_img[:h, :w, :]

    print(f"Imagem gerada com forma: {big_img.shape} (~{big_img.nbytes / (1024 ** 3):.2f} GB)")

    # Salva como BigTIFF
    tifffile.imwrite(output_path, big_img, bigtiff=True)
    print(f"Imagem salva em: {output_path}")

# Exemplo de uso
expand_image_to_7gb(r"C:\Projeto_ProgParalela2\imagens_satelites\imagem1.jpeg", "output_7gb.tif")
