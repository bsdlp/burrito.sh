Title: drdos
Date: 2012-03-09 14:49
Author: jchen
Tags: gaming, urban terror
Slug: drdos

DRDoS (Distributed Reflected Denial of Service) attacks are the bane of
quake-based server administrators. For a while now, there's been a known
bug in all quake-based games that allows attackers to exploit how quake
handles get status requests to amplify their DDoS attacks. Not only does
this cause issue with potential blacklisting, but it also eats up
bandwidth and effects server performance.

  
According to this [article][], some creative iptables use can help
mitigate DrDoS attacks.

    # create chain
    iptables -N quake3_ddos

    # accept real client/player traffic
    iptables -A quake3_ddos -m u32 ! --u32 "0x1c=0xffffffff" -j ACCEPT

    # match "getstatus" queries and remember their address
    iptables -A quake3_ddos -m u32 --u32 "0x20=0x67657473&&0x24=0x74617475&&0x25&0xff=0x73" -m recent --name getstatus --set

    # drop packet if "hits" per "seconds" is reached
    #
    # NOTE: if you run multiple servers on a single host, you will need to higher these limits
    # as otherwise you will block regular server queries, like Spider or QConnect
    # e.g. they will query all of your servers within a second to update the list
    iptables -A quake3_ddos -m recent --update --name getstatus --hitcount 5 --seconds 2 -j DROP

    # accept otherwise
    iptables -A quake3_ddos -j ACCEPT

    #
    #
    # finally insert the chain as the top most input filter

    # single server
    # iptables -I INPUT 1 -p udp --dport 27960 -j quake3_ddos

    # multiple servers
    iptables -I INPUT 1 -p udp --dports 27960,27961,27962 -j quake3_ddos

I do not operate any high-traffic public servers, so I am not able to
confirm the usefulness of these iptables rules. However, from what I can
see, it looks promising. In addition, from chats with fellow server
admins on irc, apparently these attacks are originating from port 80. So
you may want to try adding this:

    iptables -I INPUT -p udp --sport 80 -j DROP

This blocks udp packets originating from port 80.  
In addition to iptables, [Rambetter][] from the [urban terror forums][]
is going to write a patch that supposedly limits DrDoS getstatus/getinfo
packets using a smart algorithm. Currently, the official patched
executable just limits the requests per time that can go through to the
target. However, since this still doesn't actually solve the issue,
targets are still being hit by data from the thousands of urban terror
servers on the master list. Hopefully with a combination of these
iptables rules and rambetter's upcoming patch, we can mitigate the
effects of the issue.

  [article]: http://www.altfire.com/main/news/index.php?news_id=586
    "altfire"
  [Rambetter]: http://daffy.nerius.com/urtserver/
    "rambetter's urt server patches"
  [urban terror forums]: http://www.urbanterror.info/forums/topic/27825-drdos/page__view__findpost__p__325612
    "rambetter on urt forums"
