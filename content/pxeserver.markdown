Title: Debian Wheezy PXE Server
Date: 2014-03-28 20:41
Author: jchen
Category: blog
Tags: pxe, debian, coreos
Slug: debian-pxe-server

[![pxe server](/thumbs/pxelinux_thumbnail_wide.jpg)](/img/pxelinux.jpg)

<!-- PELICAN_BEGIN_SUMMARY -->
I've recently come into a few 1U servers that I plan on using as a
[coreos](https://coreos.com/) cluster. Instead of having to load up each server
with the needful, I'm setting up a PXE server running on my laptop. This is in
conjunction with my router running tomato.
<!-- PELICAN_END_SUMMARY -->

# PXE Installation/Configuration
First thing you'll probably want to do is to install tftpd-hpa:

`apt-get install tftpd-hpa`

Check the default configuration, it should look something like this, which is
fine:

```
# cat /etc/default/tftpd-hpa
# /etc/default/tftpd-hpa

TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure"
```

Since tftpd is looking in `/srv/tftp`, create the `pxelinux.cfg` directory
under `/srv/tftp`:

`mkdir /srv/tftp/pxelinux.cfg`

`pxelinux.cfg` is a directory as it contains multiple configuration files for
pxelinux. When a server asks pxelinux to serve up the install bits, pxelinux
will first look for the file as the IP address of the target server in
uppercase hex. If that file doesn't exist, then it'll pop a digit from the end
and look for that file. If all fails, it'll default to the file named
`default`.

Since we don't know what the IP addresses of the servers will be right now,
we're just going to name the file `default`.

Drop the following bits into the file:

```
default coreos
prompt 1
timeout 15

display boot.msg

label coreos
  menu default
  kernel coreos_production_pxe.vmlinuz
  append initrd=coreos_production_pxe_image.cpio.gz root=squashfs: state=tmpfs: sshkey="<ssh_pubkey>"
```

Replace `<ssh_pubkey>` with your ssh pubkey.


You'll then want to [download the
files](https://coreos.com/docs/running-coreos/bare-metal/booting-with-pxe/#download-the-files):

```
cd /srv/tftp/
wget http://storage.core-os.net/coreos/amd64-generic/dev-channel/coreos_production_pxe.vmlinuz
wget http://storage.core-os.net/coreos/amd64-generic/dev-channel/coreos_production_pxe_image.cpio.gz
```

Also grab pxelinux.0 from the Debian mirror of choice:

```
cd /srv/tftp/
wget http://ftp.us.debian.org/debian/dists/wheezy/main/installer-amd64/current/images/netboot/pxelinux.0
```

Make sure `tftpd` is enabled at boot, and start it up:

```
update-rc.d -f tftpd-hpa defaults
service tftpd-hpa start
```

You'll also need to have your dhcp server tell your servers where to look for
the PXE server. I'm using tomato, and I just went to `Advanced -> DHCP/DNS ->
Dnsmasq Custom configuration`, and dropped this in the text field:

`dhcp-boot=pxelinux.0,,10.0.0.187`

`10.0.0.187` is the IP address of the PXE server.

Now, when you boot your server in PXE mode, it'll do the needful.

