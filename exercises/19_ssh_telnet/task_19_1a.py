# -*- coding: utf-8 -*-
"""
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации на устройстве.
При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.
Для проверки измените пароль на устройстве или в файле devices.yaml.
"""
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException
from netmiko.ssh_exception import *
import yaml
from pprint import pprint
import sys

command = 'sh ip int brief'
# task_19_1
def send_show_command(device, command):
    '''
    Подключение к одному устройству
    :param device:
    :param command:
    :return:
   '''
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()    #помнить что некоторые команды можно выполнять и без en режима
            result = ssh.send_command(command)
            ip = device['ip']
            print('connect to device {}'.format(ip))
    except NetmikoAuthenticationException:
        result = "Authentication failure: unable to connect"
        print(result)
        sys.stdout.write(result)
    return result

if __name__ == "__main__":
    with open('test.yaml') as f:
        templates = yaml.load(f)
    list_of_dict = templates['routers']
    for dev in list_of_dict:
        result = send_show_command(dev, command)
        print(result)