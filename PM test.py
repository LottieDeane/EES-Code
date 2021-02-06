#!/usr/bin/env python3

from pms5003 import PMS5003, ReadTimeoutError

pms5003 = PMS5003()

while True:
    data = []
    try:
        pm_values = pms5003.read()
        Data.append("PM1.0 ug/m3: "+str(pm_values.pm_ug_per_m3(1)))
        Data.append("PM2.5 ug/m3: "+str(pm_values.pm_ug_per_m3(2.5)))
        Data.append("PM10 ug/m3: "+str(pm_values.pm_ug_per_m3(10)))
    except ReadTimeoutError:
        pms5003.reset()
        pm_values = pms5003.read() 
        Data.append("PM1.0 ug/m3: "+str(pm_values.pm_ug_per_m3(1)))
        Data.append("PM2.5 ug/m3: "+str(pm_values.pm_ug_per_m3(2.5)))
        Data.append("PM10 ug/m3: "+str(pm_values.pm_ug_per_m3(10)))
    for i in data:
        print(i)
