Script  **zabbix_map_wifi_aruba_update.py**
is update zabbix wifi maps.
It search map, names begins with AP, and then check items, add
- Triggers, if it persist on wifi Controllers Aruba
- Mac adress (only for Aruba)
- Channels (only for aruba)

script also use zabbix_sender to update item "Scripts wifi maps update status" on zabbix server. It used to control script function.

To first use, modify username and password in file "mapchanger.conf.example" and rename it to "mapchanger.conf"

usage: zabbix_map_wifi_aruba_update.py [-h] [-p] [-all] [-m M]

optional arguments:
  -h, --help  show this help message and exit
  -p          Print map names
  -all        Change all AP maps
  -m M        change only one map id, not work with -all
  
Script  **zabbix_map_wifi_msm_update.py**
is update zabbix wifi maps.
It search map, names begins with AP, and then check items, add
- Triggers, if it persist on wifi Controllers HP MSM

script also use zabbix_sender to update item "Scripts wifi maps update status" on zabbix server. It used to control script function.

To first use, modify username and password in file "mapchanger.conf.example" and rename it to "mapchanger.conf"

usage: zabbix_map_wifi_msm_update.py [-h] [-p] [-all] [-m M]

optional arguments:
  -h, --help  show this help message and exit
  -p          Print map names
  -all        Change all AP maps
  -m M        change only one map id, not work with -all