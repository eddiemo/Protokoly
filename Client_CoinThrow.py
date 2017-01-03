import random
import socket
import shara

sock = socket.socket()
sock.connect(('localhost', 9090))
print("Соединение установлено")

data = (sock.recv(10240)).decode()
if not data:
    print("Ошибка. Соединение закрыто")
    sock.close()
    exit(-1)

datasplt = data.split(' ')
if datasplt[0] != 'p' or len(datasplt) == 0:
    print("Ошибка. Соединение закрыто")
    sock.close()
    exit(-1)
p = int(datasplt[1])
q = (p - 1) // 2
print("p и большой простой делитель q:", p, q)

h = random.randint(2, p)
while(pow(h, (p - 1) // q, p) == 1 and pow(h, (p - 1) // 2, p) == 1):
    h = random.randint(2, p)
t = random.randint(2, p)
while(pow(t, (p - 1) // q, p) == 1 and pow(t, (p - 1) // 2, p) == 1):
    t = random.randint(2, p)
print("Отправленные h и t:", h, t)

sock.send(('primitive ' + str(h) + ' ' + str(t)).encode('utf-8'))

data = (sock.recv(10240)).decode()
if not data:
    print("Ошибка. Соединение закрыто")
    sock.close()
    exit(-1)

datasplt = data.split(' ')
if datasplt[0] != 'y' or len(datasplt) == 0:
    print("Ошибка. Соединение закрыто")
    sock.close()
    exit(-1)
y = int(datasplt[1])
print("y =", y)

ans = input("Выбрать h или t самостоятельно или случайно (1 - сам., 2 - случ.): ")
if ans == "1":
    ht = input("Введите h или t: ")
else:
    ht = random.choice(['h','t'])
if ht == 'h':
    sock.send(('choice h').encode('utf-8'))
else:
    sock.send(('choice t').encode('utf-8'))

data = (sock.recv(1024)).decode()
if not data:
    print("Ошибка. Соединение закрыто")
    sock.close()
    exit(-1)

datasplt = data.split(' ')
if datasplt[0] != 'result' or len(datasplt) == 0:
    print("Ошибка. Соединение закрыто")
    sock.close()
    exit(-1)
result = datasplt[1]
x = int(datasplt[2])
if result == 'eagle':
    print("Ура! Угадал")
else:
    print("Не угадал")
ans = input("Хотите осуществить проверку? (да, нет)")
if ans == "да":
    if (shara.gen_gcd(x, p - 1)[0] == 1):
        print("x и (p - 1) взаимно просты")
    else:
        print("x и (p - 1) не взаимно просты")

    y1 = pow(h, x, p)
    y2 = pow(t, x, p)
    print("h ^ x (mod p) =", pow(h, x, p))
    print("t ^ x (mod p) =", pow(t, x, p))
    print("Посланный Алисой y =", y)
    if result == 'eagle' and ht == 'h':
        print("Правильный y =", pow(h, x, p))
    elif result == 'eagle' and ht == 't':
        print("Правильный y =", pow(t, x, p))
    elif result == 'tails' and ht == 'h':
        print("Правильный y =", pow(t, x, p))
    elif result == 'tails' and ht == 't':
        print("Правильный y =", pow(h, x, p))
else:
    print("Ну и ладно =Р")
    exit(0)
