# -*- coding: utf-8 -*-

"""
Задание 25.2b

Скопировать класс CiscoTelnet из задания 25.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима или список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_25_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
import time
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

    def send_config_commands(self, commands):
        out = ''
        for command in commands:
#            print(out)
            self.telnet.write(command.encode("ascii") + b"\n")
            time.sleep(1)
            output = self.telnet.read_very_eager().decode("ascii")
#            print(output)
            print('---')
            out += output
        return out

if __name__ == '__main__':
    t = CiscoTelnet('172.16.1.2', 'cisco', 'cisco', enable_password='cisco')
#    print(t._write_line('logging 4.4.4.4'))
#    print(t.send_show_command('sh ip int brief', parse=False,templates= 'templates'))

    print(str(t.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])))