# -*- coding: utf-8 -*-
"""
Задание 19.1b

Скопировать функцию send_show_command из задания 19.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
"""
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
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
        sys.stdout.write(result)
    except NetMikoTimeoutException:
        result = 'Timeout Exception'
        sys.stdout.write(result)
    return result

if __name__ == "__main__":
    with open('test.yaml') as f:
        templates = yaml.load(f)
    list_of_dict = templates['routers']
    for dev in list_of_dict:
        result = send_show_command(dev, command)
        print(result)