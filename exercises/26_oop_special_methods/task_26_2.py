# -*- coding: utf-8 -*-

"""
Задание 26.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.
Все исключения, которые возникли в менеджере контекста, должны генерироваться после выхода из блока with.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_26_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
"""
import telnetlib
import time

class CiscoTelnet:
    def __init__(self, ip, username, password, enable_password=None, disable_paging=True):
        self.ip = ip
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username:")
        self.telnet.write(username.encode("ascii") + b"\n")

        self.telnet.read_until(b"Password:")
        self.telnet.write(password.encode("ascii") + b"\n")
        if enable_password:
            self.telnet.write(b"enable\n")
            self.telnet.read_until(b"Password:")
            self.telnet.write(enable_password.encode("ascii") + b"\n")
        if disable_paging:
            self.telnet.write(b"terminal length 0\n")
        time.sleep(0.5)
        self.telnet.write(b"conf t\n")
        time.sleep(0.5)
        self.telnet.read_very_eager()
        print('Telnet connection to divice esteblished')

    def send_show_command(self, command):
        #отправляем команду show НЕ в конфигурационном режиме
        self.telnet.write(b"end\n") #выходим из режима конфиг в который попали при инициализации __init__
        time.sleep(0.5)
        self.telnet.write(command.encode("ascii") + b"\n")
        time.sleep(1)
#        output = self.telnet.read_very_eager().decode("ascii")
#        time.sleep(1)
        self.telnet.write(b"conf t \n")  #возвращаемся в конфиг режим не уверен нужна команда ли нет
        output = self.telnet.read_very_eager().decode("ascii")
        return output

    def _write_line(self,command):  #проверить результат можно зайдя на устройство
        '''
        Отправляем строку к которой добавили перенос строки и все это преобразовали в байты те передаем байты
        :param command:
        :return:
        '''
        str = command + '\n'         #добавляем перевод строки
#        print(str)
        str_b = str.encode('utf-8')  #конвертируем в байты
        self.telnet.write(str_b)
        output = self.telnet.read_very_eager().decode("ascii")
        return output

    def __enter__(self):
        print('__enter__')
        return self
    def __exit__(self,exc_type, exc_value, traceback):
        print("__exit__")
        self.close()

    def close(self, exc_type, exc_value, traceback):
        self.telnet.close()

if __name__ == '__main__':
    with CiscoTelnet('172.16.1.2', 'cisco', 'cisco', enable_password='cisco') as r:
        print(r.send_show_command('sh clock'))
        raise ValueError
    print('all closed')
#    print(t._write_line('logging 4.4.4.4'))
#    print(t._write_line('logging 5.5.5.5'))
