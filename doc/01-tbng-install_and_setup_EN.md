# TorBOX Next Generation

##### Install and setup guide

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

Before configuration, installation of several packages is require. Also one will need **_Java_** for I2P and (and this is very importan) — **_node.js_** и **_npm_*** to get web-interface functionality.

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

**_curl, sudo, network-manager, iptables, nodejs, python3, tor, tor-geoipdb, obfsproxy, obfs4proxy, privoxy, haveged, shellinabox, links, python3-pexpect, python3-requests, python3-lxml, python3-netiface._**

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

`johndoe@linuxbox:~$ sudo tbng/setup/configure_hostapd.py -a arm -i wlan0 -n my_access_point -p mysuperpassword -d nl80211`

Options, used in this command:

* -a arm — use arm architecture. This is suitable for Orange PI, RP2 and above. For the RPI of the first version, you need to specify armvl6, and for desktop computers x86 or x86_64. For Orange Pi PC2 — aarch64.

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

Поле показывает, какой плагин использовать для чтения температуры. В данный момент используется значение "default", можно поменять на желаемый (см. папку engine/plugins).

###### wan_interface

Массив сетевых интерфейсов зоны WAN. Если указан больше, чем один интерфейс — между интерфейсами можно будет переключаться.

Признак "wireless" объявляет интерфейс беспроводным. В списке WAN может быть только один беспроводной интерфейс — это связано с особенностью работы web-интерфейса. В будущем это ограничение, возможно, будет снято.

Поле "macspoof" описывает метод, по которому будет производится подмена mac-адреса, точнее указывается плагин для выполнения операции "Mac spoof". Если интерфейс не поддерживает такой функционал — поле можно полностью убрать из описания и даже лучше это сделать.

###### lan_interface

Массив сетевых интерфейсов зоны LAN. Основное требование — массив не должен пересекаться с wan_interfaces. То есть, нельзя использовать wlan0 и в WAN и в LAN одновременно. Тип интерфейса (wireless=true) можно не указывать, он не используется.

Секция не должна быть пустой — имена интерфейсов используются при настройке IP Masquerading (NAT).

###### allowed_ports_udp,allowed_ports_tcp

Массивы портов, открытых в firewall для зоны LAN. Скажем, пользователь поставил какой-то новый сервис на устройство с TBNG, и хочет им пользоваться в локальной сети. Тогда порт, используемый этим сервисом нужно внести в список (в зависимости от типа tcp или udp соответствующий массив должен быть дополнен).

Конечно, порты можно "сократить", правда порты 22 и 3000 всегда открываются — специально для того, чтобы пользователь не смог потерять доступ к ssh и web-интерфейсу. Если и это нужно исключить — редактируем "движок" tbng/engine/tbng.py. Но уже на свой страх и риск (как и всё остальное, впрочем)

###### lock_firewal

Признак того, что firewall закрыт. Когда выставлено в true, файрволл блокирует соединения из WAN. Включать нужно в последнюю очередь, когда всё проверено.

###### allowed_ports_wan_udp,allowed_ports_wan_tcp

Массивы портов, открытых в firewall для зоны WAN. Почти тоже самое, что и предыдущая аналогичная опция для LAN. Порты доступны даже, если lock_firewall установлен в true. В дефолтной конфигурации этой настройки нет (т.е. "всё закрыто"), но если TBNG устанавливается на арендованный сервер (VPS) — настройку нужно описывать для открытия портов VPN, SSH, и других сервисов.

##### user.json

Содержит имя и пароль для доступа к web-интерфейсу. По умолчанию —  webui/webui. Можно заменить на желаемые значения.

##### torcountry.json

Содержит список стран для TOR. Требуется для отображения в web-интерфейсе. При желании можно его немного сократить, скажем, оставив только те страны, которые планируется исключать при работе через TOR.

##### runtime.json

Этот файл появляется только после первого старта TBNG и используется для хранения настроек и их восстановления. Он не предназначен для самостоятельного редактирования, однако его можно удалить, если "что-то пошло нет так", и перезагрузить систему, либо выполнить команду:

`johndoe@linuxbox:~$ sudo tbng/engine/tbng.py mode restore`

Это привёдет систему в первоначальное состояние.

## Первичная настройка TBNG

Итак, настройки сформированы, сетевые интерфейсы проверены — время применить финальную конфигурацию и пользоваться. Для запуска настройки делаем следующее:

`johndoe@linuxbox:~$ sudo tbng/setup/configure_componetns.py -u johndoe`

Эта команда сделает следующее:

* Проверит целостность конфигурации

* Установить беспарольный доступ через sudo для пользователя johndoe к tbng/engine/tbng.py

* Установит автозапуск tbng.py при запуске системы (будет вызываться восстановление настроек)

* Установит web-интерфейс и настроит его автозапуск

* Установит I2P, запустит, остановит, выполнит настройки для доступа к консоли

После успешной отработки система будет готова к использованию, рекомендуется провести powercycle (т.е. выключить и включить).

Если по каким-то причинам файлы настроек tor и privoxy находятся где-то в другом месте, то нужно будет их указать в ключах командной строки — используйте опцию "--help".

После успешной установки в системе появятся ещё три новых сервиса:

* tbng-helper — восстановление настроек при загрузке

* webui-tbng — web-интерфейс

* i2p-tbng — демон i2p

Поздравляем, система настроена и работает!

## Плагины и их использование

TBNG написана на языке Python, и почти все действия формализованы. То есть вызов iptables, старт и стоп демонов, работа с Network Manager будут одинаковы практически везде, но вот процедуры по чтению температуры процессора, или подмена mac-адреса будут отличаться не только от ядра к ядру, но даже от системы к системе. В связи с этим был введен механизм плагинов — подключаемых модулей, которые реализуют небольшой и необязательный функционал.

Плагины расположены в папке tbng/engine/plugins и именуются по принципу family_name.py, где family — семейство (например cputemp), а name — имя, характеризующее плагин. Например cputemp_default.py — читает температуру процессора "обычным" способом из сенсора процессора cpu0.

На момент написания документа существуют только два семейства — cputemp и macspoof. Первое, как было сказано реализует механизм чтения температуры процессора, второе — подмену mac-адреса сетевой карты.

Семейство "example" — это просто тестовые плагины для разработки.

В файле конфигурации tbng.json указывается только действие — "cputemp: default", "macspoof: ifconfig". 

###   Плагины для чтения информации о температуре процессора

Самый простой тип плагинов. Считывают данные о температуре, формируют строку, и передают её на стандартный вывод.

Файл имеет название cputemp_action.py. Проверить функциональность можно просто:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py cputemp default`

Если плагин вывел температуру, проверка прошла успешно. А вот на Raspberry Pi 1 процесс чтения температуры отличается и нужно использовать плагин cputemip_rpi1.py, то есть:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py cputemp rpi1`

###   Плагины  для mac spoof

MAC spoof позволяет подменять адрес интерфейса зоны WAN. Скорее всего пользователь знает, зачем это нужно.

Основная проблема в том, что mac spoofing работает по-разному на разных ядрах, модулях ядра, и на разном "железе".

Например, если адаптеры Ralink 2800 прекрасно меняют MAC адрес через команду ifconfig (правда только в Debian Jessie и Debian Stretch, но не в Ubuntu — там "мешает" Network Manager определенной версии), то для смены MAC на адаптерах Realtek нужно выгрузить текущий модуль ядра, выполнить modprobe c параметром (новый mac). И выходит, что если у вас 2 одинаковых сетевых адаптера Realtek, действие будет выполнено для обоих (модуль-то один). А это определенно введёт систему в нерабочее состояние. Что уж говорить о всяких экспериментальных модулях, где нужно где-то "подождать", где-то проверить условие.

В отличие от "температурных" плагинов для macspoof нужно передавать параметры, как минимум имя интерфейса, который нужно "спуфить". 

Вот примеры использования плагинов в файле конфигурации tbng.conf и в утилите plugin_tester.py

#### ifconfig

Выполняет подмену мак-адреса через команду ifconfig — наиболее простой вариант. Не работает в Ubuntu (однако, работает в Debian Jessie и Stretch).

##### Запись в конфигурационном файле

Формат записи довольно простой:
```
{
     "name": "wlan1",
      "wireless": true,
      "macspoof": {
        "method": "ifconfig"
       }
}
```

Разрешаем spoof на интерфейсе с именем wlan1.

##### Вызов через plugin_tester

В командную строку нужно передать JSON-строку с именем интерфейса:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py macspoof ifconfig '{"name":"wlan1"}'`

#### modrealtek

Выполняет подмену мак-адреса через выгрузку модуля и загрузку заново с параметром. Нельзя использовать, если есть более чем один интерфейс одного типа (например и wlan0 и wlan1 используют один и тот же модуль 8192cu). Также не будет работать в тех системах, где имя интерфейса содержит mac-адрес. 

##### Запись в конфигурационном файле

Формат записи немного сложнее предыдущего:

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

Разрешаем spoof на интерфейсе с именем wlan1 и указываем имя модуля, который надо перегружать.

##### Вызов через plugin_tester

В командную строку нужно передать JSON-строку с именем интерфейса и именем модуля для перегрузки:

`johndoe@linuxbox:~$ sudo tbng/engine/plugin_tester.py macspoof modrealtek '{"name":"wlan1","module_name":"8192cu"}'`

### Написание собственных плагинов

Для написания собственных плагинов нужно владеть Python третьей версии. 

Запуск плагина выполняется через вызов функции _*plugin_main*_. Для ознакомления поставляется несколько плагинов в том числе элементарные семейства "example", для тестирования же можно использовать утилиту _*tbng/engine/plugin_tester.py*_. Использование достаточно "прозрачное" и не вызовет вопросов даже у новичка в Python, тем более что все исходные тексты доступны. 
