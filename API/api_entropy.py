from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import PlainTextResponse
import os
import base64
import hashlib

app = FastAPI()
BUFFER_PATH = "../scanner/entropy_buffer.bin"
MAX_BUFFER_SIZE = 1024 * 1024 * 1024  # 1 GB

def get_entropy(n_bytes: int) -> bytes:
    if not os.path.exists(BUFFER_PATH):
        raise FileNotFoundError("Buffer ainda não foi criado.")

    with open(BUFFER_PATH, "rb") as f:
        data = f.read()

    if len(data) < n_bytes:
        raise ValueError(f"Solicitado {n_bytes}, mas o buffer tem apenas {len(data)} bytes.")

    entropy = data[:n_bytes]
    remaining = data[n_bytes:]

    with open(BUFFER_PATH, "wb") as f:
        f.write(remaining)

    return entropy

def get_buffer_size() -> int:
    return os.path.getsize(BUFFER_PATH) if os.path.exists(BUFFER_PATH) else 0

@app.get("/entropy", response_class=PlainTextResponse)
def read_entropy(
    bytes: int = Query(16, gt=0, le=1024),
    format: str = Query("hex", pattern="^(hex|base64)$")
):
    try:
        entropy = get_entropy(bytes)
        if format == "hex":
            return entropy.hex()
        elif format == "base64":
            return base64.b64encode(entropy).decode()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/entropyExpanded", response_class=PlainTextResponse)
def read_entropy_expanded(
    bytes: int = Query(32, gt=0, le=1024),
    format: str = Query("hex", pattern="^(hex|base64)$")
):
    try:
        base_entropy = get_entropy(32)  # ponto de partida com 32 bytes
        output = bytearray()
        counter = 0

        while len(output) < bytes:
            # SHA-256(base_entropy || counter)
            hasher = hashlib.sha256()
            hasher.update(base_entropy)
            hasher.update(counter.to_bytes(4, 'big'))
            output.extend(hasher.digest())
            counter += 1

        result = output[:bytes]

        if format == "hex":
            return result.hex()
        elif format == "base64":
            return base64.b64encode(result).decode()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/status")
def buffer_status():
    size = get_buffer_size()
    return {
        "available_bytes": size,
        "max_buffer_size": MAX_BUFFER_SIZE,
        "percent_full": round((size / MAX_BUFFER_SIZE) * 100, 2)
    }
