from bluepy.btle import Scanner, DefaultDelegate
import time

BUFFER_PATH = "entropy_buffer.bin"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()

def get_rssi_values(scan_time = 3):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(scan_time)

    # Ordenar por força de sinal (RSSI decrescente)
    devices_sorted = sorted(devices, key=lambda dev: dev.rssi, reverse=True)
    rssi_list = []

    for dev in devices_sorted:
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
    """
    Extrai bits com base no valor par/ímpar do RSSI.
    """
    bits = []
    for rssi in rssi_values:
        bits.append(0 if rssi % 2 == 0 else 1)
    return bits

def bits_to_bytes(bits):
    """
    Agrupa bits em bytes (8 bits por byte).
    """
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) == 8:
            byte = int("".join(str(b) for b in chunk), 2)
            byte_array.append(byte)
    return byte_array

def save_entropy(byte_array):
    with open(BUFFER_PATH, "ab") as f:
        f.write(byte_array)

def main():
    while True:
        rssi_vals = get_rssi_values(scan_time=3)
        bits = odd_or_even_extractor(rssi_vals)
        byte_array = bits_to_bytes(bits)

        print(f"Extraídos {len(bits)} bits = {len(byte_array)} bytes")

        if byte_array:
            save_entropy(byte_array)
            print(f" {len(byte_array)} bytes salvos no buffer '{BUFFER_PATH}'\n")

        time.sleep(1)

if __name__ == "__main__":
    main()
