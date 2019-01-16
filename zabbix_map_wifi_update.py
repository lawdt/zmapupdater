from pyzabbix import ZabbixAPI,ZabbixAPIException
import argparse,sys

def get_triggers(label):
   return zapi.trigger.get(host="HP MSM WiFi controller",output="triggerid",search={"description": "Access Point "+label},filter={"status": "0"})

parser = argparse.ArgumentParser(description='sample app for map triggers to access points maps')

parser.add_argument('-p', action="store_true", help='Print map names')
parser.add_argument('-m', help='map id', type=int)
namespace = parser.parse_args()
print (namespace)

zapi = ZabbixAPI("http://ru_monitoring/zabbix/")
zapi.login("username", "password")
print("Connected to Zabbix API Version %s" % zapi.api_version())

if namespace.p :
    for m in zapi.map.get(output="extend"):
        print(m['sysmapid']," ",m['name'])
    sys.exit()
if namespace.m:
    #get map elements
    mapp = zapi.map.get(sysmapids=namespace.m,selectSelements="extend")
    print("Map Name: "+mapp[0]['name'])
    elements_count = 0
    for i in mapp[0]['selements']:        
        if i['label'][0:2] == 'AP':
            triggers = get_triggers(i['label'][0:5]) 
            if triggers:
                i['elements'] = triggers
                elements_count+=1
                i['elementtype'] = 2
                i['iconid_off'] = 196
                i['iconid_on'] = 197
                print("processed "+i['label'])
                #print("----------")
                print(i['elements'])
    #print(mapp[0]['selements'])
    try:
        zapi.map.update(sysmapid=namespace.m,selements=mapp[0]['selements'])
        print("processed "+str(elements_count)+" elements")
    except ZabbixAPIException as e:
        print(e)
