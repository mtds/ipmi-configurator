#!/usr/bin/env python

# Ref: https://pymotw.com/2/ConfigParser/

import shlex
import subprocess
from ConfigParser import SafeConfigParser

# EventFilter, Sensor Number, SensorID, Upper Non-Critical Threshold, Upper Critical Threshold
def pef_config(sensor_data):
   eventFilter, sensorNumber, sensorID, upNcTh, upCrTh = sensor_data.split(",")

   # Set IPMI non-critical/critical thresholds:
   subprocess.call(shlex.split("/usr/sbin/ipmi-sensors-config --commit -e "+sensorID+":Upper_Non_Critical_Threshold="+upNcTh))
   subprocess.call(shlex.split("/usr/sbin/ipmi-sensors-config --commit -e "+sensorID+":Upper_Critical_Threshold="+upCrTh.replace('"','')))

   # Build the event filter string:
   eventFilter_string = "Event_Filter_"+eventFilter.replace('"','')

   # Setup IPMI PEF:
   subprocess.call(shlex.split("/usr/sbin/pef-config --commit -e "+eventFilter_string+":Sensor_Type=Temperature"))
   subprocess.call(shlex.split("/usr/sbin/pef-config --commit -e "+eventFilter_string+":Event_Severity=Critical"))
   subprocess.call(shlex.split("/usr/sbin/pef-config --commit -e "+eventFilter_string+":Event_Filter_Action_Power_Off=yes"))
   subprocess.call(shlex.split("/usr/sbin/pef-config --commit -e "+eventFilter_string+":Enable_Filter=yes"))
   subprocess.call(shlex.split("/usr/sbin/pef-config --commit -e "+eventFilter_string+":Sensor_Number="+sensorNumber))

parser = SafeConfigParser()
parser.read('ipmi_sensors.ini')

# 1. Iterate through the [sections] of the INI file.
# 2. Is there a product name correspondance in the config file?
# 3. If yes then proceed to parser the data for the sensor and
#    create a PEF event.

for section_name in parser.sections():
    system_name = subprocess.check_output(['/usr/sbin/dmidecode','-s', 'system-product-name'])
    if system_name.rstrip('\n') in section_name:
        for name, value in parser.items(section_name):
            pef_config(value)

