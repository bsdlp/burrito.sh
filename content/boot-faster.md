Title: Boot faster!
Date: 2012-05-07 10:09
Author: nokbar
Category: linux
Slug: boot-faster

falconindy from the Archlinux dev team posted a pretty good write-up
about trimming your modules on his blog. You can read it [here][].
Pretty cool stuff. To cut seconds off your boot time, I suggest using
[systemd][]. Instead of loading services one by one like the traditional
systemV, systemd loads everything in parallel at boot, and defers
loading of non-essential services. I'm seeing around 3-4 seconds cut
from my boot time.

  [here]: http://blog.falconindy.com/articles/optmizing-bootup-with-mkinitcpio.html
  [systemd]: https://wiki.archlinux.org/index.php/Systemd
