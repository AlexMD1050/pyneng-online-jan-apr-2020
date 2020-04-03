# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_config_commands

Функция подключается по SSH (с помощью netmiko) к устройству и выполняет перечень команд в конфигурационном режиме на основании переданных аргументов.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* config_commands - список команд, которые надо выполнить

Функция возвращает строку с результатами выполнения команды:

In [7]: r1
Out[7]:
{'device_type': 'cisco_ios',
 'ip': '192.168.100.1',
 'username': 'cisco',
 'password': 'cisco',
 'secret': 'cisco'}

In [8]: commands
Out[8]: ['logging 10.255.255.1', 'logging buffered 20010', 'no logging console']

In [9]: result = send_config_commands(r1, commands)

In [10]: result
Out[10]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#logging 10.255.255.1\nR1(config)#logging buffered 20010\nR1(config)#no logging console\nR1(config)#end\nR1#'

In [11]: print(result)
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.255.255.1
R1(config)#logging buffered 20010
R1(config)#no logging console
R1(config)#end
R1#


Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_config_commands.
"""
from netmiko import ConnectHandler
import yaml
from pprint import pprint

commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
device_params = {"ip": '172.16.1.2',
                 "username": "cisco",
                 "password": "cisco",
                 "secret": "cisco",
                 "device_type": "cisco_ios"}
device = '172.16.1.2'

def send_config_commands(device, commands):
    '''
    :param device: список устройств к которым подключаемся из yaml файла
    :param command: список команд которые выполняем на КАЖДОМ из устройств к которому подключаемся
    :return: возвращаем список с результатом выполнения команд
   '''
    with ConnectHandler(**device) as ssh:
        ssh.enable()    #помнить что некоторые команды можно выполнять и без en режима
        output = ssh.send_config_set(commands, strip_prompt=False  )
        ip = device['ip']
        print('Подключаюсь к {}...'.format(ip))
        return output
if __name__ == "__main__":  # часть относится к скрипту, а не к функции
    with open('test.yaml') as f:    #заменить на 'devices.yaml'
        templates = yaml.load(f)
    list_of_dict = templates['routers'] #список устройств - параметры подключения к одному устройсву это словарь
    for dev in list_of_dict:
        result = send_config_commands(dev, commands)
        pprint(result)