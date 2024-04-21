from sys import argv, exit
from zlib import crc32
from math import ceil
import re

FRAME_BORDER = '01111110'


def str_to_bytes(data: str) -> bytes:
    data = data.ljust(ceil(len(data)/8) * 8, '0')
    output = []

    for i in range(0, int(len(data)/8)):
        b = 0
        for j in range(0, 8):
            if data[i*8+j] == '1':
                b += 2**(7-j)
        output.append(b)

    return bytes(output)


def bytes_to_str(data: bytes) -> str:
    output = ''

    for b in data:
        bb = bin(b)[2:].ljust(8, '0')
        output += bb

    return output


def crc_wrapper(data: str) -> str:

    crc = crc32(str_to_bytes(data))

    return bytes_to_str(crc.to_bytes(4, 'big'))


def encode(data: str) -> str:

    data += crc_wrapper(data)

    data = re.sub(r'11111', '111110', data)

    return FRAME_BORDER + data + FRAME_BORDER


def decode(data: str) -> str:

    data = re.sub(FRAME_BORDER, '', data)

    data = re.sub(r'111110', '11111', data)

    crc = data[-32:]

    if crc != crc_wrapper(data[:-32]):
        raise Exception('invalid CRC => invalid frame')

    return data[:-32]


if __name__ == '__main__':

    if len(argv) < 4:
        exit('usage: main.py input_file output_file -k dla kodowania or -d dla dekodowania')

    input_file = argv[1]
    output_file = argv[2]
    mode = argv[3]
    if mode not in ['-k', '-d']:
        exit('Niepoprawne uzycie')

    with open(input_file, 'r') as fin:
        data = fin.readline().replace('\n', '')
        parsed = encode(data) if mode == '-k' else decode(data)
        with open(output_file, 'w+') as fout:
            fout.write(parsed)
            fout.write('\n')
