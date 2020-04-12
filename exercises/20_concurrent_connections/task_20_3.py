# -*- coding: utf-8 -*-
"""
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


Для выполнения задания можно создавать любые дополнительные функции.
Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""
from netmiko import ConnectHandler
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat
import time
from datetime import datetime
import logging

commands = {
    "192.168.100.1": "sh ip int br",
    "192.168.100.2": "sh arp",
    "192.168.100.3": "sh ip int br",
}

commands2 = {
    "172.16.1.2": "sh ip int br",
    "172.16.1.3": "sh arp",
    "172.16.1.2": "sh ip int br",
}
def send_show(device_dict, command):
    start_msg = "===> {} Connection: {}"
    ip = device_dict["ip"]
    print(start_msg.format(datetime.now().time(), ip))
    if ip == "172.16.1.3":
        time.sleep(5)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        name = ssh.find_prompt()
        result = ssh.send_command(command, strip_command=False)
    return (name + result)

def send_command_to_devices(devices, commands_dict,filename ,limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        for device in devices:
            ip = device['ip']
            comm = commands_dict[ip]
            future = executor.submit(send_show, device, comm)
            future_list.append(future)
            with open(filename, 'w') as file:
                for f in as_completed(future_list):
                    i = str(f.result())
                    file.write(i + '\n')

if __name__ == "__main__":
    with open('test.yaml') as f:
        templates = yaml.load(f)
    list_of_dict = templates['routers']
    result = send_command_to_devices(list_of_dict, commands_dict=commands2,filename='task_20_3_out.txt', limit=1)
