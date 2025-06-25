from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import os
import math

def gerar_com_chacha20(seed: bytes, tamanho: int, arquivo_saida: str = "prng_output.bin") -> None:
    if len(seed) < 32:
        seed = seed.ljust(32, b'\x00')  # ChaCha20 requer chave de 256 bits

    chave = seed[:32]
    nonce = os.urandom(16)  # 96 bits de nonce

    algoritmo = algorithms.ChaCha20(chave, nonce)
    cifra = Cipher(algoritmo, mode=None, backend=default_backend())
    encriptador = cifra.encryptor()

    bloco_tamanho = 1024 * 1024 * 10  # 10 MB por bloco
    blocos_totais = math.ceil(tamanho / bloco_tamanho)

    with open(arquivo_saida, 'wb') as f:
        for i in range(blocos_totais):
            restante = tamanho - (i * bloco_tamanho)
            bloco_real = min(bloco_tamanho, restante)
            dados = encriptador.update(b'\x00' * bloco_real)
            f.write(dados)

            porcentagem = ((i + 1) / blocos_totais) * 100
            print(f"[{arquivo_saida}] Progresso: {porcentagem:.1f}%")

    print(f"Arquivo '{arquivo_saida}' gerado com {tamanho} bytes de PRNG ChaCha20.")
    
with open("entropy_buffer.bin", "rb") as f:
    buffer_original = f.read()

# Gera 1 GB de saída PRNG com progresso
gerar_com_chacha20(buffer_original[:32], 1024 * 1024 * 1024 , "prng_1gb.bin")
