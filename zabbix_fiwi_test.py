from pyzabbix import ZabbixAPI,ZabbixAPIException
import sys

def get_mac(label):
    return zapi.item.get(host="ru1-aruba-mc01", output=["itemid","lastvalue"], application="Hardware", search={"name": label + " Mac"})

# печатаем приветствие, начинаем работать
print("Hello. This script test script to get items from zabbix")
print("---------------------")

# авторизация в забиксе
zapi = ZabbixAPI("http://ru_monitoring/zabbix/")
zapi.login("maptest", "maptest")
print("Connected to Zabbix API Version %s" % zapi.api_version())

# устанавливаем начальные параметры
ap_name = "AP171_3b:a0"
mac = get_mac(ap_name)
print("Mac adress:" + mac[0]['lastvalue'])
print(*mac)