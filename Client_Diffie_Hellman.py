import socket
import random

sock = socket.socket()
sock.connect(('localhost', 9090))
print("Соединение установлено")

data = (sock.recv(1024)).decode()
if not data:
    sock.close()
    exit(-1)

datasplt = data.split(' ')
if datasplt[0] != 'keys' or len(datasplt) == 0:
    sock.close()
    exit(-1)

n = int(datasplt[1])
g = int(datasplt[2])
print(n)
print(g)

x = random.randint(1, n)
print("Случайное число клиента " + str(x))
pow_clnt = pow(g, x, n)
print("g в степени x по mod n " + str(pow_clnt))

sock.send(('powmodn ' + str(pow_clnt)).encode('utf-8'))

data = (sock.recv(1024)).decode()
if not data:
    sock.close()
    exit(-1)

datasplt = data.split(' ')
if datasplt[0] != 'powmodn' or len(datasplt) == 0:
    sock.close()
    exit(-1)

servpowmodn = int(datasplt[1])

key = pow(servpowmodn, x, n)
print("client key = " + str(key))
sock.close()