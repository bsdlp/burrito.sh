Title: Migrate data in one line
Date: 2012-03-29 04:12
Author: nokbar
Category: bash, linux
Slug: migrate-data-in-one-line

So I find myself doing some repetitive tasks whenever I cancel a server
or when I'm setting up a new server and I need to transfer some files
over. Usually this is what happens:

I need to transfer my irssi configs, plugins and themes from
jchen@server1:\~/.irssi/ to jchen@server2:\~/.irssi/.  
In ssh:

    jchen@server1 ~$ tar zcvf irssi.tar.gz ~/.irssi/
    jchen@server1 ~$ scp irssi.tar.gz jchen@server2:~/
    jchen@server1 ~$ ssh jchen@server2
    jchen@server2 ~$ tar zxvf irssi.tar.gz

So this takes quite some time, and is quite annoying to type out. I've
been thinking about writing some scripts or whatever that will just grab
the most commonly used configs from a central server and sync the
central repo whenever a change is made. However, I thought that perhaps
that wouldn't really be any more time saving than just being better at
bash. So I googled around, and stumbled on this:

    jchen@server1 ~$ cd .irssi/
    jchen@server1 .irssi/$ tar zcf - irssi | ssh jchen@server2 tar xzf - -C ~/.irssi/

So thats basically a one-liner. What it does is it compresses the dir,
and then pipes it into ssh to transfer into server2 and then untars it
into the target directory.

Easypeasy.

Credits to huluwa over at lowendtalk.com
