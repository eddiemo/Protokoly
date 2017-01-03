import random
from hashlib import *
import sys, os

def regisration():
    accs = set()
    if os.stat("database").st_size != 0:
        names = open("database", "r").readlines()
        for n in names:
            x = n.split()
            accs.add(x[0])
    while True:
        name = input("Введите имя пользователя: ")
        if name in accs:
            continue
        else:
            accs.add(name)
            break

    r = random.randint(0, 2**32)
    x = r
    file = open(name, 'w')
    hashs = []
    for i in range(100):
        x = md5(str(x).encode()).hexdigest()
        hashs.insert(0, str(x))
    with open(name, 'w') as F:
        for hash in hashs:
            F.writelines(hash + "\n")
    file.close()
    data = open("database", "a")
    if os.stat("database").st_size == 0:
        data.write(name + " " + md5(str(x).encode()).hexdigest())
    else:
        data.write("\n" + name + " " + md5(str(x).encode()).hexdigest())
    data.close()

def login():
    accs = set()
    if os.stat("database").st_size != 0:
        names = open("database", "r").readlines()
        for n in names:
            x = n.split()
            accs.add(x[0])
    name = input("Введите имя пользователя: ")
    if name not in accs:
        print ("Пользователь " + name + " не найден, зарегистрируйтесь")
        sys.exit(0)

    s_user = input("Введите пароль: ")

    file = open("database", 'r+')
    text = file.readlines()
    file.seek(0)
    txt = file.read()
    file.close()
    data = open("database", 'w')
    ans = "Вход не выполнен"
    for line in text:
        a = line.split(' ')
        if a[0] == name:
            if a[1][-1] == "\n":
                a[1] = a[1][:-1]
            if str(md5(s_user.encode()).hexdigest()) == a[1]:
                txt = txt.replace(a[1], s_user)
                ans = "Вход выполнен"
            else:
                ans = "Вход не выполнен"
            break
    data.write(txt)
    print(ans)
    file.close()

if __name__ == '__main__':
    while True:
        ent = input("Выберите режим работы программы: (r)egister, (l)ogin, (q)uit: ")
        if ent == "r":
            regisration()
            print("Пользователь создан.")
        elif ent == "l":
            login()
        else:
            sys.exit(0)