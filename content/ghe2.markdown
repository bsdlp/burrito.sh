Title: GitHub Enterprise 2.0.0 on Linode
Date: 2014-11-12 16:06
Author: jchen
Category: blog
Tags: linux
Slug: ghe2-on-linode

[![GitHub Logo](/thumbs/GitHub_Logo_thumbnail_wide.png)](https://enterprise.github.com)

<!-- PELICAN_BEGIN_SUMMARY -->
The new [GitHub Enterprise
2.0.0](https://enterprise.github.com/releases#release-2.0.0) release is
awesome. However, it only comes in an
[.ova](https://en.wikipedia.org/wiki/Open_Virtualization_Format) or as a
deployable [AMI](https://en.wikipedia.org/wiki/Amazon_Machine_Image). In order
to run the jawn on a Linode (or anywhere else), let's pull the raw image out of
the provided `.ova`.

**warning**: Not supported by GitHub, things may not work as expected!
<!-- PELICAN_END_SUMMARY -->

First things first, download the `.ova` file from [your GitHub Enterprise
dashboard](https://enterprise.github.com). I would suggest pulling the download
directly onto your Linode (I'll let you figure out how to do that).

# Setting up the Linode

[Deploy a
Linode](https://www.linode.com/docs/getting-started#provisioning-your-linode),
something big enough (needs at least 80GB of disk space for the rootfs). I
chose a Linode 16GB. I created a 100GB disk image for the rootfs, a 10GB
disk image for the scratch disk, and a 512MB swap disk. You'll also need a
separate raw disk image for user data. Make it at least 10GB, or GHE will
complain.

Start your Linode in [rescue
mode](https://www.linode.com/docs/troubleshooting/rescue-and-rebuild) with all
of those disk images mounted. Remember the block device. Log into the Linode with
[LISH](https://www.linode.com/docs/networking/using-the-linode-shell-lish). Set
a password for the root user by running `passwd`, and start the ssh daemon with
`service ssh start`. Quit out of the LISH session, and log into your Linode via
SSH.

Mount your scratch disk. For me, this is `mount /media/xvdb`, but disk image
order may be different. Remember when I told you to remember the order of the
block devices?

# Doing the needful

Get the `.ova` file you downloaded from GitHub onto the scratch disk, and untar
it with `tar xvf </path/to/the/.ova>`. You should see `ghe-disk1.vmdk` in that
directory.

Rescue mode is simply a special config profile for booting into Finnix, and
Finnix is basically just a souped up debian distribution. Get the `qemu-utils`
package by running `apt-get update && apt-get install -y qemu-utils`. It's
gonna ask you a bunch of questions just install the package maintainer's
version of config files and stuff and move on with life.

Once qemu-utils is installed, let's get a raw disk image out of that `.vmdk`
file. I would recommend doing this in a [screen
session](https://www.linode.com/docs/networking/ssh/using-gnu-screen-to-manage-persistent-terminal-sessions)
because it's going to take a while even on SSD, that disk image is pretty big.

Run `qemu-img convert -f vmdk -O raw </path/to/.vmdk> raw.img` to get the raw
image. Then run `kpartx -v -a raw.img` to map the partitions in the raw image
to a loop device. The output of the command should tell you which device you'll
be looking at. For me, the output looked like this:

```
root@0:/media/xvdb# kpartx -v -a raw.img
add map loop1p1 (254:0): 0 83884032 linear /dev/loop1 2048
```

That means it's at `/dev/mapper/loop1p1`. Let's just dd the image onto your
block device! Refer back to your memorized (or written down if you're more
organized) list of block devices, and run this:

```
dd if=/dev/mapper/loop1p1 of=/dev/xvda
```

Substitute the `/dev/mapper` path with the one you got from `kpartx`, and
`/dev/xvda` with the path to the actual device for your rootfs. This is gonna
take a few minutes if you're on the SSD goodness. Once you do that, power off
your Linode. You may wish to take advantage of the [Linode Images
Beta](https://forum.linode.com/viewtopic.php?f=26&t=11180) to store the rootfs
you just created somewhere safe for possible redeployment later without a
headache.

Mount your rootfs with `mount /media/xvda` (remember to use the actual block
device for your rootfs), and drop this into `/media/xvda/boot/grub/menu.lst` to
use GHE's included custom kernel:

```
timeout 5
title GitHub Enterprise 2.0.0
root (hd0)
kernel /boot/vmlinuz-3.2.0-70-virtual root=/dev/xvda console=/dev/hvc0 ro
```

Edit `/etc/fstab` so that the rootfs is loaded from `/dev/xvda` instead of
`UUID=`, to reflect where user data disk image is located, and swap:

```
# /etc/fstab: static file system information.
# <file system>  <mount point>   <type>  <options>       <dump>  <pass>
proc             /proc           proc    defaults        0       0
/dev/xvda        /               ext4    defaults        0       0
/dev/xvdb        /data/user      ext4    defaults,noauto,noatime,nobootwait        0       2
/dev/xvdc        none            swap    defaults        0       0
```

# Boot it up!

Create a [config
profile](https://www.linode.com/docs/migrate-to-linode/disk-images/disk-images-and-configuration-profiles),
mapping xvda to your rootfs, xvdb to your user data disk image, and xvdc to
swap. Make sure to choose `pv-grub-x86_64` in the kernel dropdown, and save.
Boot it up, and you should be good to go!
