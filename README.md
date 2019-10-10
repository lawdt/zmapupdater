Script is update zabbix wifi maps.
It search map, names begins with AP, and then check items, add
- Triggers, if it persist on wifi Controllers Aruba or HP MSM
- Mac adress (only for Aruba)
- Channels (only for aruba)

script also use zabbix_sender to update item "Scripts wifi maps update status" on zabbix server. It used to control script function.

To first use, modify username and password in file "mapchanger.conf.example" and rename it to "mapchanger.conf"