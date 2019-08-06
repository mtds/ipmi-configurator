#!/usr/bin/env python

# IPMI Configurator

#
# Read from a INI config file a list of machines HW type, followed by records in this form:
# sensor_NUM="EventFilter, Sensor Number, SensorID, Upper Non-Critical Threshold, Upper Critical Threshold"
#
# 1. Iterate through the [sections] of the INI file.
# 2. Is there a product name correspondance in the config file?
# 3. If yes then proceed further to parser the data for the sensor 
#    and create a PEF event.

import getopt
import os
import shlex
import subprocess
import sys
from ConfigParser import SafeConfigParser


# EventFilter, Sensor Number, SensorID, Upper Non-Critical Threshold, Upper Critical Threshold
def pef_config(sensor_data):
   eventFilter, sensorNumber, sensorID, upNcTh, upCrTh = sensor_data.split(",")

   # Light sanity check:
   if eventFilter.isdigit() and upNcTh.isdigit() and upCrTh.isdigit() and sensorNumber.isdigit():
   
      # Get the PEF list and verify if we have already defined an alert for the sensor in question:
      pef_list = subprocess.check_output(['/usr/bin/ipmitool','pef','list'])
      if sensorNumber not in pef_list:
 
         # Set IPMI non-critical/critical thresholds:
         subprocess.call(shlex.split("/usr/sbin/ipmi-config --category=sensors --commit -e "+sensorID+":Upper_Non_Critical_Threshold="+upNcTh))
         subprocess.call(shlex.split("/usr/sbin/ipmi-config --category=sensors --commit -e "+sensorID+":Upper_Critical_Threshold="+upCrTh))

         # Build the event filter string:
         eventFilter_string = "Event_Filter_"+eventFilter

         # Setup IPMI PEF: 
         if subprocess.call(shlex.split("/usr/sbin/ipmi-config --category=pef --commit -e "+eventFilter_string+":Sensor_Type=Temperature \
                                                                                       -e "+eventFilter_string+":Event_Severity=Critical \
                                                                                       -e "+eventFilter_string+":Event_Filter_Action_Power_Off=yes \
                                                                                       -e "+eventFilter_string+":Enable_Filter=yes \
                                                                                       -e "+eventFilter_string+":Sensor_Number="+sensorNumber)): return 0
         else:
             return 1 
      else:
          return 0 # PEF already defined.
   else:
      print "WARNING: Check your temperature thresholds or the sensor/event filter number --> they cannot be in alphanumerical format!!"
      sys.exit(1)


def main(argv):

   if not os.geteuid() == 0:
       sys.exit("\nOnly root can run this script\n")

   # Preset the return status to a safe value:
   pef_status = 0

   # Initizialize the parser:
   parser = SafeConfigParser()

   # Config filename (hardcoded in case no config file is provided on the cmd line):
   config_file = 'ipmi_sensors.ini'

   # The script will accept only two options:
   # -h print (generic help msg)
   # -f config_file (a config file in INI format)

   opts, args = getopt.getopt(argv,"hf::")
   for opt, arg in opts:
      if opt == '-h':
         print sys.argv[0] + ' -f <cfgfile>'
         sys.exit()
      elif opt in ("-f"):
         config_file = arg

   parser.read(config_file)

   for section_name in parser.sections():
       system_name = subprocess.check_output(['/usr/sbin/dmidecode','-s', 'system-product-name'])
       if (system_name.replace(" ", "")).rstrip('\n') in section_name:
           for name, value in parser.items(section_name):
              pef_status = pef_config(value)

   if pef_status == 0:
       sys.exit(0)
   else:
       sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])

