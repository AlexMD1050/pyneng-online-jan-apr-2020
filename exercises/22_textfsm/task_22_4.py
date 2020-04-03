# -*- coding: utf-8 -*-
"""
Задание 22.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
"""

from netmiko import ConnectHandler
import textfsm
from textfsm import clitable

device_dict ={'device_type':'cisco_ios', 'ip':'172.16.1.2','username':'cisco','password':'cisco','secret':'cisco'}
command = "sh ip int br" #то что отправляем на все устройства
templates_path='templates'
#attributes_dict = {'Command':'sh ip int brief', 'Vendor':'cisco_ios'}

def send_and_parse_show_command(device_dict, command, templates_path, index='index'):
    '''
   '''
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()    #помнить что некоторые команды можно выполнять и без en режима
        result = ssh.send_command(command)
        ip = device_dict['ip']
        print('connect to device {}'.format(ip))
#        print(result)
    attributes_dict = {'Command': 'sh ip int brief', 'Vendor': 'cisco_ios'}
    attributes_dict['Command'] = command
    cli = clitable.CliTable(index, templates_path)
    cli.ParseCmd(result, attributes_dict )
    #print('Formatted Table:\n', cli.FormattedTable())
    data_rows = [list(row) for row in cli]  #разобратся
    header = list(cli.header)
    #print(header)
    #print(data_rows)
    list_result = []
    for data in data_rows:
        dict_temp = {}
        for i in range(4):
            dict_temp[header[i]] = data[i]
        list_result.append(dict_temp)
    return list_result
if __name__ == "__main__":  # часть относится к скрипту, а не к функции
    print(send_and_parse_show_command(device_dict, command, templates_path, index='index'))