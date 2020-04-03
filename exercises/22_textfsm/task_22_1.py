# -*- coding: utf-8 -*-
"""
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM (templates/sh_ip_int_br.template)
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

"""

import textfsm

template = 'templates/sh_ip_int_br.template'
output_file = 'output/sh_ip_int_br.txt'

def parse_command_output(template, command_output):
    with open(template) as temp, open(command_output) as output:
        result_list = []
        re_table = textfsm.TextFSM(temp)
        header = re_table.header
        result_list.append(header)
        result = re_table.ParseText(output.read())
        for list in result: #проходимся по списку списков
            result_list.append(list)
    return result_list
if __name__ == "__main__":
    print(parse_command_output(template, output_file))