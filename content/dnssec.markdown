Title: DNSSEC is kind of a pain
Date: 2013-11-02 17:36
Author: jchen
Category: blog
Tags: linux, osx, server admin
Slug: dnssec-pain

[undocumented errors](https://blog.mozilla.org/it/2013/05/16/rfo-dnssec-resolution-failures-mozilla-org-201305151800-pdt-872818/) kill me.

> Investigation found that the DNSSEC signer was refusing to sign the zone, providing only the error “fatal: cannot find SOA RRSIGs“. In hindsight, this undocumented error indicates that the zone’s ZSK has expired.

Today I was just hacking away at updating [libcloud](https://libcloud.apache.org/) support for [Linode](https://www.linode.com) [NodeBalancers](https://www.linode.com/nodebalancers/) when I realized that some of my emails and stuff weren't working correctly.

<!-- PELICAN_END_SUMMARY -->

My first thought was that the Linode that hosts most of my stuff ran into some weird issue. But connectivity was fine and services seemed to be running ok. At that point I turned to mtr to try to figure out what's up.

I tried to do an mtr, but it took a while, so I figured I'd check if the things were resolving correctly.

```
jchen@hobbes> dig sjchen.net
; <<>> DiG 9.8.3-P1 <<>> sjchen.net
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: FORMERR, id: 5725
;; flags: qr rd ra; QUERY: 0, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0

;; Query time: 78 msec
;; SERVER: 192.168.4.1#53(192.168.4.1)
;; WHEN: Sat Nov  2 16:37:52 2013
;; MSG SIZE  rcvd: 12

```

what.jpg.

Hopefully it's just my local resolver?

```
jchen@hobbes> dig @8.8.4.4 sjchen.net
; <<>> DiG 9.8.3-P1 <<>> @8.8.4.4 sjchen.net
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 24423
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;sjchen.net.            IN  A

;; Query time: 39 msec
;; SERVER: 8.8.4.4#53(8.8.4.4)
;; WHEN: Sat Nov  2 16:40:14 2013
;; MSG SIZE  rcvd: 28
```

Full RAEG mode engaged. I verified that ns[1-5].linode.com were resolving things correctly, and they were. At that point I remembered that Google DNS and my local resolver verified DNSSEC, so my next thought was that keys had probably expired as I haven't touched DNS in a while.

So I make some [keys]({filename}/dnssec-on-nsd3.markdown) and get `fatal: cannot find SOA RRSIGs`. Moar raeg.

I consulted a co-worker who's more dns-savvy that myself, and learn of the `-K` parameter, which apparently is some magic to point dnssec-signzone to a directory where it will automatically find the correct keys and do the needful.

Well cool. Things are fixed, slightly anticlimatic.

