# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

"""
from netmiko import ConnectHandler
import yaml


command = "sh ip int br" #то что отправляем на все устройства

def send_show_command(device, command):
    '''
    Подключение к одному устройству
    :param device: словарь с параметрами подключения к устройству
    :param command: команда, которую надо выполнить одна
    :return: строку с выводом команды
   '''
    with ConnectHandler(**device) as ssh:
        ssh.enable()    #помнить что некоторые команды можно выполнять и без en режима
        result = ssh.send_command(command)
        ip = device['ip']
        print('connect to device {}'.format(ip))
        return result

if __name__ == "__main__":  # часть относится к скрипту, а не к функции
    with open('devices.yaml') as f:
        templates = yaml.load(f)
    list_of_dict = templates['routers'] #список устройств - параметры подключения к одному устройсву это словарь
    for dev in list_of_dict:
        result = send_show_command(dev, command)
        print(result)
