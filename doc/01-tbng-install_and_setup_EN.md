# TorBOX Next Generation

##### Install and Setup Guide

## Introduction

This document describes the steps for installing and configuring the TorBOX Next Generation (hereinafter TBNG) script set, a simple and convenient tool for creating access points to the Internet using the TOR (The Onion Router) pseudo-anonymous network.

It is assumed that user:

* Is sufficiently competent in the Linux OS — e.g. can install packages and edit configuration files.

* Has an understanding about Linux network stack

* Familiar with TBNG overview document

It is also assumed, that OS is fully functional, there is no problems with drivers, including network ones and system can access the Internet.

TBNG does not provide "pre-made images" or "working out-of-the box distribution" of any kind and no one will solve problems with drivers other than the user. It is a tool that enhances privacy and yes, it takes some effort to properly configure it.

## System requirements

* SystemD powered Linux (OpenRC, Init.d are not supported and won't be in visible future)

* Network Manager availability (at least in standart packages repository of operating system, if not used at the moment). The version must be at least 0.9.10.0.

* One network interface for Internet access (should work at the time of installation).

* One network interface (virtual TUN/TAP also possible) for the client connection. Ideally, it should already be configured and working.

* A non-root account (a regular user account).

* Ability to get root (either sudo, or need to know the root password).

An excellent option is to put TBNG on a freshly installed system, where there are only standard packages.

TBNG is tested on the following equipment:

* Orange Pi PC 2, Armbian Ubuntu 16.04 unstable mainline kernel, Wifi 1 Realtek 8188EU, Wifi 2 Ralink 2800

* Orange Pi Zero, Armbian  Ubuntu 16.04 stable legacy kernel, Wifi 1 Internal WiFi, Wifi 2 Ralink 2800

* Cubieboard 2, Armbian Debian Jessie stable mainline kernel, Wifi RTL8192CU (concurrent mode)

* Raspberry Pi 1, Raspbian@Debian Stretch, Wifi 1 RTL8188EU, Wifi 2 Ralink 2800

* Different boards under Diet Pi OS.

* VPS x86-64, Ubuntu 16.04, Ethernet, VPN virtual interface

The amount of memory for comfortable work is 512 MB + Swap. A single-core processor from 600..800 MHz is also sufficient for operation.

TBNG is just a set of scripts. The main memory-hungry parts are  web-interface and of course I2P, which uses Java.

## Terms and assumptions

Let's introduce some terms, just to be clear

We will call "outer" network (Internet) —  **WAN**.

The network that TBNG will create for client access will be called **LAN**.

Let's assume that the device (computer, single board computer) is connected to a router, and has access to the Internet. Let the router have the address 192.168.1.1, and the target device for TBNG received the WAN address 192.168.1.x. It can be either a wired interface or wireless, the main thing is to get access to the Internet. 

LAN interface on TBNG has static address — 192.168.222.1. 

Also assume that the Linux user is called _johndoe_, so the home directory will be called _/home/johndoe_.

We will configure TBNG with two wireless network interfaces to illustrate the configuration of the access point on TBNG. The following figure shows an example of work:

![TBNG example configuration](images/image_2.png)

## Getting TBNG project files

Files must be cloned from GIT repository.

`johndoe@linuxbox:~$ git clone https://github.com/znoxx/tbng`

After executing the command, a directory **_tbng_** will appear in the home directory.

```
johndoe@linuxbox:~$ ls -la tbng
drwxr-xr-x 10 johndoe johndoe 4096 Jul 31 13:51 .
drwxr-xr-x 21 johndoe johndoe 4096 Aug 10 13:19 ..
-rw-r--r--  1 johndoe johndoe 1876 Jul 14 20:24 app.js
drwxr-xr-x  2 johndoe johndoe 4096 Jul 25 12:01 bin
-rw-r--r--  1 johndoe johndoe  285 Jul 31 13:51 check-version.js
drwxr-xr-x  3 johndoe johndoe 4096 Aug  4 14:05 config
drwxr-xr-x  4 johndoe johndoe 4096 Aug  4 14:05 engine
-rw-r--r--  1 johndoe johndoe  570 Jul 31 13:51 package.json
drwxr-xr-x  5 johndoe johndoe 4096 Jul 14 20:24 public
-rw-r--r--  1 johndoe johndoe  198 Jul 14 20:24 README.md
drwxr-xr-x  3 johndoe johndoe 4096 Aug  4 14:05 routes
drwxr-xr-x  4 johndoe johndoe 4096 Aug  4 14:05 setup
drwxr-xr-x  2 johndoe johndoe 4096 Aug  4 14:05 views
```

## Installation of required packages

Before configuration, installation of several packages is require. Also one will need **_Java_** for I2P and (and this is very importan) — **_node.js_** и **_npm_** to get web-interface functionality.

Node.js version — not earlier than 4.2.1.

Tested Java version — 8 for ARM platforms from Oracle website.

If system has alredy **_tor_** и **_privoxy_** installed — it is recommended to purge them with configuration files and re-install with default "factory" settings.

For Debian/Ubuntu users, the installation of packages is automated, for users of other distributions — the packages need to be installed via system package manager.

### Automatic install for Debian/Ubuntu

The automatic package installation command is executed with superuser privileges:

`johndoe@linuxbox:~$ sudo run-parts tbng/setup/apt`

Auto-install scripts run for a considerable amount of time. The process will remove tor and privoxy, and their configuration will be saved to a backup. There will also be a couple of additional Java repositories and node.js.

#### Additional steps for Raspbian (Debian Stretch) on Raspberry PI 1

First of all, it's worth mentioning that for RPI 1 the work was checked only in the new Debian Stretch. The version of the headless system finally became available, and also it's just the newest distribution, which should be used.

Raspberry PI 1 requires additional steps *even* with automatic installation of required packages.

The node.js installation script reports that there is no node.js for the armv6l architecture, and a version from Stretch/Raspbian repository will be installed. It _must_ be replaced with a newer version:

```
johndoe@linuxbox:~$ sudo apt-get purge nodejs
johndoe@linuxbox:~$ wget http://node-arm.herokuapp.com/node_latest_armhf.deb
johndoe@linuxbox:~$ dpkg -i ./node_latest_armhf.deb
johndoe@linuxbox:~$ sudo apt-get install npm
johndoe@linuxbox:~$ ln -s /usr/local/bin/node /usr/bin/nodejs
```

Generally those steps are sufficient to continue.

### List of packages for manual install in other distributions

Packages are named as in Debian / Ubuntu. Perhaps some names do not match, you may also need to install the python3 modules via pip. However, this list should be sufficient to find all required packages.

**_curl, sudo, network-manager, iptables, nodejs, python3, tor, tor-geoipdb, obfsproxy, obfs4proxy, privoxy, haveged, shellinabox, links, python3-pexpect, python3-requests, python3-lxml, python3-netiface, dnsutils._**

As it mentioned before,  **_Java_** and **_npm_** must be installed also.

In general, there is a set of scripts in the setup/apt directory that installs packages, so that the user of another distribution will easily identify the actions that need to be performed on his system based on this data.

In addition to installing packages, there is one more important action that you should not forget to do when using non-Debian/Ubuntu — set SUID bit on **_nmcli_**.

Can be done like this:

```
NMCLILOCATION=$(which nmcli)
chmod u+s,a-w $NMCLILOCATION
```

This is required for correct web-interface operation and some other actions.

## Network interfaces operation check-list

Before configuring TBNG, you need to make sure that the network interfaces "involved" in the work are configured correctly. As already mentioned, we have two zones - LAN and WAN.

LAN is used for TBNG clients, WAN — "outer world". For consitency and according to figure abouve **wlan0** is LAN, **wlan1** — WAN.

In this case:

* **wlan0** must be configured with static addres in  /etc/network/interfaces (For Debian/Ubuntu. For other OS, please consult your documentation). Also *it must be UNMANAGED* for Network Manager. Usually, listing interface in /etc/network/interfaces Network Manager restart will make interface to have this unmanaged state.

* **wlan1** in our case *must be MANAGED* for Network Manager. This will allow connection to WiFi networks in web-interface and interface resetting (also via web-interface).

If WAN interface is wired, one must take care to configure it. It can be done via Network Manager, or via /etc/network/interfaces.

## Setting up hostapd and dnsmasq

### dnsmasq

The dnsmasq package performs many useful functions, but in our case it is needed for two important purposes:

* Assign IP addresses via dhcp in LAN zone.

* Cache DNS requests

dnsmasq can be instaled and configured manually , but TBNG do have helper setup script for it.

Script must be run with superuser rights (root). Let's figure out how, using an example:

`johndoe@linuxbox:~$ sudo tbng/setup/configure_dnsmasq.py -i wlan0 -s apt -b 192.168.222.10 -e 192.168.222.30 -m 255.255.255.0`

Here we claim, that dnsmasq will work on interface wlan0 (-i wlan0), we will install it from apt-repository (-s apt), addresses will be assigned from 192.168.222.10 to 192.168.222.30 (options -b, -e) and subnet mask will be 255.255.255.0 (-m).

There is also possible option "-s yum" — in this case dnsmasq installed via yum. Or one can use option "-s none". In this case install step will be skipped and only configuration wiil be applied.

If command execution succeeds:

`johndoe@linuxbox:~$ sudo systemctl restart dnsmasq`

Setup is completed successfully. If LAN interface is wired, one can connect client to TBNG immediately and check, that address is assigned. If not — one must configure wireless access point.

### hostapd

If LAN interface is wireless, then in most cases one will need a wireless access point. Almost all modern distributions contain this package and there are lots of instructions on setting up on the Internet.

However, TBNG contains a helper script to configure the access point.

The user needs to configure the hostapd for the LAN zone (in our case wlan0 interface). This can be done via standart hostapd or with helper script.

Let's check an example:

`johndoe@linuxbox:~$ sudo tbng/setup/configure_hostapd.py -a armhf -i wlan0 -n my_access_point -p mysuperpassword -d nl80211`

Options, used in this command:

* -a armhf — use arm architecture. This is suitable for Orange PI, RP2 and above. For the RPI of the first version, you need to specify armvl6, and for desktop computers x86 or x86_64. For Orange Pi PC2 — aarch64.

* -i wlan0 — interface

* -n — access point name (your future WiFi network)

* -p — password for network

* -d — driver. In the version installed by the script there is both a driver **nl80211** (standard) and **rtl871xdrv** for Realtek wireless adapters. So in case one have Realtek WiFi, appropriate driver must be used.

In general, using a script for a beginner is the preferred way — all settings are done automatically, the binary file is static, all popular architectures are supported.

After installation, you can check the operation of the access point with a command (if one used a script):

`johndoe@linuxbox:~$ sudo systemctl restart hostapd-tbng`

If one used standard hostapd:

`johndoe@linuxbox:~$ sudo systemctl restart hostapd`

If the access point is visible, the installation was successful. Of course it happens that the network is visible, but there is no connection, but this is already a question to the operation of the equipment.

When using the script, the binary file can be found in the folder **_tbng/bin_**, and the configuration in **_tbng/config_**. In case of problems, you can run the binary from the command line and see what happens:

`johndoe@linuxbox:~$ sudo tbng/bin/hostapd-tbng tbng/config/hostapd-tbng.conf`

## Configuration files preparation

One *must* prepare configuration files. TBNG is supplied only with sample files, from which you need to create real configuration files. This is done by simply copying from configfile.json.example files in configfile.json.

```
johndoe@linuxbox:~$ cp tbng/config/tbng.json.example tbng/config/tbng.json
johndoe@linuxbox:~$ cp tbng/config/user.json.example tbng/config/user.json
johndoe@linuxbox:~$ cp tbng/config/torcountry.json.example tbng/config/torcountry.json
```

Next, you need to edit the files, at least tbng.json, because it contains the key information necessary to work.

### Configuration files format

The format used for configuration files is [JSON (Javascript Object Notation)](http://json.org/example.html). They can be edited in a regular text editor. The most important thing is to strictly follow the syntax of JSON. Unfortunately, the JSON format does not provide comments.

##### tbng.json

The most important configuration file. At least it must be aligned with network interface configuration on device with TBNG. Let's take an example:
```
{
  "cputemp": "default",
  "wan_interface": [
   {
     "name": "wlan1",
      "wireless": true,
      "macspoof": {
        "method": "ifconfig"
       }
   } 
  ],
  "lan_interface": [
    {
      "name": "wlan0"
    }
  ],
  "allowed_ports_tcp" : [22,3000,7657,9050,8118,4200],
  "allowed_ports_udp" : [53],
  "lock_firewall": false
}
```

Below mandatory fields are listed.

###### cputemp

The field shows which plug-in is used to read the temperature. At the moment, the value "default" is used, you can change it to the desired one (see the engine/plugins folder).

###### wan_interface

An array of network interfaces for the WAN zone. If more than one interface is specified, you can switch between interfaces.

The "wireless" attribute declares the interface as wireless. There can be only one wireless interface in the WAN list — this is due to the peculiarity of the web-interface. In the future, this restriction may be lifted.

The "macspoof" field describes the method by which the mac-address will be replaced, in other words here one sets plugin for "Mac spoof" operation. If the interface does not support such functionality  it is better to completely remove it.

###### lan_interface

An array of network interfaces for the LAN zone. The main requirement is that the array should not intersect wan_interfaces. That is, you can not use wlan0 in both WAN and LAN simultaneously. The type of interface (wireless = true) can be omitted, it is not used.

Section must not be empty, since interface names are used for with IP Masquerading (NAT).

###### allowed_ports_udp,allowed_ports_tcp

Arrays of ports opened in the firewall for the LAN zone. For example, the user has put some new service on the device with TBNG, and wants to use it on the local network. Then the port used by this service needs to be added to the list (depending on the type of tcp or udp the corresponding array should be added).

Of course, the ports can be "reduced", although ports 22 and 3000 are always opened - specifically to ensure that the user can not lose access to the ssh and web-interface. If this should be excluded, we also edit the "engine" tbng/engine/tbng.py. But already at your own peril and risk (like everything else, however).

###### lock_firewal

A sign that the firewall is closed. When set to true, the firewall blocks connections from the WAN. Set it only when everything is checked and working.

###### allowed_ports_wan_udp,allowed_ports_wan_tcp

Arrays of ports opened in the firewall for the WAN zone. Almost the same as the previous similar option for LAN. Ports are available even if lock_firewall is set to true. In the default configuration settings is not used (WAN is "all closed"), but if TBNG is installed on a leased server (VPS), the configuration should be described for opening VPN, SSH, and other services.

##### user.json

Contains a name and password for accessing the web-interface. The default is webui/webui. Can be replaced with the desired values.

##### torcountry.json

Contains a list of countries for TOR. Required for display in the web interface. If desired, you can slightly reduce it, say, leaving only those countries that are planned to be excluded when working through TOR.

##### runtime.json

This file appears only after the first start TBNG and is used to store settings and restore them. It is not intended for self-editing, but you can delete it if "something went wrong", and reboot the system, or execute the command:

`johndoe@linuxbox:~$ sudo tbng/engine/tbng.py mode restore`

This will bring the system to its original state.

## Primary TBNG setup

So, the settings are formed, the network interfaces are checked — the time to apply the final configuration and use. To start the configuration, do the following:

`johndoe@linuxbox:~$ sudo tbng/setup/configure_componetns.py -u johndoe`

This command does the follwing:

* Validates configuration.

* Sets passwordless sudo for user johndoe for tbng/engine/tbng.py

* Sets tbng.py for autostart (settings are restored on autostart)

* Sets up web-interface and configures it autostart

* Sets up I2P, runs, stops, then configure settings to allow console access

After successful run the system will be ready for use, it is recommended to conduct a power cycle (ie turn off and on).

If, for some reason, the tor and privoxy configuration files are somewhere else, you will need to specify them in the command line options — use the "--help" option).

After successful installation, three new services will appear in the system:

* tbng — loading TBNG settings on system start or creating/applying default settings  (consider this as TBNG "autostart")

* webui-tbng — web-interface

* i2p-tbng — i2p daemon

Congratulations, the system is configured and working !

## Plugins 

TBNG is written in Python, and almost all actions are formalized. That is, calling iptables, starting and stopping daemons, working with Network Manager will be the same almost everywhere, but here are the procedures for reading the processor's temperature, or spoofing mac-addresses will differ not only from core to kernel, but even from system to system. In connection with this, a plug-in mechanism was introduced — plug-ins that implement a small and optional functionality

Plugins are located in the folder tbng/engine/plugins and are named according to the principle family_name.py, where family is a family (for example cputemp), and name is the name that characterizes the plugin. For example, cputemp_default.py reads the CPU temperature in the "normal" way from the cpu0 processor sensor.

At the time of writing, there are only two families — cputemp and macspoof. The first, as it was said, realizes the mechanism of reading the temperature of the processor, the second is the substitution of the mac-address of the network card.

The "example" family is just test plug-ins for development.

The tbng.json configuration file specifies only the action — "cputemp: default", "macspoof: ifconfig".

### Plugins for reading CPU temperature information

The simplest type of plugins. Read the temperature data, form a string, and transmit it to the standard output.

The file is named cputemp_action.py. Check functionality is simple:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py cputemp default`

If the plug-in brought out the temperature, the test was successful. But on the Raspberry Pi 1 process of reading the temperature is different and you need to use the plugin cputemip_rpi1.py, that is:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py cputemp rpi1`

### Plugins for mac spoof

MAC spoof allows you to replace the interface address of the WAN zone. Most likely the user knows the purpose for this action.

The main problem is that mac spoofing works differently on different kernels, kernel modules, and on different hardware.

For example, if the Ralink 2800 adapters perfectly change the MAC address through the ifconfig command (although only in Debian Jessie and Debian Stretch, but not in Ubuntu - there "hinders" Network Manager of a certain version), then to change the MAC on Realtek adapters, you need to unload the current kernel module , execute modprobe with the parameter (new mac). And it turns out that if you have 2 identical Realtek network adapters, the action will be performed for both (since they share one kernel module). And this will definitely put the system into an inoperative state. Experimental or buggy modules for example has even more obstacles.

Unlike the "temperature" plug-ins for macspoof, you need to pass parameters, at least the name of the interface that you need to "spoof".

Here are examples of using plugins in the tbng.conf configuration file and in the plugin_tester.py utility.

#### ifconfig

Performs the substitution of MAC addresses through the command ifconfig — the most simple option. Does not work in Ubuntu (however, it works in Debian Jessie and Stretch).

##### Configuration file record

Format is almost straightforward:

```
{
     "name": "wlan1",
      "wireless": true,
      "macspoof": {
        "method": "ifconfig"
       }
}
```

Enabling spoof on wlan1 interface.

##### Call via plugin_tester

On the command line, you need to pass a JSON string with the interface name:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py macspoof ifconfig '{"name":"wlan1"}'`

#### modrealtek

Performs a substitution of the mac address by unloading the module and reloading it again with the parameter. Can not be used if there is more than one interface of the same type (for example, both wlan0 and wlan1 use the same 8192cu module). Also will not work on systems where the interface name contains a mac-address.

##### Configuration file record

Format is slightly more complicated:

```
 {
     "name": "wlan1",
      "wireless": true,
      "macspoof": {
        "method": "modrealtek",
        "parameters": {
         "module_name": "8192cu"
        }
     }
}
```

Enable spoof on wlan1 interface __and__ point to kernel module name which must be reloaded.

##### Call via plugin_tester

On the command line, you need to pass a JSON string with the interface name __and__ kernel module name for reloading:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py macspoof modrealtek '{"name":"wlan1","module_name":"8192cu"}'`

### Creating your own plugin

To write your own plug-ins you need Python 3.x.

The plugin is started by calling the _*plugin_main*_ function. To get started, several plug-ins are delivered including elementary families "example", for testing you can use the utility _*tbng/engine/plugin_tester.py*_. The use is fairly strtaightforward and will not raise questions even for a beginner in Python, especially since all source code is available.

