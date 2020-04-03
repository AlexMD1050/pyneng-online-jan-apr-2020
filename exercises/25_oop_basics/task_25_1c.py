# -*- coding: utf-8 -*-

"""
Задание 25.1c
Изменить класс Topology из задания 25.1b.
Добавить метод delete_node, который удаляет все соединения с указаным устройством.
Если такого устройства нет, выводится сообщение "Такого устройства нет".
Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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

    def delete_node(self, node_name):
        name = node_name
        self.topology_2 = self.topology.copy()
        items = self.topology_2.items()
        for item in items:
            if name in item[0]:
                del self.topology[item[0]]
            if name in item[1]:
                del self.topology[item[0]]



#top = Topology(topology_example)
#print(top.topology)
#top.delete_node('SW1')
#print('='*10)
#print(top.topology)

