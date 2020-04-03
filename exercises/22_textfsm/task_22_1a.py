# -*- coding: utf-8 -*-
"""
Задание 22.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM (templates/sh_ip_int_br.template)
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
"""
import textfsm

template = 'templates/sh_ip_int_br.template'
output_file = 'output/sh_ip_int_br.txt'

def parse_output_to_dict(template, command_output):
    with open(template) as temp, open(command_output) as output:
        result_list_of_dict = []    #результирующий список словарей
        re_table = textfsm.TextFSM(temp)
        header = re_table.header
#        result_list.append(header)
        result = re_table.ParseText(output.read())
        for list in result: #проходимся по списку списков
            dict_of_line = {}  # словарь
            for i in range(4):
                key = header[i]
                value = list[i]
                dict_of_line[key] = value
            result_list_of_dict.append(dict_of_line)
    return result_list_of_dict
if __name__ == "__main__":
    print(parse_output_to_dict(template, output_file))