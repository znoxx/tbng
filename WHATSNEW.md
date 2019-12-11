# Version history

## 11-Dec-2019
Fix of I2P

## 04-Aug-2019
Massive I2P fix

## 10-Jun-2019
Oracle Java -> OpnJDK8
Node.js to version 12
npm packages upgraded to actual versions

## 09-May-2019
Firewall rules fix to be VPN (pppX) friednly. Mac spoof realtek plugin updated to perform delay allowing kernel module to settle. Documentation fixes.

## 07-Dec-2018
Installer tool fix. Bionic Beaver compatibility update.

## 26-Jul-2018

Java8 repository update, NodeJS version change (now 8), NPM components updated to latest version from npmjs.org 

## 28-Mar-2018

Docker/LXC compatibility introduced, firewall rules deletion rework, documentation update.

## 05-Mar-2018

Updated tor config to align with current recommendations. Removed obsolete directives.

## 04-Feb-2018

Added autogeneration of AP name and password. Useful for mass production.

## 14-Nov-2017

Added functionality to reset DNS cache. Needed when switchig between WAN networks.

Changed settings for dnsmasq: expected effect is to have google dns and fallback to local provider dns on resolution failure (e.g. captive portals with local names).

Added "dnsutils" package to installation script, doc updated.

Upgrade path:

In tbng folder: git pull, then reconfigure dnsmasq with option "-s none", but same interface and parameters of IP. It will update config file.

Manual update of dnsmasq.conf:

Replace string (including comment):

```
server=8.8.8.8 #Change this to your favourite public dns server, if needed
```
to:
```
server=#
server=8.8.8.8
```

## 30-Oct-2017

TOR troubleshooting section updated in documentation, thanks to user feedback.

## 26-Oct-2017

I2P Installer URL fix

## 20-Oct-2017

Fully migrated to GitHub, fixed typos in doc, and repo location for Java

## 04-Oct-2017
English and russian documentation added to repository. First public snapshot version (early release) is published.

TODO: README.md and full GitHUB public repo migration.
