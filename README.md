# IPMI Configurator

## Why?

There's no shortage of scripts which can interact with BMC cards and extract relevant information out of it. Although most of these can do an egregious job, the vast majority suffer from the following issues:

* they are tight coupled with some alerting/monitoring system (e.g. Nagios);
* they try to identify the HW type of the server underneath and based on that set the thresholds and alerts.

The second issue can be quite painful, because no standard between HW producers can guarantee you to have the same name for sensors on different kind of servers.

This script takes a different approach: the data about the sensor (ID and Name), event filter number and temperature thresholds comes from a configuration file.  
If the 'system-product-name', extracted from *dmidecode* output, matches the one provided in the configuration file then the script will create one or more PEF (*Platform Event Filtering*)  
events for the sensors listed.

The idea is based on a simple fact: sysadmins knows beforehand which kind of HW they are dealing with and can extract the sensible thresholds and sensor IDs/names from the cmd line tools.  
Once these data are available, the script will just digest all of them through the configuration file.

## Configuration file

It's based on the *INI* format:

```
[system-product-name]
sensor1=16,1,4_System_Temp,55,58
```

The fields have the following meaning:
* EventFilter number;
* Sensor number;
* Sensor ID;
* Upper Non-Critical Threshold
* Upper Critical Threshold

## Prerequisites

* BMC card which supports the IPMI protocol (from version 1.5 to 2.0).
* Packages:
  - ipmitool
  - freeipmi

## References

* [IPMI on Wikipedia](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface)
* [IPMI: commands, sensors thresholds, events and filters.](https://github.com/vpenso/scripts/blob/master/docs/hardware/ipmi.md)
* [Info about BMCs](https://www.thomas-krenn.com/en/wiki/IPMI_Basics)

