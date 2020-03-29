# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к устройству, которому надо передать команды
* show - одна команда show (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции send_commands, всегда будет передаваться только один из аргументов show, config.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: send_commands(r1, config=['username user5 password pass5', 'username user6 password pass6'])
Out[15]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#username user5 password pass5\nR1(config)#username user6 password pass6\nR1(config)#end\nR1#'
"""
from task_19_1 import send_show_command
from task_19_2 import send_config_commands
from netmiko import ConnectHandler
import yaml
from pprint import pprint

commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
command = "sh ip int br"
device = {"ip": '172.16.1.2',   # СЛОВАРЬ С ПАРАМЕТРАМИ ПОДКЛЮЧЕНИЯ К УСТРОЙСТВУ
                 "username": "cisco",
                 "password": "cisco",
                 "secret": "cisco",
                 "device_type": "cisco_ios"}


def send_commands(device, **kwargs):
    if 'show' in kwargs:    #если есть show выполняем функцию send_show_command из задания 19.1
#        print('we need show')
        command = kwargs['show']
#        print(command)
        result = send_show_command(device, command)
    elif 'config' in kwargs:    #если есть config выполняем функцию send_config_commands из задания 19.2
#        print('we have config')
        conf_commands = kwargs['config'] #список команд
#        print(conf_commands)
        result = send_config_commands(device, conf_commands)
    else:   #   Если нет ни show ни config
        print('something wrong in ' + kwargs)
    return result

#print(send_commands(device, show = 'sh ip int br' ))
print(send_commands(device, config=["logging 10.255.255.1", "logging buffered 20010", "no logging console"]))
