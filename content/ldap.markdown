Title: LDAP Quickstart
Date: 2014-05-10 15:29
Author: jchen
Category: blog
Tags: linux, devops
Slug: ldap-quickstart

[![ldap header image](/thumbs/ldap_thumbnail_wide.jpg)](/img/ldap.jpg)

## Quickstart notes for LDAP:

<!-- PELICAN_BEGIN_SUMMARY -->
LDAP seems to be the "best" solution for a centralized authentication
management system. However, it is also ridiculously overcomplicated. If I had
bigger balls, I would want to write a simplified version. Unfortunately, I
opted to write a quick blog post so I can keep a quick refresher course on the
crap that is LDAP configuration.
<!-- PELICAN_END_SUMMARY -->

### TL;DR:

This is a quickstart for LDAP. You'll probably want to read the manpage or
something. We're running two Debian Wheezy Linodes, `dfw0.serv.pw` and
`dfw1.serv.pw`, with dfw0 being the LDAP server, and dfw1 being just a client
server that we want to log into using creds managed by LDAP.

## LDAP Server:

`apt-get update && apt-get install -y ldap-utils slapd`

Set your LDAP admin password in the debconf prompt, then answer the following
prompts:

```
Omit OpenLDAP server configuration? No
DNS domain name: serv.pw
Organization name: serv.pw
Administrator password: <PASSWORD>
Confirm password: <PASSWORD>
Database backend to use: HDB
Do you want the database to be removed when slapd is purged? No
Move old database? Yes
Allow LDAPv2 protocol? No
```

Good enough.

Add the following lines to `/etc/ldap/ldap.conf`:

```
BASE dc=serv,dc=pw
URI ldap://dfw0.serv.pw/
```

### Add an OU (Organizational Unit):

Make a temporary file named `ou.ldif`:

```
dn: ou=Groups,dc=serv,dc=pw
ou: Groups
objectClass: top
objectClass: organizationalUnit

dn: ou=Users,dc=serv,dc=pw
ou: Users
objectClass: top
objectClass: organizationalUnit
```

Run `ldapadd -x -D cn=admin,dc=example,dc=com -W -f ou.ldif` to add these jawns
into the LDAP db.

### Add a user:

Make a temporary file named `<username>.ldif`, replacing `<username>` with the
username.

```
dn: cn=<username>,ou=Groups,dc=serv,dc=pw
cn: <username>
gidNumber: 5000
objectClass: posixGroup

dn: uid=<username>,ou=Users,dc=serv,dc=pw
uid: <username>
uidNumber: 5000
gidNumber: 5000
cn: <Full Name>
sn: <Last Name>
objectClass: posixAccount
objectclass: organizationalPerson
loginShell: /usr/bin/zsh
homeDirectory: /home/<username>
```

Add the user to the db:

```
ldapadd -x -D cn=admin,dc=serv,dc=pw -W -f <username>.ldif
```

Set a password for the user:

```
ldappasswd -x -D cn=admin,dc=serv,dc=pw -W -S uid=<username>,ou=users,dc=serv,dc=pw
```

You can check if things worked correctly with `ldapsearch`:

```
ldapsearch -x uid=<username>
```

## LDAP Client:

I've now switched over to `dfw1.serv.pw`, which is the server we want to log
into using the LDAP server on `dfw0.serv.pw` to authenticate.

Install the jawns:

```
apt-get install libpam-ldapd libnss-ldapd nslcd -y
```

Respond with something similar to what I got here to the debconf prompts:

```
LDAP server URI:
ldap://dfw0.serv.pw/

LDAP server search base:
dc=serv,dc=pw

Name services to configure:
[x] group
[x] password
[x] shadow
```

For the `nslcd` debconf prompts, answer as so:

```
LDAP server URI:
ldap://dfw0.serv.pw/

LDAP server search base:
dc=serv,dc=pw

LDAP authentication to use: none

Use StartTLS: no
```

Blah blah blah SSL yeah whatever.

Edit `/etc/nslcd.conf` using your favorite `vim`:

```
ldap_version 3
rootpwmoddn cn=admin,dc=serv,dc=pw
```

Add the following bits to `/etc/pam.d/common-session` so that the user's
homedir is created and populated with `/etc/skel/` on first login:

```
session required        pam_mkhomedir.so skel=/etc/skel/ umask=0022
```

OK? Without adding the user to `dfw1`, you should now be able to log into
`dfw1` with that username and the password you set.

## Glossary:

* `CN`: Common Name
* `OU`: Organizational Unit
* `DC`: Domain Component
