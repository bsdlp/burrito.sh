Title: windows live email services
Date: 2013-03-31 18:01
Author: jchen
Category:
Slug: windows-live-email

So, [outlook.com][] is pretty slick. I think it can serve as a pretty
good alternative for gmail, now that google apps is now "free" but not
really free, and might be nuked at any time. So, how do you host your
domain's email on outlook?

Hit up <https://domains.live.com/Signup/SignupDomain.aspx>, and follow
the instructions. Make sure "Set up Outlook.com for my domain" is
checked.

If you want to use something like [Sparrow][] to send/receive your
email, you'll want to use these [settings][]:

`Incoming (POP3): Server address: pop3.live.com Port: 995 SSL Encryption: Yes`

`Outgoing (SMTP): Server address: smtp.live.com Port: 587 Authentication: Yes TLS or SSL Secure Encrypted Connection: Yes`

Use your new outlook email address and password for the authentication
fields. You need to make sure you put in user@domain.tld, not just
"user" into the username field. Then you should be good to go!

  [outlook.com]: http://outlook.com "outlook.com"
  [Sparrow]: http://www.sparrowmailapp.com/ "sparrow"
  [settings]: http://windows.microsoft.com/en-US/windows/outlook/send-receive-from-app
    "outlook pop3 smtp"
