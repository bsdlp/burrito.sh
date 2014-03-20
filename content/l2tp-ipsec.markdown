Title: L2TP/IPSEC
Date: 2014-03-20 02:30
Author: jchen
Category: blog
Tags: server admin, tutorial, linux
Slug: l2tp-ipsec

In many [cases where OpenVPN can be detected and
banned](https://github.com/OpenVPN/openvpn/pull/3), L2TP/IPSEC can become a
viable alternative for tunnelling traffic. Unfortunately, L2TP/IPSEC is not as
popular as OpenVPN. As such, support and documentation for L2TP/IPSEC may not
be as thorough or as user-friendly. This post aims to simplify the use of
L2TP/IPSEC using a Linode running Debian Wheezy.

I assume that you've already [set up your Linode account and deployed your
first Linode using Debian](https://library.linode.com/getting-started). So,
let's get started!

<!-- PELICAN_END_SUMMARY -->

## Installation:

Firstly, make sure your Linode is up to date:

```
apt-get update
apt-get upgrade
```

Next, install the necessary software:

`apt-get install openswan xl2tpd iptables-persistent` 

When installing `openswan`, you'll be prompted to configure openswan to use
certificate authentication. You can simply have `openswan` do the needful and
create a self-signed cert for you.

[![openswan configuration step 1](/thumbs/openswan1_thumbnail_wide.png)](/img/openswan1.png)

[![openswan create cert](/thumbs/openswan2_thumbnail_wide.png)](/img/openswan2.png)

[![openswan rsa key length](/thumbs/openswan3_thumbnail_wide.png)](/img/openswan3.png)

[![tell openswan to do it](/thumbs/openswan4_thumbnail_wide.png)](/img/openswan4.png)

[![set cert country code](/thumbs/openswan5_thumbnail_wide.png)](/img/openswan5.png)

[![set state/province](/thumbs/openswan6_thumbnail_wide.png)](/img/openswan6.png)

[![set locality](/thumbs/openswan7_thumbnail_wide.png)](/img/openswan7.png)

[![set common name](/thumbs/openswan8_thumbnail_wide.png)](/img/openswan8.png)

We're done; that was easy!

## Configuration:

We'll also need to make some adjustments to `/etc/sysctl.conf`:

```
sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward = 1/' /etc/sysctl.conf
sed -i 's/#net.ipv4.conf.all.accept_redirects = 0/net.ipv4.conf.all.accept_redirects = 0/' /etc/sysctl.conf
sed -i 's/#net.ipv4.conf.all.send_redirects = 0/net.ipv4.conf.all.send_redirects = 0/' /etc/sysctl.conf
```

To make the settings go live right meow, run `sysctl -p`. Otherwise, you can
reboot.

Next, run the following changes to edit `/etc/ipsec.conf`, but make sure the
edit the following values:

`<cert>`: The name of cert generated, usually `<common_name>Cert.pem`.
`<public_ip>`: The public ipv4 address of your Linode.

```
mv /etc/ipsec.conf{,.dist}
cat <<EOF > /etc/ipsec.conf
config setup
    protostack=netkey
    nat_traversal=yes
    virtual_private=%v4:172.16.0.0/12
    plutoopts="--interface=eth0"

conn pub-nat
    rightsubnet=vhost:%priv
    also=pub

conn pub
    authby=rsasig
    leftrsasigkey=%cert
    rightrsasigkey=%cert
    leftcert=<cert>
    pfs=no
    auto=add
    keyingtries=3
    rekey=no
    ikelifetime=8h
    salifetime=10m
    type=tunnel
    left=<public_ip>
    leftprotoport=17/1701
    right=%any
    rightprotoport=17/1701
    dpddelay=10
    dpdtimeout=90
    dpdaction=clear
EOF
```

On to configuring the L2TP server daemon, again replacing the following values:

`<public_ip>`: The public ipv4 address of your Linode.
`<hostname>`: The Linode's hostname.

```
mv /etc/xl2tpd/xl2tpd.conf{,.dist}
cat <<EOF > /etc/xl2tpd/xl2tpd.conf
[global]
listen-addr = <public_ip>
port = 1701
ipsec saref = yes

[lns default]
ip range = 10.0.1.50-10.0.1.255
local ip = 10.0.1.1
refuse chap = yes
refuse pap = yes
require authentication = yes
ppp debug = no
pppoptfile = /etc/ppp/options.xl2tpd
length bit = yes
exclusive = no
assign ip = yes
name = <hostname>
EOF
```

Now, edit `/etc/ppp/options.xl2tpd`:

`<resolver_ip>`: Your Linode resolvers, which you can find in the [Remote
Access](https://library.linode.com/remote-access) section of the Linode
Manager.
`<hostname>`: The Linode's hostname.

```
mv /etc/ppp/options.xl2tpd{,.dist}
cat <<EOF > /etc/ppp/options.xl2tpd
refuse-mschap-v2
refuse-mschap
ms-dns <resolver_ip>
ms-dns <resolver_ip>
asyncmap 0
auth
crtscts
idle 1800
mtu 1200
mru 1200
lock
hide-password
local
name <hostname>
proxyarp
lcp-echo-interval 120
lcp-echo-failure 10
EOF
```

Set your username and password for PPP in `/etc/ppp/chap-secrets`:

`<hostname>`: The Linode's hostname.
`<username>`: Your PPP username.
`<password>`: Your PPP password.

```
cat <<EOF > /etc/ppp/chap-secrets
<username> <hostname> <password> *
EOF
```

Restart your services:

```
service ipsec restart
service xl2tpd restart
```

Make Debian start these services at boot:

```
update-rc.d -f ipsec defaults
update-rc.d -f xl2tpd defaults
```

Check ipsec configuration:

```
ipsec verify
```

Set your iptables rules:

```
iptables -t nat -A POSTROUTING -s 10.0.1.0/24 -j SNAT --to-source <ip_address>
iptables -A FORWARD -s 10.0.1.0/24 -j ACCEPT
iptables -A FORWARD -d 10.0.1.0/24 -j ACCEPT

iptables-save > /etc/iptables/rules.v4
```

