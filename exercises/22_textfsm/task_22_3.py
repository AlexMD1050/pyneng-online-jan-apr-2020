# -*- coding: utf-8 -*-
"""
Задание 22.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - templates

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""
import sys
import textfsm
from textfsm import clitable

output_file = 'output/sh_ip_int_br.txt'
attributes_dict = {'Command':'sh ip int brief', 'Vendor':'cisco_ios'}
index_file = 'index'
templ_path = 'templates'

def parse_command_dynamic(command_output, attributes_dict, index_file, templ_path='templates'):
    with open(command_output) as output:
        command_output = output.read()
    cli = clitable.CliTable(index_file, templ_path)
    cli.ParseCmd(command_output, attributes_dict)
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

if __name__ == "__main__":
    print(parse_command_dynamic('output/sh_ip_int_br.txt', attributes_dict, 'index' ))
