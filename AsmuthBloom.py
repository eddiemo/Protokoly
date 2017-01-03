import random
import shara
from functools import *

print("Привеееет :)")
while True:
    mode = input("Выберите режим: 1 - разделение секрета, 2 - восстановление секрета\n")

    if mode == "1":
        secret = int(input("Введите число для засекречивания: "))

        n = int(input("Введите количество участников: "))
        m = int(input("Введите количество участников, необходимое для восстановления секрета: "))

        while True:

            p = shara.gen_prime(secret, 2**(len(shara.to_bin(secret)) + 10))
            d = []
            x = p + 2
            for i in range(0, n):
                x = shara.gen_prime(x, 2**(len(shara.to_bin(secret)) + 10))
                d.append(x)
                x += 2

            dmsum1 = reduce(lambda x, y: x * y, d[:m])
            dmsum2 = p * reduce(lambda x, y: x * y, d[n-m+2:])
            if dmsum1 < dmsum2:
                continue

            r = random.randint(1, (dmsum1 - secret) // p)
            s = secret + r * p

            k = [s % di for di in d]

            f = open("AB.txt", "w")
            for i in range(n):
                f.write(str(p) + " " + str(d[i]) + " " + str(k[i]) + "\n")
            f.close()
            break

    elif mode == "2":
        m = int(input("Введите количество участников восстановления секрета: "))

        p = 0
        pset = set()
        d = []
        k = []
        print("Введите " + str(m) + " долей:")
        for i in range(m):
            data = input()
            datasplt = data.split(' ')
            p = int(datasplt[0])
            pset.add(int(datasplt[0]))
            d.append(int(datasplt[1]))
            k.append(int(datasplt[2]))
        if len(pset) > 1:
            print("Восстановление не завершено. Неверные данные")
            break
        dmul = reduce(lambda x,y: x * y, d)
        dj = [dmul // di for di in d]
        djinv = [shara.inverse(dj[i], d[i]) for i in range(m)]
        s = reduce(lambda x,y: (x + y) % dmul,[k[i] * dj[i] * djinv[i] for i in range(m)])

        secret = s % p
        print(secret)

    else:
        continue

    y = input("Продолжить работу программы? 1 - да, 2 - нет: ")
    while y != "1" and y != "2":
        y = input("Неверные данные. Продолжить работу программы? 1 - да, 2 - нет: ")
    if y == "1":
        continue
    else:
        print("Пока ;)")
        exit(0)
