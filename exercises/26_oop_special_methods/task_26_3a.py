# -*- coding: utf-8 -*-

"""
Задание 26.3a

Изменить класс IPAddress из задания 26.3.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

Для этого задания нет теста!
"""
import ipaddress

class IPAddress:
    def __init__(self,ip_mask):
        self.ip = ip_mask.split('/')[0]
        self.mask = ip_mask.split('/')[1]
        if not ipaddress.ip_address(self.ip):
            raise ValueError('Incorrect IPv4 address')
        if not int(self.mask) >8 and int(self.mask)<32:
            raise ValueError('Incorrect mask')
#        print('===')
        self.ip = ip_mask.split('/')[0]
        self.mask = ip_mask.split('/')[1]

    def __str__(self):
        return f"IP address: {self.ip}/{self.mask}"

    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"

if __name__ == "__main__":
    ip1 =IPAddress('192.168.1.1/26')
    print(str(ip1))
    ip_list = []
    ip_list.append(ip1)
    print(ip_list)