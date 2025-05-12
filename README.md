# Bluerandom Entropy Service

Este projeto implementa um serviço de entropia baseado em RSSI via Bluetooth, utilizando um Raspberry Pi 4 como fonte. Ele coleta valores de RSSI, extrai bits aleatórios e os disponibiliza via API REST.

---

## Requisitos

- Python 3.9+
- Raspberry Pi OS (ou outra distribuição Linux com suporte Bluetooth)
- Adaptador Bluetooth compatível (ex: embutido no Raspberry Pi 4)

### Dependências do sistema:

```bash
sudo apt update
sudo apt install -y bluetooth bluez libbluetooth-dev libglib2.0-dev python3-pip python3-venv build-essential
```

---

## Ambiente Python

### Criação do ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalação das dependências Python:

```bash
pip install bluepy fastapi uvicorn
```

---

## Execução

### 1. Scanner BLE (gerador de entropia)

Este script coleta RSSI, extrai bits e gera entropia em `entropy_buffer.bin`.

```bash
source venv/bin/activate
python3 bluerandom_scanner.py
```

Deixe este script rodando continuamente em segundo plano.

---

### 2. API REST

Expõe a entropia via HTTP usando FastAPI e Uvicorn.

```bash
source venv/bin/activate
uvicorn api_entropy:app --host 0.0.0.0 --port 8000
```

---

## Endpoints da API

### `/entropy`
Retorna entropia bruta diretamente do buffer:

```
GET /entropy?bytes=32&format=hex
```

- `bytes`: número de bytes a retornar (ex: 16, 32, 64)
- `format`: `hex` (padrão) ou `base64`

---

### `/entropyExpanded`
Retorna entropia derivada via SHA-256, útil para ampliar aleatoriedade:

```
GET /entropyExpanded?bytes=64&format=base64
```

---

### `/status`
Mostra a situação atual do buffer de entropia:

```
GET /status
```

Exemplo de resposta:

```json
{
  "available_bytes": 512,
  "max_buffer_size": 1073741824,
  "percent_full": 0.05
}
```


## 🧠 Observações

- O sistema utiliza um buffer de bits auxiliar para maximizar o aproveitamento da entropia mesmo em ciclos curtos com poucas leituras.
- O buffer é gerenciado com tamanho máximo definido (1 GB por padrão).
- O script `get_entropy.py` é útil para testes locais sem usar a API.

---

## 📚 Referência

Baseado no artigo:

**An Entropy Source based on the Bluetooth Received Signal Strength Indicator**  
_Alexandre Giron, Ricardo Custódio_

https://sol.sbc.org.br/index.php/sbseg/article/view/19231
