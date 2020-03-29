# -*- coding: utf-8 -*-
"""
Задание 19.2a

Скопировать функцию send_config_commands из задания 19.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода
информация о том к какому устройству выполняется подключение.

По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства из файла devices.yaml с помощью функции send_config_commands.
"""
from netmiko import ConnectHandler
import yaml
from pprint import pprint

commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]

def send_config_commands(device, commands, log = True):
    '''

    :param device:
    :param command:
    :return:
   '''
    with ConnectHandler(**device) as ssh:
        ssh.enable()    #помнить что некоторые команды можно выполнять и без en режима
        output = ssh.send_config_set(commands)
#        output2 = ssh.send_config_set('do show run | inc logging')
        ip = device['ip']
        if log == True:
            print('Подключаюсь к {}...'.format(ip))
        else:
            pass
        return output
if __name__ == "__main__":  # часть относится к скрипту, а не к функции
    with open('test.yaml') as f:    #заменить на 'devices.yaml'
        templates = yaml.load(f)
    list_of_dict = templates['routers'] #список устройств - параметры подключения к одному устройсву это словарь
    for dev in list_of_dict:
        result = send_config_commands(dev, commands, log=True)
        pprint(result)