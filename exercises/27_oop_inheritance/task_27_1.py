# -*- coding: utf-8 -*-

"""
Задание 27.1

Создать класс CiscoSSH, который наследует класс BaseSSH из файла base_connect_class.py.
Создать метод __init__ в классе CiscoSSH таким образом, чтобы после подключения по SSH выполнялся переход в режим enable.

Для этого в методе __init__ должен сначала вызываться метод __init__ класса BaseSSH, а затем выполняться переход в режим enable.

In [2]: from task_27_1 import CiscoSSH

In [3]: r1 = CiscoSSH(**device_params)

In [4]: r1.send_show_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}
# device_type= "cisco_ios", ip="192.168.100.1", username="cisco",password= "cisco", secret= "cisco"
import netmiko
import os

class BaseSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)

    def send_show_command(self, command):
        return self.ssh.send_command(command)

    def send_cfg_commands(self, commands):
        return self.ssh.send_config_set(commands)

class CiscoSSH(BaseSSH):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ssh.enable()
#        self.tr = kwargs['username']

if __name__=="__main__":
    t = CiscoSSH(device_type="cisco_ios", ip="172.16.1.2", username="cisco",password= "cisco", secret= "cisco")
    print(t.send_show_command('sh ip int brief'))
#print(t.tr)