from PIL import Image
import os

def converter_para_tif(pasta_entrada, pasta_saida):
    # Criar pasta de saída, se não existir
    os.makedirs(pasta_saida, exist_ok=True)

    # Extensões de imagem que vamos converter
    extensoes = ('.jpg', '.jpeg', '.png')

    # Percorrer os arquivos da pasta
    for nome_arquivo in os.listdir(pasta_entrada):
        if nome_arquivo.lower().endswith(extensoes):
            caminho_original = os.path.join(pasta_entrada, nome_arquivo)
            nome_sem_ext = os.path.splitext(nome_arquivo)[0]
            caminho_tif = os.path.join(pasta_saida, f"{nome_sem_ext}.tif")

            try:
                with Image.open(caminho_original) as img:
                    img = img.convert("RGB")  # Converte para RGB se não estiver
                    img.save(caminho_tif, format='TIFF')
                    print(f"[OK] Convertido: {nome_arquivo} -> {caminho_tif}")
            except Exception as e:
                print(f"[ERRO] Falha ao converter {nome_arquivo}: {e}")

# Exemplo de uso:
if __name__ == "__main__":
    pasta_entrada = os.path.join(os.getcwd(),"imagens_satelites")
    pasta_saida = "./imagens_convertidas_tif"
    converter_para_tif(pasta_entrada, pasta_saida)
