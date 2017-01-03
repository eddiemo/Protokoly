import struct
from tkinter.filedialog import *

def open_file():
    op = askopenfile()
    op = str(op)
    st = op.find('name=') + 6
    fin = op.find('mode') - 2
    path = op[st:fin]
    return path

def hash(path):
    H0 = 0x67452301
    H1 = 0xEFCDAB89
    H2 = 0x98BADCFE
    H3 = 0x10325476
    H4 = 0xC3D2E1F0

    fl = open(str(path), 'rb')
    mes = fl.read()
    start_mes = mes
    cnt_byte = len(mes)
    mes += (128).to_bytes(1, byteorder='big')
    while len(mes) % 64 != 56:
        mes += (0).to_bytes(1, byteorder='big')
    mes += (cnt_byte * 8).to_bytes(8, byteorder='big')

    blcks = []
    cnt_blck = len(mes) // 64
    for i in range(0, cnt_blck):
        blcks.append(mes[i*64 : i*64+64])
    for blck in blcks:
        shiftl = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xffffffff
        w = [0] * 80
        for i in range(0, 16):
            w[i] = struct.unpack(b'>I', blck[i * 4 : i * 4 + 4])[0]

        for i in range(16, 80):
            w[i] = shiftl(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

        A = H0
        B = H1
        C = H2
        D = H3
        E = H4

        for t in range(0, 80):
            if t >= 0 and t <= 19:
                f, K = (B & C) | ((~B) & D), 0x5A827999
            elif t >= 20 and t <= 39:
                f, K = B ^ C ^ D, 0x6ED9EBA1
            elif t >= 40 and t <= 59:
                f, K = (B & C) | (B & D) | (C & D), 0x8F1BBCDC
            elif t >= 60 and t <= 79:
                f, K = B ^ C ^ D, 0xCA62C1D6

            E, D, C, B, A = D, C, shiftl(B, 30), A, shiftl(A, 5) + f + E + K + w[t] & 0xffffffff

        H0 = (H0 + A) & 0xffffffff
        H1 = (H1 + B) & 0xffffffff
        H2 = (H2 + C) & 0xffffffff
        H3 = (H3 + D) & 0xffffffff
        H4 = (H4 + E) & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (H0, H1, H2, H3, H4)