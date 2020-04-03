# -*- coding: utf-8 -*-

"""
Задание 25.2

Создать класс CiscoTelnet, который подключается по Telnet к оборудованию Cisco.

При создании экземпляра класса, должно создаваться подключение Telnet, а также переход в режим enable.
Класс должен использовать модуль telnetlib для подключения по Telnet.

У класса CiscoTelnet, кроме __init__, должно быть, как минимум, два метода:
* _write_line - принимает как аргумент строку и отправляет на оборудование строку преобразованную в байты и добавляет перевод строки в конце.
  Метод _write_line должен использоваться внутри класса.
* send_show_command - принимает как аргумент команду show и возвращает вывод полученный с обрудования

Пример создания экземпляра класса:
In [2]: from task_25_2 import CiscoTelnet

In [3]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}
   ...:

In [4]: r1 = CiscoTelnet(**r1_params)

In [5]: r1.send_show_command('sh ip int br')
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

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

if __name__ == '__main__':
    t = CiscoTelnet('172.16.1.2', 'cisco', 'cisco', enable_password='cisco')
#    print(t._write_line('logging 4.4.4.4'))
    print(t.send_show_command('sh ip int brief'))
#    print(t._write_line('logging 5.5.5.5'))
