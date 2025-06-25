################# usado para testes ####################

import sys
import base64
from typing import Literal

BUFFER_PATH = "entropy_buffer.bin"

def get_entropy(n_bytes: int, output: Literal["hex", "base64"] = "hex") -> str:
    with open(BUFFER_PATH, "rb") as f:
        data = f.read()

    if len(data) < n_bytes:
        raise ValueError(f"Buffer o número de bytes solicitados.")

    entropy = data[:n_bytes]
    remaining = data[n_bytes:]

    with open(BUFFER_PATH, "wb") as f:
        f.write(remaining)

    if output == "hex":
        return entropy.hex()
    elif output == "base64":
        return base64.b64encode(entropy).decode()
    else:
        raise ValueError("Formato de saída inválido. Use 'hex' ou 'base64'.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 get_entropy.py <quantidade_bytes> [hex|base64]")
        sys.exit(1)

    n = int(sys.argv[1])
    output_format = sys.argv[2] if len(sys.argv) > 2 else "hex"

    try:
        result = get_entropy(n, output_format)
        print(result)
    except Exception as e:
        print(f"[ERRO] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
