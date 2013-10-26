Title: linode-python api tool
Date: 2013-03-11 19:30
Author: nokbar
Category: linode, linux, python, tutorial, web
Slug: linode-python-api-tool

Thanks to @[linode][]'s API and @[tjfontaine][] & co's [linode-python
api tool][], there's now an quick and easy way to programmatically
manage the many services offered by Linode.  
<!--more-->  
You'll want to grab pycurl first: `sudo pip install pycurl`

Check out the official [Linode API Documentation][] first, to make sure
you know what does what.

I use Linode's nameservers as slaves to my hidden master NSD3 server,
and I've got a bunch of active zones that need updating. All of the
domains that need to be migrated have the same MASTER\_IPS value, let's
use for example.

Let's take a look at what the output looks like for each domain request:

    from linode import api
    linode = api.Api('topsekritkey')

    for domain in linode.domain.list():
        print domain

This outputs something like:

`{u'STATUS': 1, u'RETRY_SEC': 0, u'DOMAIN': u'example.com', u'DOMAINID': 1337, u'DESCRIPTION': u'', u'MASTER_IPS': u'1.2.3.4;', u'SOA_EMAIL': u'', u'AXFR_IPS': u'1.2.3.4;', u'REFRESH_SEC': 0, u'TYPE': u'slave', u'EXPIRE_SEC': 0, u'TTL_SEC': 0} {u'STATUS': 1, u'RETRY_SEC': 0, u'DOMAIN': u'example.net', u'DOMAINID': 1338, u'DESCRIPTION': u'', u'MASTER_IPS': u'1.2.3.4;', u'SOA_EMAIL': u'', u'AXFR_IPS': u'1.2.3.4;', u'REFRESH_SEC': 0, u'TYPE': u'slave', u'EXPIRE_SEC': 0, u'TTL_SEC': 0}`

So on and so forth.

If the domain is of the type 'slave', then I'll want to grab that
domain's ID number, and then update that domain's MASTER\_IPS value to
my new master, 127.0.0.1.

    from linode import api
    linode = api.Api('topsekritkey')

    for domain in linode.domain.list():                                      # for each domain entry in the list,
        if domain['TYPE'] == 'slave':                                        # check if the domain is a slave entry, as I have some master entries mixed in,
            targetID = domain['DOMAINID']                                    # grab the domain ID,
            linode.domain.update(DomainID=targetID, MASTER_IPS='127.0.0.1')  # update the MASTERS_IPS value for $DomainID, if additional ips, semicolon ";" delimited.
            print(domain)                                                    # look pretty sorta.

That quick and dirty snippet should do the trick.

[Here][] are all the api actions available from [tjfontaine][]'s
[linode-python api tool][]:

  [linode]: http://www.linode.com/?r=a4cabf720dc4beb8628b63538a4b18aab7d0ed80
    "linode.com"
  [tjfontaine]: https://github.com/tjfontaine "tjfontaine on github"
  [linode-python api tool]: https://github.com/tjfontaine/linode-python
    "linode-python on github"
  [Linode API Documentation]: http://www.linode.com/api/
    "linode api documentation"
  [Here]: http://p.voltaire.sh/3 "linode api actions"
