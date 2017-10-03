# TorBOX Next Generation
##### Overview

## What is it

TorBOX Next Generation (hereinafter TBNG) —  is a set of scripts for the Linux OS which allows fast and effortless deploy of secure internet access points.

User has an opportunity to:

* Use TOR transparently

* Gains access to [I2P network](https://geti2p.net/).

* Block unwanted traffic (banners/ads).

* Work via wireless or wired channel (depends on actual equipment).

* Manage system via web-interface.

## What for

TOR, the same The Onion Router — a set of utilities for obtaining pseudo-anonymous access to the Internet. 
Each packet sent to a node through the TOR goes through a chain of nodes, so the original packet address for the end node is hidden. 
You can read more about this in the [official project documentation](https://www.torproject.org/about/overview.html.en).
TBNG's goal is to automate the configuration and provide a simple interface that can be accessed from almost any modern device — smartphone, tablet or computer.

## For whom

### Intended audience

Using the ready-made configured system is as simple as possible — to connect to the configured network and select the desired mode of operation via the web interface.

The initial setup and installation will require certain skills in Linux, such as:

* Working with the command line.

* Ability to install needed packages.

* Change configuration of network interface (via configuration file).

* Basic understanding of  TCP/IP in Linux.

* In some cases — readiness to compile a driver from source code, especially for some weird network device (hi, Realtek Wifi!).

### Hardware requirements

* A device that is compatible with Linux is a regular computer, rented VPS (KVM or better), a single-board Raspberry Pi-level computer.

* Two or more network interfaces. One is required to connect clients, the second to connect to the Internet. It is possible to use a virtual interface, such as ** tun / tap ** when working through a VPN.

### OS requirements

#### System

Linux, better Debian / Ubuntu. At least, it is tested on these OS.

#### Mandator packages without which nothing will work properly

* systemd 

* Network Manager 

* sudo 

Last two should be available at least in your Linux distribution repository.

#### User accounts

For general activity you need an account with no superuser rights (non-root), _but_ root rights are required during the installation.
So you should know your root password or be able to execute sudo command.

Generally, any major modern Linux distro should work, excel most marginal ones. OpenWRT, Alpine Linux are not supported and won't be supported in visible future.

## How it works

After successful installation and initial configuration, the target device becomes an Internet access point, and all client traffic is redirected through the [TOR network](https://torproject.org/).
In addition, you can configure the filtering mode for traffic — deleting advertisements, "Like" buttons, etc (through the package [Privoxy](https://www.privoxy.org/)).
It is also possible to use the service [I2P](http://geti2p.com). Detailed configuration is available in the user manual.

#### General working diagramm

![TBNG work schematics](images/image_0.png)

Client devices connect to interfaces ** _ lan0 ... lanX _ ** — they can be either wired or wireless.
The device addresses are assigned using the [dnsmasq package](http://www.thekelleys.org.uk/dnsmasq/doc.html).

Using the [iptables rules](https://www.netfilter.org/), traffic is routed either through the TOR + Privoxy, TOR, or directly. For traffic routing, [IP Masquerading](http://tldp.org/HOWTO/IP-Masquerade-HOWTO/ipmasq-background2.1.html) (also known as NAT) is used.

#### TBNG project componetns

TBNG does not use binary files, all components are written in Python.
During installation, you need to install some packages (Python3, Tor, Privoxy, iptables and others).
Some of them may already be present in the system.
A complete list of components is available in the installation and configuration manual.

Key project componets are on diagram below.

![TBNG key componets](images/image_1.png)

TBNG can be managed via the web-interface or via the command line (ssh or the web version [shell-in-a-box](https://www.tecmint.com/shell-in-a-box-a- web-based-ssh-terminal-to-access-remote-linux-servers/)).

