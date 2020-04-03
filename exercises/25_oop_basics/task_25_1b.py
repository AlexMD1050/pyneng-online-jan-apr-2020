# -*- coding: utf-8 -*-

"""
Задание 25.1b

Изменить класс Topology из задания 25.1a или 25.1.

Добавить метод delete_link, который удаляет указанное соединение.
Метод должен удалять и зеркальное соединение, если оно есть.

Если такого соединения нет, выводится сообщение "Такого соединения нет".

Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление линка:
In [9]: t.delete_link(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление зеркального линка
In [11]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))

In [12]: t.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3')}

Если такого соединения нет, выводится сообщение:
In [13]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
Такого соединения нет

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
    def delete_link(self, list1_to_del, list2_to_del):
        src = list1_to_del
        dst = list2_to_del
        keys = self.topology.keys()
        val = self.topology.values()
        if src in keys:
            del self.topology[src]
            print('delete SRC link')
        elif dst in keys:
            del self.topology[dst]
            print('delete DST link')
        else:
            print('Такого соединения нет')
#        print(dst)
'''
top = Topology(topology_example)
print(top.topology)
print('===')
top.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
print(top.topology)
print('===')
top.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
#print(top.topology)
'''
