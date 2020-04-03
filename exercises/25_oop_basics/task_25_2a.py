# -*- coding: utf-8 -*-

"""
Задание 25.2a

Скопировать класс CiscoTelnet из задания 25.2 и изменить метод send_show_command добавив два параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей, полученные после
обработки с помощью TextFSM. При parse=True должен возвращаться список словарей, а parse=False обычный вывод
* templates - путь к каталогу с шаблонами

Пример создания экземпляра класса:
In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_25_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command('sh ip int br', parse=False)
Out[4]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

In [5]: r1.send_show_command('sh ip int br', parse=True)
Out[5]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '190.16.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.100',
  'address': '10.100.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.200',
  'address': '10.200.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.300',
  'address': '10.30.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback0',
  'address': '10.1.1.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback55',
  'address': '5.5.5.5',
  'status': 'up',
  'protocol': 'up'}]
"""

import telnetlib
import time
import textfsm
from textfsm import clitable

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

    def send_show_command(self, command, parse, templates):
        #отправляем команду show НЕ в конфигурационном режиме
        self.telnet.write(b"end\n") #выходим из режима конфиг в который попали при инициализации __init__
        time.sleep(0.5)
        self.telnet.write(command.encode("ascii") + b"\n")
        time.sleep(1)
        self.telnet.write(b"conf t \n")  #возвращаемся в конфиг режим не уверен нужна команда ли нет
        output = self.telnet.read_very_eager().decode("ascii")
        if parse==True:
            attributes_dict = {'Vendor': 'cisco_ios'}
            attributes_dict['Command'] = command
            cli = clitable.CliTable('index', templates)
            cli.ParseCmd(output, attributes_dict)
            data_rows = [list(row) for row in cli]  # разобратся
            header = list(cli.header)
            list_result = []
            for data in data_rows:
                dict_temp = {}
                for i in range(4):
                    dict_temp[header[i]] = data[i]
                list_result.append(dict_temp)
            output = list_result
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
    print(t.send_show_command('sh ip int brief', parse=False,templates= 'templates'))
#    print(t._write_line('logging 5.5.5.5'))