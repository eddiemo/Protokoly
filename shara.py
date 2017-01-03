import random
from tkinter.filedialog import *

def gcdex(a, b):
    a0, a1, b0, b1 = 1, 0, 0, 1
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        a0, a1, b0, b1 = b0, b1, a0 - q * b0, a1 - q * b1
    return a0

def inverse(z, p):
    return ((gcdex(z,p) % p + p) % p)

def open_file():
    op = askopenfile()
    op = str(op)
    st = op.find('name=') + 6
    fin = op.find('mode') - 2
    path = op[st:fin]
    return path

def to_bin(n):
    r = []
    while n > 0:
        r.append(n & 1)
        n //= 2
    return r

def test(a, n):
    b = to_bin(n - 1)
    k = 1
    for i in range(len(b) - 1, -1, -1):
        x = k
        k = (k * k) % n
        if k == 1 and x != 1 and x != n - 1:
            return True
        if b[i] == 1:
            k = (k * a) % n
    if k != 1:
        return True
    return False

def is_prime(n, bits):
    if n == 1:
        return False
    for j in range(0, bits):
        a = random.randint(2, n - 1)
        if test(a, n):
            return False
    return True

def gen_p(bits):
    # int(input('Введите битность длинного простого числа: '))
    #print("Идёт генерация...")
    while True:
        p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        while p % 2 == 0:
            p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        while not is_prime(p, bits):
            p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
            while p % 2 == 0:
                p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        p = p * 2 + 1
        if is_prime(p, bits):
            #print("Случайное длинное простое число сгенерировано")
            return p

def gen_prime(start, fin):
    # int(input('Введите битность длинного простого числа: ')
    p = random.randint(start, fin)
    while not is_prime(p, len(to_bin(p))):
        p = random.randint(start, fin)
        while p % 2 == 0:
            p = random.randint(start, fin)
    return p

def gen_gcd(a, b):
    u = [1, 0, a]
    v = [0, 1, b]
    t = [0, 0 ,0]
    while v[2] != 0:
        q, r = divmod(u[2], v[2])
        t = [v[0], v[1], v[2]]
        v = [u[0] - q * v[0], u[1] - q * v[1], u[2] - q * v[2]]
        u = [t[0], t[1], t[2]]
    return [u[2], u[0], u[1]]