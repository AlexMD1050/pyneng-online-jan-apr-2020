# -*- coding: utf-8 -*-

"""
Задание 27.2a

Дополнить класс MyNetmiko из задания 27.2.
Добавить метод _check_error_in_command, который выполняет проверку на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Метод ожидает как аргумент команду и вывод команды.
Если в выводе не обнаружена ошибка, метод ничего не возвращает.
Если в выводе найдена ошибка, метод генерирует исключение ErrorInCommand с сообщениеем о том какая ошибка была обнаружена, на каком устройстве и в какой команде.
Переписать метод send_command netmiko, добавив в него проверку на ошибки.
In [2]: from task_27_2a import MyNetmiko
In [3]: r1 = MyNetmiko(**device_params)
In [4]: r1.send_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '
In [5]: r1.send_command('sh ip br')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-1c60b31812fd> in <module>()
----> 1 r1.send_command('sh ip br')
...
ErrorInCommand: При выполнении команды "sh ip br" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker."

"""

from netmiko.cisco.cisco_ios import CiscoIosBase
class ErrorInCommand(Exception):
    '''
    дополнительные исключения
    '''

class MyNetmiko(CiscoIosBase):
    def __init__(self, **kwargs):
        self.ipo = kwargs['ip']
        super().__init__(**kwargs)
        self.enable()  #при выключени данной команды "sh run" не выполняется.

    def send_command(self,command):
        self.command=command
        self.output = super().send_command(command)
        self._check_error_in_command(command, self.output)
        return self.output

    def _check_error_in_command(self,command, output):
        if 'Invalid input detected' in output:
            raise ErrorInCommand(
                f'При выполнении команды {command} на устройстве {self.ipo} возникла ошибка "Invalid input detected at "^" marker." ')
        elif "Incomplete command" in output:
            raise ErrorInCommand(
                f'При выполнении команды {command} на устройстве {self.ipo} возникла ошибка "% Incomplete command."')
        elif "Ambiguous command" in output:
            raise ErrorInCommand(
                f'При выполнении команды {command} на устройстве {self.ipo} возникла ошибка "Ambiguous command"')
        else:
            pass

#if __name__=="__main__":
c = MyNetmiko(device_type= "cisco_ios", ip="172.16.1.2", username="cisco",password= "cisco", secret= "cisco")
print(c.send_command('sh clock'))
#    c.send_command('sh clock')
#    print(c.send_config_set( ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]))
#    print(CiscoIosBase.mro())