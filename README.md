# TorBOX Next Generation #

## RU:
TorBOX Next Generation (TBNG) -- это набор скриптов, позволяющий быстро и без особых усилий создать точку доступа к сети [TOR](https://torproject.org) -- как проводную, так и беспроводную. 

TBNG является продолжением проекта [Orange TorBOX](https://github.com/znoxx/torbox), но при этом никак не привязан к аппаратной части, то есть его можно запустить не только 
на ограниченном наборе плат OrangePi, а практически на любом Linux, управляемом через _SystemD_, имеющим возможность запускать _Network Manager_ и _Python3_. Полный список 
системных требований вы найдёте в документации.

### Быстрый старт

Клонируйте этот репозитарий, ознакомьтесь с документацией (директория doc) в следующем порядке:
* Общее описание
* Руководство по Установке и Настройке
* Руководство пользователя
* Устранене Проблем и Часто Задаваемые вопросы
Для удобства чтения вы можете сконвертировать документацию в формат html (потребуется pandoc и make):

```
cd doc
make
```
Установите TBNG согласно документации, перезагрузите устройство и начинайте использовать!

## EN:
TorBOX Next Generation (TBNG) -- is a set of scripts, which allows fast and almost effortless creation of [TOR](https://torproject.org) Access Point (wireless and wired).

TBNG is a sequel of [Orange TorBOX](https://github.com/znoxx/torbox) project, but now it can be run not only on limited set of Orange Pi devices, but on virtually any Linux, driven  
by _SystemD_, having _Network Manager_ and _Python3_. Full list of system requiremets is described in project documentation.

### Quick start

Clone this repository, get familiar with docs in following order:
* Overview
* Install and setup guide
* User manual
* Troubleshooting & FAQ
For your convinience documentation can be converted to  html (you will need pandoc and make):

```
cd doc
make
```
Install TBNG according to documentation, reboot the device and start using it!

