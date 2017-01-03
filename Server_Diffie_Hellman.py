import socket
import shara
import random

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)

print("Генерация n и g")
n = shara.gen_p(200)
g = random.randint(2, n - 1)
print("n и g сгенерированы")

print("Ждём подключение...")
while True:
    conn, addr = sock.accept()
    print("Соединение установлено")

    conn.send(('keys ' + str(n) + ' ' + str(g)).encode('utf-8'))

    data = (conn.recv(1024)).decode()
    if not data:
        conn.close()
        continue

    datasplt = data.split(' ')
    if datasplt[0] != 'powmodn' or len(datasplt) == 0:
        conn.close()
        continue

    clpowmodn = int(datasplt[1])

    y = random.randint(1, n)
    pow_serv = pow(g, y, n)

    conn.send(('powmodn ' + str(pow_serv)).encode('utf-8'))

    key = pow(clpowmodn, y, n)
    print("server key = " + str(key))
    conn.close()