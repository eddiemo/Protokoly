import sha1
import random

class PrivateKey(object):
    def __init__(self, p = None, g = None, x = None):
        self.p = p
        self.g = g
        self.x = x

class PublicKey(object):
    def __init__(self, p = None, g = None, y = None):
        self.p = p
        self.g = g
        self.y = y

class Signature(object):
    def __init__(self, mes = None, r = None, s = None):
        self.mes = mes
        self.r = r
        self.s = s

def gcd(a, b):
    while b:
        a %= b
        a, b = b, a
    return a

def gcdex(a, b):
    a0, a1, b0, b1 = 1, 0, 0, 1
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        a0, a1, b0, b1 = b0, b1, a0 - q * b0, a1 - q * b1
    return a0

def inverse(z, p):
    return ((gcdex(z,p) % p + p) % p)

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

def gen_p():
    bits = 0
    while (bits < 161):
        bits = int(input('Введите битность числа p: '))
    print("Идёт генерация числа p...")
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
            print("Случайное длинное число p сгенерировано")
            return p

def gen_keys():
    print("Идёт генерация ключей...")
    p = gen_p()
    g = random.randint(2, p-1)
    x = random.randint(1, p)
    y = pow(g, x, p)

    pubkey = PublicKey(p, g, y)
    privkey = PrivateKey(p, g, x)

    print("Генерация ключей завершена")
    return privkey, pubkey

def sign(privkey, mes):
    print("Идёт подпись сообщения...")
    m = int(sha1.hash(mes), 16)
    _p = int(privkey.p)
    _g = int(privkey.g)
    _x = int(privkey.x)
    p1 = _p - 1
    k = random.randint(1, p1)
    while gcd(k, p1) != 1:
        k = random.randint(1, p1)
    r = pow(_g, k, _p)
    x1 = (_x * r) % p1
    x2 = (m - x1) % p1
    s = (x2 * inverse(k, p1)) % p1
    signmes = Signature(mes, r, s)
    print("Подпись готова")
    return signmes

def verify(pubkey, signmes):
    print("Идёт проверка подписи...")
    _p = int(pubkey.p)
    _g = int(pubkey.g)
    _y = int(pubkey.y)
    _r = int(signmes.r)
    _s = int(signmes.s)
    if 0 < _r < _p and 0 < _s < _p - 1:
       pass
    else:
        return False
    m = int(sha1.hash(signmes.mes), 16)
    v1 = (pow(_y, _r, _p) * pow(_r, _s, _p)) % _p
    v2 = pow(_g, m, _p)
    if v1 == v2:
        return True
    else:
        return False

if __name__ == '__main__':
    while True:
        #file_mes = sha1.open_file()
        ans = input("Выберите режим работы программы:\n 1 - генерация ключей\n 2 - подпись файла\n 3 - проверка подписи\n")
        if ans == "1":
            priv, pub = gen_keys()

            file_pub = open("public_keys.txt", "w")
            file_pub.write(str(pub.p) + "\n")
            file_pub.write(str(pub.g) + "\n")
            file_pub.write(str(pub.y) + "\n")
            file_pub.close()

            file_priv = open("private_keys.txt", "w")
            file_priv.write(str(priv.p) + "\n")
            file_priv.write(str(priv.g) + "\n")
            file_priv.write(str(priv.x) + "\n")
            file_priv.close()

            ans = input("Хотите продолжить работу программы? (да/нет) ")
            if ans == "да":
                continue
            else:
                break

        elif ans == "2":
            print("Выберите файл c private_keys")
            file = sha1.open_file()
            file_priv = open(file, "r")
            p = file_priv.readline()
            g = file_priv.readline()
            x = file_priv.readline()
            privkey = PrivateKey(p, g, x)
            file_priv.close()

            print("Выберите файл-сообщение")
            file = sha1.open_file()
            signmes = sign(privkey, file)
            file_sign = open("signature.txt", "w")
            file_sign.write(str(signmes.r) + "\n")
            file_sign.write(str(signmes.s) + "\n")
            file_sign.close()

            ans = input("Хотите продолжить работу программы? (да/нет) ")
            if ans == "да":
                continue
            else:
                break

        elif ans == "3":
            print("Выберите файл c public_keys")
            file = sha1.open_file()
            file_pub = open(file, "r")
            p = file_pub.readline()
            g = file_pub.readline()
            y = file_pub.readline()
            pubkey = PublicKey(p, g, y)
            file_pub.close()

            print("Выберите файл с подписью")
            file = sha1.open_file()
            file_sign = open(file, "r")
            r_tmp = int(file_sign.readline())
            s_tmp = int(file_sign.readline())
            file_sign.close()

            print("Выберите файл-сообщение")
            file = sha1.open_file()
            signmes = Signature(mes = file, r = r_tmp, s = s_tmp)
            if verify(pubkey, signmes):
                print("Проверка прошла успешно")
            else:
                print("Проверка не пройдена")

            ans = input("Хотите продолжить работу программы? (да/нет) ")
            if ans == "да":
                continue
            else:
                break

        elif ans == "4":
            break