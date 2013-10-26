Title: Minecraft crashes if you run it on a secondary monitor on OSX?
Date: 2013-02-24 06:28
Author: jchen
Category:
Slug: minecraft-crashes-if-you-run-it-on-a-secondary-monitor-on-osx

So I've got two monitors set up. I was watching some movie on my main
monitor, and I decided I want to play some Minecraft on my other
monitor. The OSX menu bar is located on monitor 1. I launch up
Minecraft, and connect to my [server][]. But when I try to access the
menu to turn down the sound, the game locks up and crashes. lolwat?

Then I stumble upon this [Bug report][].

Ugh, lwjgl has a bad time capturing the pointer if the client isn't
running on the main monitor, the one with the OSX menu bar.

  [server]: http://mc.voltaire.sh/
  [Bug report]: https://mojang.atlassian.net/browse/MC-658
