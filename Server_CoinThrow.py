import socket
import shara
import random

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)

print("Ждём подключение...")
while True:
    conn, addr = sock.accept()
    print("Соединение установлено")

    print("Генерация p")
    p = shara.gen_p(200)
    q = (p - 1) // 2
    while not shara.is_prime(q, len(shara.to_bin(q))):
        p = shara.gen_p(200)
        q = (p - 1) / 2
    print("p сгенерировано =", p)
    print("q =", q)

    conn.send(('p ' + str(p)).encode('utf-8'))

    data = (conn.recv(10240)).decode()
    if not data:
        print("Ошибка. Соединение закрыто")
        conn.close()
        continue

    datasplt = data.split(' ')
    if datasplt[0] != 'primitive' or len(datasplt) == 0:
        print("Ошибка. Соединение закрыто")
        conn.close()
        continue
    h = int(datasplt[1])
    t = int(datasplt[2])
    print("Принятые h и t: ", h, t)

    if (pow(h, (p - 1) // q, p) == 1 and pow(h, (p - 1) // 2, p) == 1):
        print("Ошибка. Соединение закрыто")
        conn.close()
        continue
    if (pow(t, (p - 1) // q, p) == 1 and pow(t, (p - 1) // 2, p) == 1):
        print("Ошибка. Соединение закрыто")
        conn.close()
        continue
    print(h, "и", t, "примитивные")

    x = random.randint(2, p)
    while (shara.gen_gcd(x, p - 1)[0] != 1):
        x = random.randint(2, p)
    print("x =",x)
    coin = random.getrandbits(1)
    if coin:
        print("Выбрана h")
        choice = 'h'
        y = pow(h, x, p)
    else:
        print("Выбрана t")
        choice = 't'
        y = pow(t, x, p)
    print("y =", y)

    conn.send(('y ' + str(y)).encode('utf-8'))

    data = (conn.recv(10240)).decode()
    if not data:
        print("Ошибка. Соединение закрыто")
        conn.close()
        continue

    datasplt = data.split(' ')
    if datasplt[0] != 'choice' or len(datasplt) == 0:
        print("Ошибка. Соединение закрыто")
        conn.close()
        continue
    if datasplt[1] == choice:
        print("Угадал. Орёл.")
        conn.send(('result eagle ' + str(x)).encode('utf-8'))
    else:
        print("Не угадал. Решка.")
        conn.send(('result tails ' + str(x)).encode('utf-8'))