# -*- coding: utf-8 -*-
"""
Задание 20.1
Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.
Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)
Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов
Для выполнения задания можно создавать любые дополнительные функции.
Для проверки доступности IP-адреса, используйте ping.
"""
import subprocess
from concurrent.futures import ThreadPoolExecutor
import time

def ping_ip_addres(ip):
    list_ok = []
    list_not_ok = []
#    ip_ping = 'ping {} -n 2'.format(ip) # как будет выглядеть текст команды
#    result = subprocess.run(ip_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    result = subprocess.run(["ping", "-c", "3", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)   #Linux
    result = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)    #Windows
    r = result.returncode   # говорит о том что сама команда выполнилась успешно
    out = result.stdout.decode('cp866')   #for lin ""utf-8"
#    time.sleep(15)  #в выводе видна задержка в выполнении в зависимости от количества потоков
    if r == 0 and not "узел недоступен" in out:  # если успешно выполняется команда и узел доступен!!
        list_ok.append(ip)
#        print(f"{ip} accesible !!!!")
    else:
        list_not_ok.append(ip)
    ip_tuple = (list_ok, list_not_ok)
    return ip_tuple

def ping_ip_addresses(ip_list, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip_addres, ip_list)  #возвращает генератор
    list_a = [] #список доступных адресов
    list_un_a = []  #список недоступных адресов
    for a1 in result:
        la1_0 = len(a1[0])
        la1_1 = len(a1[1])
        if la1_0 == 1:  #с учетом что функция "ping_ip_addres" работает только с одним адресом
            list_a.append(a1[0][0])
        elif la1_1 == 1:
            list_un_a.append(a1[1][0])
    tup_result = (list_a, list_un_a)
    return tup_result

if __name__ == "__main__":
    l_ip = ['172.16.1.1', '172.16.1.2', '172.16.1.3', '172.16.1.4', '172.16.1.5' ]
    list_of_ips = ["1.1.1", "8.8.8.8", "8.8.4.4", "8.8.7.1"]
#    print(ping_ip_addresses(l_ip))
    print(ping_ip_addresses(list_of_ips, 2))