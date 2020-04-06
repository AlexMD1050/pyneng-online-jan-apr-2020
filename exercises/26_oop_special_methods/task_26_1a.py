# -*- coding: utf-8 -*-

"""
Задание 26.1a

В этом задании надо сделать так, чтобы экземпляры класса Topology были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 25.1x или задания 26.1.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        #### убираем дубли криво но вроде работает, проверить как правильно в ДОМАШКЕ.
        key = topology_dict.keys()
        value = list(topology_dict.values())
        dict_comm2 = topology_dict.copy()
        for n in value:  # перебираем значения
            if n in key:  # если значение равно какому либо ключу
                val = topology_dict[n]
                value.remove(val)
                del (dict_comm2[n])
            else:
                pass
        return dict_comm2

    def __add__(self, second):
        t1 = self.topology.copy()
        t2 = second.topology
        t1.update(t2)
        return t1
    def __iter__(self):
        print("Вызываю __iter__")
        return iter(self.topology)


if __name__=='__main__':
    top1 = Topology(topology_example)
    for item in top1:
        print(item)
#    print(top1 + top2)
#    print('---')
#    print(top1.topology)
#    print(top2.topology)