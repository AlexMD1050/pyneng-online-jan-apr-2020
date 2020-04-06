# -*- coding: utf-8 -*-

"""
Задание 25.1a

Скопировать класс Topology из задания 25.1 и изменить его.
Если в задании 25.1 удаление дублей выполнялось в методе __init__,
надо перенести функциональность удаления дублей в метод _normalize.
При этом метод __init__ должен выглядеть таким образом:
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
if __name__=="__main__":
    top = Topology(topology_example)
    print(top.topology)