Title: nsd3 configuration
Date: 2012-08-09 06:30
Author: nokbar
Category: linux, server admin, tutorial
Slug: nsd3-configuration

I've recently gotten around to setting up my own authoritative
nameservers. So here's some very basic copypasta that should work for
most people. I'm running debian squeeze in this case.

You need the following packages:

-   nsd3
-   ldns-utils
-   dns-utils

<!--more-->

Here is what an nsd zone file looks like. This should work with bind as
well:

    $TTL 86400
    @       IN          SOA         ns1.example.com.    webmaster.example.tld. (
                                        2012080822      ;serial
                                        14400           ;Refresh
                                        14400            ;retry
                                        864000          ;expire
                                        86400           ;min ttl
                                        )

                        NS              ns1.example.com.
                        NS              ns2.example.com.

    ns1     86400       IN      A       NS1.IP.ADDR.HERE
    ns2     86400       IN      A       NS2.IP.ADDR.HERE
    @       300         IN      A       YOUR.IP.ADDR.HERE
    www     300         IN      A       YOUR.IP.ADDR.HERE

mx, cname, txt and other records are added similarly. You should update
the serial number whenever you edit the zone

this is a very basic configuration file for the master nameserver:

    server:
        logfile: "/var/log/nsd.log"
        username: nsd

    key:
        name: KEYNAME
        algorithm: hmac-sha1
        secret: "XFRPRIVKEYHERE"

    zone:
        name: example.com
        zonefile: /etc/nsd3/master/example.com.zone

        #slave
        notify: SLAVE.IP.ADDR.HERE KEYNAME
        provide-xfr: SLAVE.IP.ADDR.HERE KEYNAME

This is what a really basic slave config looks like:

    server:
        logfile: "/var/log/nsd.log"
        username: nsd

    key:
        name: KEYNAME
        algorithm: hmac-sha1
        secret: "XFRPRIVKEYHERE"

    zone:
        name: "example.com"
        zonefile: "/etc/nsd3/slave/example.com.zone"

        #slave
        allow-notify: MASTER.IP.ADDR.HERE KEYNAME
        request-xfr: AXFR MASTER.IP.ADDR.HERE KEYNAME

use the same privkey for both the master and slave. Here's how you
generate a key:

    ldns-keygen -a hmac-sha1 -b 160 -r /dev/random example.com

grab the key using \`cat\`. the keyfile will be the file that is named
K\$domainSOMENUMBERS.private:

    cat Kexample.com.+123+45678.private

grab the key value, and plop it into the configuration files.

you will need to rebuild the db whenever you add zones in nsd.conf
using:

    nsdc rebuild

restart the service, and you're good to go.

verify that it's working using:

    dig @localhost example.com

glhf mileage may vary.
