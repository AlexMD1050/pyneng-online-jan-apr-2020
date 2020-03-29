# -*- coding: utf-8 -*-
"""
Задание 19.2b

Скопировать функцию send_config_commands из задания 19.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра log.
При этом, параметр log по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате:
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'a',
 'logging buffered 20010',
 'ip http server']

In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "a" выполнилась с ошибкой "Ambiguous command:  "a"" на устройстве 192.168.100.1

In [18]: pprint(result, width=120)
({'ip http server': 'config term\n'
                    'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                    'R1(config)#ip http server\n'
                    'R1(config)#',
  'logging buffered 20010': 'config term\n'
                            'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                            'R1(config)#logging buffered 20010\n'
                            'R1(config)#'},
 {'a': 'config term\n'
       'Enter configuration commands, one per line.  End with CNTL/Z.\n'
       'R1(config)#a\n'
       '% Ambiguous command:  "a"\n'
       'R1(config)#',
  'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'a'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
"""

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]
commands = commands_with_errors + correct_commands

from netmiko import ConnectHandler
import yaml
from pprint import pprint

#commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]

def send_config_commands(device, commands, log = True):
    '''
    Функция передачи команд на устройство с контролем результатат выполнения
    :param device: устройство на котором выполняются команды
    :param command: список команд
    :param log: вывод на stdout информации о подключении к IPадресу устройства
    :return: кортеж из 2х словарей ( успешные и неудачные команды)
   '''
    with ConnectHandler(**device) as ssh:
        ssh.enable()    #помнить что некоторые команды можно выполнять и без en режима
        ip = device['ip']
        dict_r = {} #словарь безошибочных команд
        dict_w = {} #словарь команд с ошибкой
        list_command = []
        error_text = 'Команда "{}" выполнилась с ошибкой "{}" на устройстве "{}"'
        if log == True:
            print('Подключаюсь к {}...'.format(ip))
        else:
            pass
        for command in commands:
            result = ssh.send_config_set(command,) # попробовать оптимизировать
            list_a = result.split('\n') #переделать на regexp
            # как то переделать if/elif statement
            # знаем что в определенных позициях списка могут содержатся значения с результатом выполнения программы
            if ('Ambiguous command:') in list_a[4] or ('Incomplete command') in list_a[4] or ('Invalid input detected') in list_a[4]:
                print('===' + error_text.format(command, list_a[4], ip))
                dict_w[command] = result
#                list_command.append(dict_w)
            elif ('Ambiguous command:') in list_a[3] or ('Incomplete command') in list_a[3] or ('Invalid input detected') in list_a[3]:
                print('---' + error_text.format(command, list_a[3], ip))
                dict_w[command] = result
#                list_command.append(dict_w)
            else:
                dict_r[command] = result
        list_command.append(dict_r)
        list_command.append(dict_w)
        result_tuple = tuple(list_command)
        return result_tuple

if __name__ == "__main__":  # часть относится к скрипту, а не к функции
    with open('test.yaml') as f:    #заменить на 'devices.yaml'
        templates = yaml.load(f)
    list_of_dev = templates['routers'] #список устройств - параметры подключения к одному устройсву это словарь
    for dev in list_of_dev:
        result = send_config_commands(dev, commands, log=True)
        pprint(result, width=120)