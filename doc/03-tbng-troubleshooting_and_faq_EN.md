# TorBOX Next Generation

##### Troubleshooting And FAQ


Depending on the hardware configuration, the kernel version and the component, the user may encounter some difficulties when working with TorBOX Next Generation (TBNG). Here, various recipes for problem solving and answers to frequently asked questions will be collected. Remember that system log files (logs) very often facilitate the task and help to eliminate the cause.

## Causes of problems

There are several reasons why TBNG does not work or works incorrectly:

* Driver problems

* Wrong configuration file

* Misuse of TBNG

* Conflict in Firewall rules (iptables)

* Features of the project components used

## Problem resolution

### Driver problem resolution

At the time of this writing, Linux has acquired a sufficient number of device drivers, including wireless network adapters, to ensure the operation of almost any device on the market.

However, before installing TBNG, it is recommended to check if your network equipment is working, in particular, whether the wireless adapter supports the "access point" mode.

For example, Realtek wireless network cards are mostly able to work in this mode, but the service **_hostapd_** in "default" package repositories is usually compiled without support for Realtek mode. Here you can go in three ways — to search for the desired version in alternative repositories, or install it using the utility **_configure_hostapd.py_**, which is bundled with TBNG, and finally —  to build yourself.

On this [link](https://github.com/pritambaral/hostapd-rtl871xdrv) there is enough information on this problem.

### Correcting errors in the configuration file

The TBNG configuration file is located in the config directory and is called tbng.json. 

File format — [JSON](https://ru.wikipedia.org/wiki/JSON) (JavaScript Object Notation). The syntax of the file is quite strict, so that no command can be executed. Check the syntax is quite simple — just give the command:

`sudo ./tbng/engine/tbng.py chkconfig`

It will validate the file.

Sometimes during installation, the file is forgotten to create. Just copy it from the example and edit to your own needs. The file is required for work, so it is necessary to create it.

### Misuse of  TBNG

The project is still designed for the user who understands what one is doing. Some facts:

* TBNG is quite aggressive and often changes firewall rules (iptables), in particular when switching modes of operation.

* Your device acquires the functionality of the router/access point, which introduces some limitations to the familiar style of work.

* TBNG, like any other software product does not give one hundred percent protection from surveillance, hiding the "virtual personality" and other risks.

If something does not work, read the documentation, especially the "General Description" section for understanding the principles of work.

### Conflict in Firewall rules

The iptables firewall, which is used in TBNG, serves not only for blocking connections, but also for routing. The access point, which is organized by means of TBNG, uses Network Address Translation.

For example, your home network uses the 192.168.1.x range. In this case, it is possible to assign an address range of the form 192.168.2.x for TBNG. In this case, the first range will be "visible" from the second when using the "Direct" mode. In the "TOR" or "Privoxy" mode, the first band is no longer available, because TCP packets are "wrapped" in TOR, and it has no idea what your printer with an address is, let's say 192.168.1.55.

No one forbids the inclusion of additional services on the device where TBNG is installed, but they must be properly configured. The easiest way is to "open" the corresponding ports for LAN and WAN in the tbng.conf configuration file.

Here is an example of a configuration where TBNG is installed on a leased server (VPS), which is used as a VPN server.

```
{
  "cputemp": "default",
  "wan_interface": [
   {
     "name": "ens3"
   }
    ],
  "lan_interface": [
    {
      "name": "tap_vpn"
    }
  ],
  "allowed_ports_tcp" : [6022,3000,7657,9050,8118,4200],
  "allowed_ports_udp" : [53],
  "allowed_ports_wan_tcp" :[22,6022,443,992,1194,5555],
  "allowed_ports_wan_udp" :[500,4500],
   "lock_firewall": true
}
```

In the "external network", UDP ports 500, 4500, as well as TCP 1194 and 5555 are additionally allowed, which corresponds to the authorized ports for VPN L2TP.

Nobody forbids "opening" these ports directly through iptables, but you need to remember first about the order of application rules, and secondly, that TBNG often rewrites the firewall rules to ensure functionality. So the safest way to "open a port" is to add it to the configuration file.

### Features of the project components used

TBNG uses a large number of components — it's Network Manager, TOR, and Privoxy. 

Since there is no binding to a particular version (the main thing is not to use frankly old ones) — these same components can in some cases work incorrectly out of the box. All cases of "similar behavior" are taken to the FAQ, so it makes sense to look there first.

The second point, which is worth paying attention to is the functionality for replacing MAC-addresses on adapters. Briefly — it does not always work and not everywhere. That is why the functional is put into the plug-in mechanism and is optional. Obstacles to the job are repaired as device drivers, and kernel and Network Manager. In other words, what works on Debian Jessie can earn on Ubuntu. Or, you need an additional configuration in Debian Stretch.

For Realtek wireless modules, for example, kernel module reload is required. In Ubuntu, this causes the interface to be renamed, which in turn completely destroys the configuration file. Each case should be treated separately and there is simply no general recipe. It is possible to write your own plugins by changing the address, again, if the user is confident in their abilities.

## FAQ — Frequently Asked Questions

##### TOR is not working! What to do?

Service TOR sometimes refuses to start in the system or constantly restarts. The reason is in interaction with systemd. This may be the case with a "too new kernel", or vice versa - with "too old".

There were 2 problems with TOR.

Diagnostics is performed using syslog (/var/log/syslog).

The first one is a fail with NO_NEW_PRIVILEGES error. The fix is quite simple — create a file:

`/etc/systemd/system/tor@.service.d/10-no-new-privileges.conf`

With contents:

```
[Service]
NoNewPrivileges=no
```

Now your should restart TOR — it should run normally.

Second problem — errors, related to APPARMOR, e.g.:

`tor@default.service: Failed at step APPARMOR spawning /usr/bin/tor: No such file or directory`

As written [here](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=808296), problem is solved with editing file:

`/lib/systemd/system/tor.service`

And replacing ExecStart=/bin/true to ExecStart=/usr/bin/tor (or wherever TOR is located in your system). Actually it shows up in Debian Stretch on Raspberry Pi.

#### Unable to connect to WiFi network (external network)

The symptoms are as follows — the list of WiFi is visible, but when trying to connect, even if the password is entered correctly — the system either does not respond, or gives a connection error.

First, you need to check the permissions on the nmcli file. It must have a suid bit set. That is, the file should always be run with root privileges. Yes, it's not safe, but otherwise you'll have to configure a lot of configuration files, and without much hope for success.

File should have mask like this:

```
$ ls -la /usr/bin/nmcli
-r-sr-xr-x 1 root root 600816 Feb 22 2017 /usr/bin/nmcli
```

If there is no "s", then most likely the system has undergone an update and the file has been replaced with a new version.

Run following command:

`sudo chmod u+s,a-w /usr/bin/nmcli`

Or you can fix this with TBNG command:

`sudo tbng/engine/tbng.py patch_nmcli`

If this method does not help, try adding to the file:

`/etc/NetworkManager/NetworkManager.conf`

Following lines:

```
[device]
wifi.scan-rand-mac-address=no
```

More info [here](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=842422).

#### Unable to connect to the device where TBNG is installed

There could be several reasons:

* Network interface is not configured

* Access point is not working

* DHCP does not assign addresses

All this has nothing to do with TBNG, since connectivity is user care. The best way is to connect via the console (monitor, serial port) and look at the configuration. Just in case:

* LAN addresses on TBNG must be static

* They must be unmanaged in Network Manager

* **_dnsmasq_** should use those adresses to assign DHCP

#### MAC Spoof does not work.

Actually it is kind of expected behaviour. Not much can be done here, but sometimes recipe from  "Unable to connect to WiFi network (external network)" may help (adding line to NM config). 

Statistics — in Ubuntu 16.04 mac spoof does not work due to Network Manager, in Debian Jessie — worked fine, in Debian Stretch — worked with NM config changes. 

#### Speed of TOR is so low

Speed faster than 0.5Mbit/s was not observed at all. TOR is not intended for constant usage by-design.

#### Your Access Point settings are not optimal. Mine is better!

Settings are chosen to cover *majority* of devices. One can edit file (in case hostapd-tbng is used):

`tbng/config/hostapd-tbng.conf`

and introduce changes of choice. 

#### Can TBNG run from root account ?

Engine itself runs with sudo only. But web-interface should NOT run under root. It is not safe..

#### I have a server leased from the provider. Physically, it has 1 interface, but there is also a virtual interface — tun0 for VPN. Will TBNG work?

It should. In the configuration, you need to specify that the WAN interface "looks on the Internet", and tun0 is the LAN. So, VPN clients will see the access point's interface and receive Internet traffic with the possibility of using TOR.

But, there are several pitfalls. Some VPNs do not assign addresses to the interface, or generally start late, so TBNG can start earlier. Here you will either have to change the order of the start, or restart **_tbng helper_** at the very end to see all the network interfaces.

#### I'm trying to switch the WAN interface to another, and everything hangs.

Most likely the interface is not configured or there is no network cable/connection. Do not switch to deliberately broken interfaces. If they are not used — remove them from the configuration file, so as not to get confused.

#### What USB WiFi should I buy?

General answer — one which will work with your kernel. 

Little bit more details — Ralink 2800 worked in all modes, survived MAC spoofing (everywhere except Ubuntu 16.04 due to Network Manager). On the other hand dirt-cheap Realtek 8192CU, 8188CUS allowed to use only one NIC in system, since it utilized [Concurrent Mode](http://znoxx.me/2017/09/09/dvukhgholovyi-realtek/). It all depends on your goals.

