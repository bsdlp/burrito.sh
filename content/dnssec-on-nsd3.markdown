Title: dnssec on nsd3
Date: 2013-02-13 22:05
Author: jchen
Category: blog
Tags: freebsd, linux, server admin, tutorial, web
Slug: dnssec-on-nsd3

I'm currently working to dnssexify all of my domains, and it's going
pretty well. I'm surprised I haven't done this sooner. By signing your
zones, you're securing your domain with a chain of trust that allows
users to verify that DNS lookups aren't being faked by someone who may
have poisoned their ISP's resolver cache. This is kind of similar to the
basis of SSL certificates, but it protects the DNS lookup process, which
is in essence the first process to reaching a website when one types in
a URL into their browser. So here's how I've been signing my zones.  
  
I'm working with nsd3 on FreeBSD 9.1 AMD64:  
` NSD version 3.2.15 Written by NLnet Labs.`

Copyright (C) 2001-2011 NLnet Labs. This is free software.  
There is NO warranty; not even for MERCHANTABILITY or FITNESS  
FOR A PARTICULAR PURPOSE.  
</code>  
The configuration files for nsd are located in `/usr/local/etc/nsd/`,
and here's how the directory tree looks:

    /usr/local/etc/nsd/
    ├─ keys
    │   └─ example-com
    │       ├─ Kexample.com.+005+43917.key
    │       ├─ Kexample.com.+005+43917.private
    │       ├─ Kexample.com.+005+51472.key
    │       ├─ Kexample.com.+005+51472.private
    │       └─ dsset-example.com.
    ├─ nsd.conf
    ├─ nsd.conf.sample
    ├─ slaves.conf
    ├─ var
    │   ├─ db
    │   │   └─ nsd
    │   ├─ log
    │   └─ run
    ├─ zones
    │   ├─ example.com.zone.signed
    │   └─ example.com.zone
    └─ zones.conf

This is how I do it, and it works for me. I'm not going to go into
detail as to the contents of my configuration files, as that's out of
the scope of this post.

First step is to create a zone-signing key pair for your existing
zonefile:

    # /usr/sbin/dnssec-keygen -r/dev/random  -a RSASHA1 -b 1024 -n ZONE example.com
    Kexample.com.+005+43917

Next you'll want to create Secure Entry Points (SEP) keys:

    # /usr/sbin/dnssec-keygen -r/dev/random  -f KSK -a RSASHA1 -b 1280  -n ZONE example.com
    Kexample.com.+005+51472

This should create the following files:

    Kexample.com.+005+43917.key
    Kexample.com.+005+43917.private
    Kexample.com.+005+51472.key
    Kexample.com.+005+51472.private

You'll want to add your keys to your zonefile, adjusting the path as
necessary:

    $include /usr/local/etc/nsd/keys/example-com/Kexample.com.+005+43917.key ;ZSK
    $include /usr/local/etc/nsd/keys/example-com/Kexample.com.+005+51472.key ;KSK

This is what your zonefile should look like after you've added those two
lines. Keep in mind your syntax may be different for the rest of the
zonefile:

    example.com.        86400       IN      SOA         ns1.example.com.    noc.example.com. (
                                        2013021316      ;serial
                                        900           ;Refresh
                                        14400            ;retry
                                        864000          ;expire
                                        86400           ;min ttl
                                        )

                                            NS              ns1.example.com.
                                            NS              ns2.example.com.

    example.com.        300         IN      A       192.168.1.1

    $include /usr/local/etc/nsd/keys/example-com/Kexample.com.+005+43917.key ;ZSK
    $include /usr/local/etc/nsd/keys/example-com/Kexample.com.+005+51472.key ;KSK

Then you'll want to actually sign the zone:

    # /usr/local/sbin/dnssec-signzone    
   -o example.com    
   -k /usr/local/etc/nsd/keys/example-com/Kexample.com.+005+51472   
   /usr/local/etc/nsd/zones/example.com.zone   
   /usr/local/etc/nsd/keys/example-com/Kexample.net.+005+43917.key

After that, just rebuild your NSD db and reload to put it into effect:

    # /usr/local/sbin/nsdc rebuild
    # /usr/local/sbin/nsdc reload

That's it! You're done.

    $ dig example.com DNSKEY
