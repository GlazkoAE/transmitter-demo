import random


def hex2signed(hex_str, bits=16):
    value = int(hex_str, 16)
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value


def transmit_random_data(port, block_length: int):
    random_byte = random.randbytes(block_length)
    port.write(random_byte)


def receive_data(port, block_length: int, bytes_per_sample=2):
    signed_data = []
    data = port.read(block_length).hex()
    for index in range(0, len(data), 2 * bytes_per_sample):
        hex_sample = data[index: index + 2 * bytes_per_sample]
        int_sample = hex2signed(hex_sample, 8*bytes_per_sample)
        signed_data.append(int_sample)
    return signed_data


def transmit_and_receive_data(port, block_length, is_single_byte=False, bytes_per_sample=2):
    if is_single_byte:
        rx_signal = []
        for _ in range(block_length):
            transmit_random_data(port, 1)
            rx_signal += receive_data(port, 1)
    else:
        transmit_random_data(port, block_length)
        rx_signal = receive_data(port, block_length, bytes_per_sample=bytes_per_sample)

    return rx_signal
