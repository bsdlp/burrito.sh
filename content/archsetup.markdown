Title: /arch/setup
Date: 2012-03-10 11:22
Author: jchen
Category: blog
Tags: Uncategorized
Slug: archsetup

So finally I got a working template of archlinux on a xen vps in the
netherlands. It does,however, require some effort to get it to the
latest updates. I will try to explain as best I can how I got mine up
and running.

Since most providers are still using the 2010.05 iso, this guide will be
based on that.

**\*\*\*\*\*\*\*WARNING\*\*\*\*\*\*\*\* This guide is NOT a full guide
on how to install archlinux. It is just a quick guide for experienced
arch users on how to get arch working with an outdated template on a xen
vps.**

**Before you get started:**  
I highly recommend reading the [archlinux wiki][] and especially their
[beginner's guide][] and [official installation guide][]. Archlinux is
famous for their incredibly deep and easy to understand wiki articles,
and I consult those wikis even when I'm not using arch.  


**-----------You will need to do these steps in the rescue console in
your control panel--------------**

**First:**  
Check your `/etc/rc.conf` and change your hostname to something you
want.

    # -----------------------------------------------------------------------
    # NETWORKING
    # -----------------------------------------------------------------------
    #
    # HOSTNAME: Hostname of machine. Should also be put in /etc/hosts
    #
    HOSTNAME=""

*change the HOSTNAME field to your desired hostname*

**Second:**  
Check with your provider about how to get your networking set up.
Normally, they would have a article in their knowledge base with all the
information you need to fill in. Open up `/etc/rc.conf` again and find
this block:

    #Static IP Configuration
    lo="lo 127.0.0.1"
    eth0="eth0 123.456.789.123 netmask 255.255.255.0 broadcast 123.456.789.123"
    INTERFACES=(lo eth0)

    # Routes to start at boot-up (in this order)
    # Declare each route then list in ROUTES
    #   - prefix an entry in ROUTES with a ! to disable it
    #
    gateway="default gw 123.456.789.1"
    ROUTES=(gateway)

Change the IP address after eth0 to your vps's IP address, and the
broadcast IP address /should/ be the same as your vps ip address. Then
look in your provider's knowledgebase for what you should fill in for
your netmask and gateway. If you can't find this information, open a
ticket.

**Third:**  
Go to `/etc/pacman.conf` and check that you at least have `[core]`
enabled. Then open up `/etc/pacman.d/mirrorlist` and uncomment some
mirrors.

**Fourth:**  
Run:  
`# pacman -Syyu`  
It will first ask you to update pacman, which you should do, and then
say NO to all of the other updates. It should ask you to run :  
`# pacman-db-upgrade`  
After you upgrade pacman, do this:  
`# pacman -S filesystem --force`  
There is some issue with upgrading the filesystem, so you need to
manually upgrade it. Normally it's not advised to use the --force flag,
but we don't have a choice here. Then after that, run:  
`# pacman -Syyu`  
again, and then you should be up to date!

  [archlinux wiki]: https://wiki.archlinux.org/index.php/Main_Page
    "archlinux wiki"
  [beginner's guide]: https://wiki.archlinux.org/index.php/Beginners%27_Guide
    "beginner's guide"
  [official installation guide]: https://wiki.archlinux.org/index.php/Official_Installation_Guide
    "official installation guide"
