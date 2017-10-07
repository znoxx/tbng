# TorBOX Next Generation #

## RU
TorBOX Next Generation (TBNG) — это набор скриптов, позволяющий быстро и без особых усилий создать точку доступа к сети [TOR](https://torproject.org) и [I2P](https://geti2p.com) — как проводную, так и беспроводную. 

TBNG является продолжением проекта [Orange TorBOX](https://github.com/znoxx/torbox). 

ТруЪ кроссплатформенность -- проект можно запустить ___не только___  на ограниченном наборе плат Orange Pi/Raspberry Pi,
а практически на __любом Linux__.

Базовые системные требования просты -- _SystemD_, наличие _Network Manager_ и _Python3_. Полный список 
системных требований вы найдёте в документации.

### Быстрый старт

Клонируйте этот репозитарий, ознакомьтесь с документацией (директория doc) в следующем порядке:

* Общее описание
* Руководство по Установке и Настройке
* Руководство пользователя
* Устранение Проблем и Часто Задаваемые вопросы

Для удобства чтения вы можете сконвертировать документацию в формат html (потребуется pandoc и make):
```
cd doc
make
```
Или ознакомиться с документацией [здесь](http://tbng.ml) — снапшоты публикуются на регулярной основе. 

Установите TBNG согласно документации, перезагрузите устройство и начинайте использовать!

Возможности:

* "Прозрачно" использовать TOR на любом подключенном устройстве.
* Получать доступ к сети I2P.
* Блокировать нежелательный трафик (баннеры).
* Работать как через проводной канал, так  и беспроводной (зависит от используемого оборудования).
* Управлять системой через web-интерфейс.


## EN
TorBOX Next Generation (TBNG) — is a set of scripts, which allows fast and almost effortless creation of [TOR](https://torproject.org) and [I2P](https://geti2p.com) Access Point (wireless and wired).

TBNG is a sequel of [Orange TorBOX](https://github.com/znoxx/torbox) project.

Totally hardware-agnostic — can be run ___not only___ on limited set of Orange Pi/Raspberry Pi devices, but on __virtually any Linux__.

Basic requirements are _SystemD_, _Network Manager_ and _Python3_. 
Full list of system requiremets is described in project documentation.

### Quick start

Clone this repository, get familiar with documentation (doc folder) in following order:

* Overview
* Install and Setup Guide
* User Manual
* Troubleshooting & FAQ

For your convinience documentation can be converted to  html (you will need pandoc and make):
```
cd doc
make
```
Or get familiar with it [here](http://tbng.ml) — snapshots are published regularily.

Install TBNG according to documentation, reboot the device and start using it!

Features:

* "Transparently" use TOR on any connected device.
* Access the I2P network.
* Block unwanted traffic (banners).
* Work both through a wired channel, and wireless (depends on the equipment used).
* Manage the system through the web-interface.

