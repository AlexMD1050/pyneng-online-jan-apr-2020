# -*- coding: utf-8 -*-

"""
Задание 25.1d

Изменить класс Topology из задания 25.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


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

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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

    def add_link(self, src_link, dst_link):
        if src_link in self.topology.keys() and dst_link in self.topology.values():
            print('Такое соединение существует')
        elif src_link in self.topology.keys():
            print('Cоединение с одним из портов существует')
        elif dst_link in self.topology.keys():
            print('Cоединение с одним из портов существует')
        elif src_link in self.topology.values():
            print('Cоединение с одним из портов существует')
        elif dst_link in self.topology.values():
            print('Cоединение с одним из портов существует')
        else:
            self.topology[src_link] = dst_link
if __name__ == "__main__":
    pass
    '''
    top = Topology(topology_example)
    print(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    print(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    '''