Title: Teamspeak3 server management
Date: 2012-03-29 20:07
Author: jchen
Category:
Slug: teamspeak3-server-management

So I've been hosting some friends' teamspeak3 servers on the extra
resources I have on my VPS, and with a quick google, here's what I've
found extremely useful for managing ts3 virtual servers via telnet:

So for this guide, we will be using the following bogus information:  
Server IP: ts3.test.com  
Server port: 9987 (the default)  
sid: 2  
Server query port: 10011 (the default)  
Serveradmin password: 12345  
<!--more-->

**Log into the server:**  
On Linux:

    admin@test ~$ telnet ts3.test.com 10011
    Trying 123.456.789.123
    Connected to ts3.test.com.
    Escape character is '^]'.
    TS3
    Welcome to the TeamSpeak 3 ServerQuery interface, type "help" for a list of commands and "help " for information on a specific command.

At this point you should login as server admin. I will prefix all of my
inputs with a "\>".

    >login serveradmin 12345
    error id=0 msg=ok

Now that you are logged in, here's what you can do:

**Create a server:**

    >servercreate virtualserver_name=FriendlysTestsServer virtualserver_port=9987 virtualserver_maxclients=25
    sid=2 token=ygGoIJDppFQ5CfQPRt0mvJUCDXOylTv4YMkUIcye virtualserver_port=9987

The new server you have created has an sid of 2 and server port 9987.
You should save the token to gain admin rights in the server, but if you
lose it you can generate another token later via telnet. If you don't
specify a virtualserver\_port, it will assign the next available port
starting from 9987.

**Delete a server:**

    >serverstop sid=2
    error id=0 msg=ok
    >serverdelete sid=2
    error id=0 msg=ok

In order to delete a server, you have to stop it first. Pretty easy.

**Create new token to get admin rights:**  
If you lose your admin somehow, here's how you regain admin:  
First of all, look in your ts3 client and make sure advanced
permissions system is enabled in options.  
Then:  
Permissions -\> Server Groups  
Look in the leftmost area where it lists the groups. Find the group
with the highest permissions, and look at the group id number.  
For example,

Server admin (6)

That will be the group id number you use to generate a token.

    >use sid=2
    >tokenadd tokentype=0 tokenid1=6 tokenid2=0
    token=DC9X3JDNzYZM7ZnbuObL2LaOP46WT4jW5wS2Jom9
    error id=0 msg=ok

Set tokenid1 as the server admin group id number, and it will generate a
token for you. Copy the token, and go to:  
Permissions -\> Use Privilege Key  
and paste in the token. You should be admin again :)
