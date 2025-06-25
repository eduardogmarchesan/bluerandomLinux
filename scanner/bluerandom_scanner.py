from bluepy.btle import Scanner, DefaultDelegate
import time
import os

BUFFER_PATH = "entropy_buffer.bin"
MAX_BUFFER_SIZE = 1024 * 1024 * 1024  # tamanho máximo do buffer em bytes

bit_buffer = []  # buffer auxiliar para armazenar bits até formar bytes

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()

def get_rssi_values(scan_time=3):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(scan_time)

    rssi_list = []

    for dev in devices:
        rssi_list.append(dev.rssi)
        name = None
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Complete Local Name":
                name = value
                break

        if name:
             print(f" {dev.addr} RSSI={dev.rssi} dB  Nome: {name}")
        else:
            print(f" {dev.addr} RSSI={dev.rssi} dB  Nome: [indisponível]")

    return rssi_list

def odd_or_even_extractor(rssi_values):
    return [0 if rssi % 2 == 0 else 1 for rssi in rssi_values]

def convert_bits_to_bytes():
    global bit_buffer
    byte_array = bytearray()
    while len(bit_buffer) >= 8:
        byte_bits = bit_buffer[:8]
        del bit_buffer[:8]
        byte = int("".join(str(b) for b in byte_bits), 2)
        byte_array.append(byte)
    return byte_array

def get_buffer_size():
    return os.path.getsize(BUFFER_PATH) if os.path.exists(BUFFER_PATH) else 0

def save_entropy(byte_array):
    byte_len = len(byte_array)
    buffer_size = get_buffer_size()

    if buffer_size + byte_len > MAX_BUFFER_SIZE:
        with open(BUFFER_PATH, "rb") as f:
            data = f.read()
        remaining = data[byte_len:]
        with open(BUFFER_PATH, "wb") as f:
            f.write(remaining)
        print(f"Buffer cheio: removidos {byte_len} bytes antigos para liberar espaço.")

    with open(BUFFER_PATH, "ab") as f:
        f.write(byte_array)

    new_size = get_buffer_size()
    print(f"{byte_len} bytes salvos no buffer (total: {new_size} bytes)\n")

def main():
    global bit_buffer

    while True:
        rssi_vals = get_rssi_values(scan_time= 0.1)
        bits = odd_or_even_extractor(rssi_vals)
        bit_buffer.extend(bits)

        byte_array = convert_bits_to_bytes()

        print(f"Extraídos {len(bits)} bits | Acumulados: {len(bit_buffer)} bits restantes no buffer")
        print(f"Convertidos: {len(byte_array)} bytes")

        if byte_array:
            save_entropy(byte_array)

        #time.sleep(1)

if __name__ == "__main__":
    main()
