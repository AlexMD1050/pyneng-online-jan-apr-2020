# -*- coding: utf-8 -*-
"""
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
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
    with open('test.yaml') as f:
        templates = yaml.load(f)
    list_of_dict = templates['routers'] #список устройств - параметры подключения к одному устройсву это словарь
    for dev in list_of_dict:
        result = send_show_command(dev, command)
        print(result)
