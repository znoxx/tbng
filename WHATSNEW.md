# Version history

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
