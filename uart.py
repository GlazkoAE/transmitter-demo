import array
import random


def transmit_random_data(port, block_length: int):
    random_byte = random.randbytes(block_length)
    port.write(random_byte)


def receive_data(port, block_length: int):
    data = port.read(block_length)
    signed_data = array.array('b')
    signed_data.frombytes(data)
    return signed_data.tolist()


def transmit_and_receive_data(port, block_length):
    transmit_random_data(port, block_length)
    rx_signal = receive_data(port, block_length)
    return rx_signal
