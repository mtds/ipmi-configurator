# IPMI Configurator

## Why?

There's no shortage of scripts which can interact with BMC cards and extract relevant information out of it. Although most of these can do an egregious job, the vast majority suffer from the following issues:

* they are tight coupled with some alerting/monitoring system (e.g. Nagios);
* they try to identify the HW type of the server underneath and based on that set the thresholds and alerts.

The second issue can be quite painful, because no standard between HW producers can guarantee you to have the same name for sensors on different kind of servers.

This script takes a different approach: the data about the sensor (ID and Name), event filter number and temperature thresholds comes from a configuration file.  
If the 'system-product-name', extracted from *dmidecode* output, matches the one provided in the configuration file then the script will create one or more PEF (*Platform Event Filtering*) events for the sensors listed.

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

## How to create your own config file

The config file has to be based on your own hardware, so the following steps are meant to help:

1. Identify the system through the ``dmidecode`` command:
```bash
~# /usr/sbin/dmidecode -s system-product-name
```
*NOTE*: the ``dmidecode`` command extract the information from **sysfs**. The same result can be achieved looking directly under the ``/sys/devices/virtual/dmi/id`` subdirectory.

2. Extract the list of sensors available on your HW through the ``ipmi-sensors`` command and grep for relevant IDs:
```bash
~# ipmi-sensors -vv | grep -e 'Record ID' -e 'ID String' -e 'Sensor Number'
```

Once the relevant sensor is properly identified (double check with the **Motherboard** manual is recommended), it will be possible to create 
the string in the INI config file related to your HW. Be careful while choosing the PEF number. Usually there are some pre-defined event filters 
already in place (most likely from the HW manufacturer itself). 

In order to check the list of free PEF IDs you can run the following command:
```bash
~# ipmitool pef filter list | grep -E "(inactive|disabled)"
16 | inactive
17 | inactive
18 | inactive
19 | inactive
[...]
```
The output may of course change depending on the PEFs already defined.

## Prerequisites

* BMC card which supports the IPMI protocol (from version 1.5 to 2.0).
* Packages:
  - ipmitool
  - freeipmi

## Build an RPM

``rpmbuild ipmi-configurator.spec``

[Setup an environment to build RPMs (CentOS Wiki)](https://wiki.centos.org/HowTos/SetupRpmBuildEnvironment)

## References

* [IPMI on Wikipedia](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface)
* [IPMI: commands, sensors thresholds, events and filters.](https://github.com/vpenso/scripts/blob/master/docs/hardware/ipmi.md)
* [Info about BMCs](https://www.thomas-krenn.com/en/wiki/IPMI_Basics)

