#! /usr/bin/python
# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI,ZabbixAPIException
import argparse,sys,re,os,configparser

def get_triggers(label):
    return zapi.trigger.get(host=msm_host,output="triggerid",search={"description": "Access Point "+label},filter={"status": "0"})
'''def get_mac(label):
    return zapi.item.get(host=msm_host, output=["itemid","lastvalue"], application="Hardware", search={"name": "*" + label + "*Mac"}, searchWildcardsEnabled="true") '''
def get_channels(label):
    chan1 = zapi.item.get(host=msm_host, output=["itemid", "lastvalue"], application="Hardware", search={"name": "*" + label + "*na channel"}, searchWildcardsEnabled="true")
    chan2 = zapi.item.get(host=msm_host, output=["itemid", "lastvalue"], application="Hardware", search={"name": "*" + label + "*ng channel"}, searchWildcardsEnabled="true")
    if chan1 and chan2:
        return "Channels: " + chan1[0]['lastvalue'] + ", " + chan2[0]['lastvalue']
    else: return ""

def map_change(map_id):
    # get map elements
    mapp = zapi.map.get(sysmapids=map_id, selectSelements="extend")
    print("Map Name: " + mapp[0]['name'])
    triggers_count = 0
    channels_count = 0
    #mac_count = 0
    for i in mapp[0]['selements']:
        if i['label'][0:2] == 'AP':  # если в название элемента есть AP то
            '''
            mac = get_mac(i['label'][0:5])  # ищем мак адрес через айтем
            if mac:
                mac_count+=1
                #print('Mac adress: '+mac[0]['lastvalue'])
                if "Mac:" in i['label']:
                    #print('AP map label: '+i['label'])
                    #print("mac absent, need to insert")
                    i['label'] = re.sub(r'Mac:..-..-..-..-..-..', 'Mac:' + mac[0]['lastvalue'],
                                        i['label'])  # меняем мак
                else:
                    i['label'] = i['label'] + "\nMac:" + mac[0][
                        'lastvalue']  # если нет мака в названии то добавляем его '''
            channels = get_channels(i['label'][0:5])  # ищем каналы на этой точке
            if channels:
                channels_count += 1
                if "Channels:" in i['label']:
                    i['label'] = re.sub(r"Channels: \d+, \d+", channels, i['label'])
                else:
                    i['label'] = i['label'] + "\n" + channels  # если нет Канала в названии то добавляем его

            triggers = get_triggers(i['label'][0:5])  # получаем триггеры, завязаные на эту точку
            if triggers:
                i['elements'] = triggers  # добавляем связь на эти триггеры
                triggers_count += 1
                i['elementtype'] = 2  # меняем тип элемента на триггер
                i['iconid_off'] = 196  # меняем иконку выключенного триггера
                i['iconid_on'] = 197  # меняем иконку включенного триггера
                #print("Triggers changed on  " + i['label'])
                #print("----------")
                #print(i['elements'])
    #print(mapp[0]['selements'])
    try:
        zapi.map.update(sysmapid=map_id, selements=mapp[0]['selements'])  # пушим наши изменения в карту
        print("processed:\n" + "Triggers: "+str(triggers_count)+"\nChannels: "+str(channels_count))
        os.system('zabbix_sender -z ru_monitoring -s "Zabbix server" -k script.wifi.map.status -o 0')
    except ZabbixAPIException as e:
        print(e)
        os.system('zabbix_sender -z ru_monitoring -s "Zabbix server" -k script.wifi.map.status -lo 1')
def crudConfig(path):
    global username,password,msm_host
    """
       Create, read, update, delete config
       """
    if not os.path.exists(path):
        createConfig(path)

    config = configparser.ConfigParser()
    config.read(path)

    # Читаем некоторые значения из конфиг. файла.
    username = config.get("Settings", "username")
    password = config.get("Settings", "password")
    msm_host = config.get("Settings", "msm_host")
    #print(username)
def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "username", "username")
    config.set("Settings", "password", "password")
    config.set("Settings", "msm_host", "HP MSM WiFi controller")
    with open(path, "w") as config_file:
        config.write(config_file)
# печатаем приветствие, начинаем работать
print("Hello. This script wolud modify HP MSM APs from simple images to Interactive objects with connected triggers. Script scan map for AP items and connect triggers to them")
print("---------------------")

# считываем конфиг с паролем , пользователем, и другими параметрами
# определяем переменные, не используйте для установки. Используйте вместо этого параметры в конфиг файле mapchanger.conf
username="none"
password="none"
msm_host="none"
path=os.path.dirname(os.path.abspath(__file__))+"/mapchanger.conf"
#print(path)
crudConfig(path)
#print(msm_host)

# парсим аргументы, маленькая помощь при запуске. либо печатаем карты либо изменяем одну.
parser = argparse.ArgumentParser(description='sample app for map triggers to access points maps')
parser.add_argument('-p', action="store_true", help='Print map names')
parser.add_argument('-all', action="store_true", help='Change all AP maps')
parser.add_argument('-m', help='change only one map id, not work with -all', type=int)
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)
namespace = parser.parse_args()
#print (namespace)

# авторизация в забиксе
zapi = ZabbixAPI("http://ru_monitoring/zabbix/")
zapi.login(username, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())

if namespace.p : # печатаем карты
    for m in zapi.map.get(output="extend"):
        print(m['sysmapid']+" "+m['name'])
    sys.exit()
if namespace.m: # модифиуируем карту
    map_change(namespace.m)
    sys.exit()
if namespace.all : # обрабатываем все карты
    for m in zapi.map.get(output=["sysmapid","name"],search={"name":"AP"},startSearch="true"):
        #print(m['sysmapid']," ",m['name'])
        map_change(m['sysmapid'])
    sys.exit()