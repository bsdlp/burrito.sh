Title: Adventures in FreeBSD part 1
Date: 2013-01-02 15:35
Author: nokbar
Category: freebsd, server admin, tutorial
Slug: adventures-in-freebsd-part-1

I've recently ordered a new dedicated server from OVH in their new
Canada datacenter. Here are it's specs:

hw.machine: amd64  
hw.model: Intel(R) Atom(TM) CPU D425 @ 1.80GHz  
hw.ncpu: 2  
4GB of ram  
2TB disk (no raid)

For \~\$140 / year.

This is a pretty good deal. I don't really do anything cpu-intensive,
mostly just irssi, some small webhosting, nameserver, git and the
occasional building of software from source. It comes with 1 IPv4, with
the option to get 2 more IP's for "failover" for free, and a /64 of IPv6
addresses. They automate pretty much everything; you can script
deployment for partitioning your hard drive, and you get a wide range of
operating systems to choose from. There's three negatives that affect
me:

-   No IPv6 PTR records
-   Shoddy routing
-   No serial console

The serial console is really the thing that kills, as I'm still pretty
new to freeBSD and so I might break stuff that may cause me to lock
myself out. However, they do have a "netboot" option, which I think is
just like a rescue environment where you can mount your disk image and
do the needful to get your stuff back up and running. Luckily, I haven't
had to use that feature yet, although I might want to make a dry run at
some point just to familiarize myself with how it works.

<!--more-->

Of course, the first thing I did was edit /etc/rc.conf, the /main/
configuration file for the system. This is what mine looks like right
now, a few days after I first set it up:

    sshd_enable="YES"
    ntpdate_enable="YES"
    ntpdate_hosts="213.186.33.99"
    fsck_y_enable="YES"
    nginx_enable="YES"
    php_fpm_enable="YES"
    nsd_enable="YES"
    fail2ban_enable="YES"
    inetd_enable="YES"
    mysql_enable="YES"
    mysql_args="--user=mysql"
    icecast_enable="YES"
    pf_enable="YES"
    pflog_enable="YES"
    teamspeak_enable="NO"
    # Set dumpdev to "AUTO" to enable crash dumps, "NO" to disable
    dumpdev="NO"

    ifconfig_re0="(ipv4 addr)"
    ifconfig_re0_alias0="(ipv4 "failover" addr)"
    defaultrouter="(router)"

    # IPv6 configuration
    ipv6_enable="YES"
    ipv6_static_routes="ovhgw"
    ipv6_route_ovhgw="(ipv6 gateway stuff)"
    ipv6_defaultrouter="(ipv6 gateway stuff)"
    ipv6_ifconfig_re0="(ipv6 addr)"
    hostname="(hostname)"

The first bits with all the \*\_enable is where you would set the bits
to auto-start services on boot, and allow services to be started via
initscripts. The hostname and networking directives should be
self-explanatory.

Next, I set my timezone:

    # cp /usr/share/zoneinfo/Etc/UTC /etc/localtime

Of course I use UTC! It's the only time zone that matters. It might be
easier for most people to use their local time zone, but you'll run into
problems sometimes when you use a program that relies on timestamps.

Next, I initiated the ports tree by running:

    # portsnap fetch extract

Which grabs the ports tree, allowing me to build stuff from the
comprehensive collection of programs. I usually build from ports, and I
try to stay away from mixing ports and packages. Right now I use
portmaster (ports-mgmt/portmaster) to manage my ports collection.
Portmaster is pretty easy. I would recommend it to new users of freeBSD
who are overwhelmed by the ports tree.

**PREVIEW:**  
In the future, I'll be talking about other facets of freeBSD:

-   Ports
-   nsd3
-   irssi
-   nginx
-   php
-   pf (openbsd firewall used in freebsd)

